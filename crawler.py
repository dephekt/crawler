import requests
import warnings
from lxml import html
from urllib3 import disable_warnings
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count

disable_warnings()


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
    with open(infile, 'rt') as f:
        return f.readlines()


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
    with open(infile, 'rt') as f:
        return chunk_list(f.read().splitlines(), chunk_size)


def scan(infile: str = 'scanner_domains.txt', outfile: str = 'scanner_log.txt', signature: str = 'None'):
    """Scans an input list for metadata and, optionally, for the presence of a given signature and sends the results to
    be written to a file.

    :param infile: An optional string containing the path to the input data to use for this scan.
    :param outfile: An optional string containing the path to the output file to write results to.
    :param signature: An optional string containing the signature to check each input item for.
    """
    pool = Pool(cpu_count() * 10)
    batch = read_infile_threaded(infile)
    batch_counter = 0
    batch_count = batch.__len__()
    for item in batch:
        batch_counter += 1
        print('Batch #{0} | Batches remaining: {1} | {2}% complete'.format(
            batch_counter,
            batch_count - batch_counter,
            round(100 * (batch_counter / batch_count), 3),
        ))
        responses = pool.map(get, item)
        for response in responses:
            sig_detect = 'N/A'
            if response[0]:
                doc_html = response[2]
                doc_text = response[3]
                metadata = metadata_parse(doc_html)
                if signature != 'None':
                    sig_detect = signature_parse(doc_text, signature)
                write_outfile(
                    '{0}, {1}, {2}, {3}'.format(response[1], metadata.get('title'), metadata.get('desc'), sig_detect),
                    outfile
                )
            else:
                write_outfile('{0}, \'{1}\''.format(response[1], response[2]), outfile)


def get(target: str) -> tuple:
    """Fetches a document via HTTP/HTTPS and returns a tuple containing a boolean indicating the result of the request,
     the URL we attempted to contact and the request HTML content in bytes and text format, if successful.

     Otherwise, returns a tuple containing a boolean indicating the result of the request, the URL we attempted to
     contact and the HTTP status code or exception error output from the request.

    :param target:
    :return: tuple
    """
    if target.startswith('http://') is False and target.startswith('https://') is False:
        target = 'http://{0}'.format(target)
    try:
        request = requests.get(url=target, timeout=3, verify=False)
    except Exception as e:
        return False, target, e.__str__()

    try:
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return False, target, e.__str__()
    if request.ok:
        return True, request.url, request.content, request.text

    return False, request.url, request.status_code


def metadata_parse(content: bytes) -> dict:
    """Parses raw HTML content as bytes and returns the page's meta-description and HTML title tag values as a
     dictionary in the form: {'title': <page title>, 'desc': <page description>}.

    :param content: bytes of HTML
    :return: dict{'title': <page title>, 'desc': <page description>}
    """
    title = 'None'
    desc = 'None'
    try:
        root = html.fromstring(content)
    except html.etree.ParserError:
        return {'title': title, 'desc': desc}

    try:
        title = "'{0}'".format(root.xpath('/html/head/title')[0].text)
    except Exception:
        title = 'None'

    try:
        desc = "'{0}'".format(root.xpath('/html/head/meta[@name="description"]/@content')[0])
    except Exception:
        desc = 'None'

    return {'title': title, 'desc': desc}


def signature_parse(content: str, signature: str) -> bool:
    """Parses given text looking for the presence of a given signature. Returns ``True`` if the signature was found,
    ``False`` otherwise.

    :param content: str
    :param signature: str
    :return: bool
    """
    if content.find(signature) != -1:
        return True

    return False


def write_outfile(results: str, outfile: str = 'scanner_log.txt'):
    """Writes tuples of results as tuples to the output log file.

    This is for processing synchronous results from a non-threaded scan.

    :param results: Metadata about the scan to be logged.
    :type results: tuple

    :param outfile: A string containing the location of the output log file. Uses ``scanner_log.txt`` by default.
    :type outfile: str

    :return: Returns ``True`` if the operation was successful, ``False`` otherwise.
    """
    try:
        with open(outfile, 'ab') as f:
            f.write(str(results + '\n').encode())
    except FileNotFoundError:
        warnings.warn('Unable to open output file {0}'.format(outfile))


def write_outfile_async(iterable: list, outfile: str = 'scanner_log.txt'):
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
                try:
                    with open(outfile, 'ab') as f:
                        f.write(str(results + '\n').encode())
                except FileNotFoundError:
                    warnings.warn('Unable to open output file {0}'.format(outfile))
