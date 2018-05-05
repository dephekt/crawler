import requests
import warnings
from lxml import html
from urllib3 import exceptions

signature = '\\x76\\x75\\x75\\x77\\x64\\x2e\\x63\\x6f\\x6d\\x2f\\x74\\x2e\\x6a\\x73'
scansig_timeout = 5


def chunk_list(list_: list, size: int) -> list:
    """Take a list `list_` and break it down into a list of lists containing `size` elements per list.

    :param list_: A list of elements to be chunked.
    :type list_: list

    :param size: The number of elements per chunk.
    :type size: int

    :return: A list of chunks containing `size` elements per chunk.
    """
    return [
        list_[index:index + size]
        for index in range(0, len(list_), size)
    ]


def read_infile(infile: str = 'scanner_domains.txt') -> list:
    """Loads an input file containing a list of domains to scan.

    This loader should be called when the intention is to perform a scan against one domain at a time, synchronously.
    For running parallel scans, call the `read_infile_threaded` function instead.

    :param infile: A string containing the location of the output log file. Uses ``scanner_domains.txt`` from script
        runtime directory by default.
    :type infile: str

    :return: Returns a list of domains if successful, returns a list containing ``None`` otherwise.
    """
    try:
        with open(infile, 'r') as f:
            stack = f.readlines()
            f.close()
            return stack
    except FileNotFoundError:
        warnings.warn('Unable to open input file `%s`... File not found.' % infile)
        return [None]


def read_infile_threaded(infile: str = 'scanner_domains.txt', chunk_size: int = 25) -> list:
    """Loads an input file containing a list of domains to scan and chunks it.

    This loader should be called when making threaded requests. It takes a list of domains, divides them up into
    equal-numbered chunks of `chunk_size` domains and returns a `chunk_list` of lists of domains, where the index
    of `chunk_list` references a list of domains and the index of the domain list references a domain to scan.

    :param infile: A string containing the location of the output log file. Uses ``scanner_domains.txt`` by default.
    :type infile: str

    :param chunk_size: An integer indicating the number of domains to include in each map operation sent to the pool
        of workers. Larger chunks do not necessarily equate to faster processing. Default is 25 domains per chunk.
    :type chunk_size: int

    :return: Returns a list of domain chunks referencing lists of domains if successful, returns a list containing
        ``None`` otherwise.
    """
    try:
        with open(infile, 'rt', encoding='utf-8') as f:
            domain_chunks = chunk_list(f.readlines(), chunk_size)
    except FileNotFoundError:
        warnings.warn('Unable to open input file `%s`... File not found.' % infile)
        return [None]
    else:
        f.close()
        return domain_chunks


# pylint: disable=too-many-branches
def scan(domain: str, timeout: int) -> tuple:
    """Scans a list of domains for relevant metadata.

    Currently gets the homepage of a domain and returns the domain, page title, site meta description and HTTP status
    code of the request, if any, as a tuple of values.

    :param domain: A string containing a domain to scan for metadata.
    :type domain: str

    :param timeout: The number of seconds to wait before timing out.
    :type timeout: int

    :return: Returns a tuple of results.
    """
    domain = str(domain).strip()
    title = None
    desc = None

    try:
        r = requests.get('http://' + domain + '/', timeout=timeout)
        r.raise_for_status()
    except UnicodeError:
        return domain, None, None, 'UnicodeError'
    except exceptions.LocationValueError:
        return domain, None, None, None
    except exceptions.HeaderParsingError:
        warnings.warn('Error parsing headers for %s ...' % r.url)
    except requests.ConnectionError:
        return domain, title, desc, None
    except requests.HTTPError:
        return domain, title, desc, None
    except requests.Timeout:
        return domain, title, desc, 'Timeout'
    except requests.TooManyRedirects:
        return domain, title, desc, 'RedirectLoop'
    except requests.exceptions.ContentDecodingError:
        return domain, title, desc, 'ContentDecodingError'
    except requests.exceptions.ChunkedEncodingError:
        return domain, title, desc, 'ChunkedEncodingError'
    except requests.exceptions.InvalidSchema:
        return domain, title, desc, 'InvalidSchema'
    except requests.exceptions.InvalidURL:
        return domain, title, desc, 'InvalidURL'
    except requests.exceptions.InvalidHeader:
        return domain, title, desc, 'InvalidHeader'
    except requests.exceptions.FileModeWarning:
        return domain, title, desc, 'FileModeWarning'

    try:
        root = html.fromstring(r.content)
    except html.etree.ParserError:
        return domain, title, desc, 'Empty'

    try:
        title = root.xpath('/html/head/title')[0].text
    except Exception:
        title = None

    try:
        desc = root.xpath('/html/head/meta[@name="description"]/@content')[0]
    except Exception:
        desc = None

    return domain, title, desc, r.status_code


def scansig(url: str) -> tuple:
    """Scans a list of URLs for a given signature.

    :param url: A string containing a URL to scan for a given signature.
    :type url: str

    :return: Returns a tuple of results.
    """
    url = str(url).strip()
    try:
        r = requests.get(url, timeout=scansig_timeout)
        r.raise_for_status()
    except Exception:
        pass
    else:
        if r.ok:
            if r.text.find(signature) != -1:
                print('Signature detected at %s ...' % url)
                return url, 'ScanSignatureDetected'
            return url, None
        return url, None


def write_outfile(results: tuple, outfile: str = 'scanner_log.txt', clobber: bool = False) -> bool:
    """Writes tuples of results as tuples to the output log file.

    This is for processing synchronous results from a non-threaded scan.

    :param results: Metadata about the scan to be logged.
    :type results: tuple

    :param outfile: A string containing the location of the output log file. Uses ``scanner_log.txt`` by default.
    :type outfile: str

    :param clobber: A boolean to determine if an existing log should be clobbered or not.
    :type clobber: bool

    :return: Returns ``True`` if the operation was successful, ``False`` otherwise.
    """
    if clobber:
        log_file_action = 'wt'
    else:
        log_file_action = 'at'

    try:
        with open(outfile, log_file_action) as f:
            print(str(results).encode("utf-8"), file=f)
    except FileNotFoundError:
        warnings.warn('Unable to open output file `%s`... File not found.' % outfile)
    else:
        if f:
            f.close()
        return True


def write_outfile_async(iterable: list, outfile: str = 'scanner_log.txt') -> bool:
    """Iterates on a list of tuples of results and writes each result as a tuple to the output log file.

    This is for processing results of an asynchronous/threaded scan.

    :param iterable: A list containing metadata about the scanned chunk to be logged.
    :type iterable: tuple

    :param outfile: A string containing the location of the output log file. Uses ``scanner_log.txt`` by default.
    :type outfile: str

    :return: Returns ``True`` if the operation was successful, ``False`` otherwise.
    """
    if iterable.__len__() is not 0 or iterable.__len__() is not False:
        for results in iterable:
            if results is not None:
                with open(outfile, 'a') as f:
                    print(str(results).encode("utf-8"), file=f)
        if f:
            f.close()
        return True
    else:
        return False
