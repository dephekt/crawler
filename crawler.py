from lxml import html
import requests


def read_infile(infile='scanner_domains.txt') -> list:
    """Loads an input file containing a list of domains to scan.

    Parameters
    ----------
    infile : str
        A string containing the location of the output log file.
        Uses ``scanner_domains.txt`` from script runtime directory by default.

    Returns
    -------
    list
        Returns a list of domains if successful, ``None`` otherwise.
    """
    try:
        with open(infile, 'r') as f:
            stack = f.readlines()
            f.close()
            return stack
    except FileNotFoundError:
        print('Unable to open input file `' + str(infile) + '`... File not found.')
        return [None]


def scan(domain: str, timeout=30) -> tuple:
    """Scans a list of domains for relevant metadata.

    Parameters
    ----------
    domain : str
        A string containing a domain to scan for metadata.
    timeout : int
        An integer indicating the number of seconds to wait for a response before timing out.

    Returns
    -------
    tuple
        Returns a tuple of results.
    """
    title = None
    desc = None

    try:
        # Make a GET request to the domain
        r = requests.get('http://' + domain + '/', timeout=timeout)
        r.raise_for_status()
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

    try:
        root = html.fromstring(r.content)
    except html.etree.ParserError:
        return domain, title, desc, 'Empty'

    # Store the address of the page title element
    title_path = root.xpath('/html/head/title')
    if title_path:
        try:
            title = title_path[0].text
        except UnicodeDecodeError:
            title = 'UnicodeDecodeError'
    else:
        title = None

    # Store the address of the meta description content element
    desc_path = root.xpath('/html/head/meta[@name="description"]/@content')
    if desc_path:
        try:
            desc = desc_path[0]
        except UnicodeDecodeError:
            desc = 'UnicodeDecodeError'
    else:
        desc = None

    # Return a tuple of the domain, title, description and HTTP status code
    return domain, title, desc, r.status_code


def write_outfile(results: tuple, outfile='scanner_log.txt', clobber=False) -> bool:
    """Writes results as tuples to the output log file.

    Parameters
    ----------
    results : tuple
        A tuple of metadata to be logged.
    outfile : str
        A string containing the location of the output log file.
        Uses ``scanner_log.txt`` from script runtime directory by default.
    clobber : bool
        A boolean to determine if an existing log will be clobbered.
        ``True`` if the log will be clobbered, ``False`` otherwise.

    Returns
    -------
    bool
        Returns ``True`` if the operation was successful, ``False`` otherwise.
    """
    if clobber:
        log_file_action = 'w'
    else:
        log_file_action = 'a'

    try:
        # Open the output log file and write incoming tuples to it.
        with open(outfile, log_file_action) as f:
            print(str(results).encode("utf-8"), file=f)
            f.close()
            return True
    except FileNotFoundError:
        print('Unable to open output file `' + str(outfile) + '`... File not found.')
