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


def scan(domain: str) -> tuple:
    """Scans a list of domains for relevant metadata.

    Parameters
    ----------
    domain : str
        A string containing a domain to scan for metadata.

    Returns
    -------
    tuple
        Returns a tuple of results.
    """
    try:
        # Make a GET request to the domain
        r = requests.get('http://' + domain + '/')
        r.raise_for_status()

        # Store the elements to a tree to reference later
        root = html.fromstring(r.content)

        # Store the address of the page title element
        title_path = root.xpath('/html/head/title')
        if title_path:
            title = title_path[0].text
        else:
            title = None

        # Store the address of the meta description content element
        desc_path = root.xpath('/html/head/meta[@name="description"]/@content')
        if desc_path:
            desc = desc_path[0]
        else:
            desc = None

        # Return a tuple of the domain, title, description and HTTP status code
        return domain, title, desc, r.status_code
    except requests.exceptions.RequestException:
        return domain, title, desc, None


def write_outfile(results: tuple, outfile='scanner_log.txt') -> bool:
    """Writes results as tuples to the output log file.

    Parameters
    ----------
    results : tuple
        A tuple of metadata to be logged.
    outfile : str
        A string containing the location of the output log file.
        Uses ``scanner_log.txt`` from script runtime directory by default.

    Returns
    -------
    bool
        Returns ``True`` if the operation was successful, ``False`` otherwise.
    """
    try:
        # Open the output log file and write incoming tuples to it.
        with open(outfile, 'a') as f:
            print(str(results).encode("utf-8"), file=f)
            f.close()
            return True
    except FileNotFoundError:
        print('Unable to open output file `' + str(outfile) + '`... File not found.')
