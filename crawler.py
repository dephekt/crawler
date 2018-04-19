from lxml import html
import requests


def read_infile(infile='scanner_domains.txt') -> list:
    """Loads an input file containing a list of domains to scan.

    Parameters
    ----------
    infile : str
        Filesystem path to the local input file to use.
        Uses ``scanner_domains.txt`` from script runtime directory by default.

    Returns
    -------
    list
        Returns a list of domains if successful, ``None`` otherwise.
    """
    try:
        # Read our input file, store all the lines to stack and return it
        with open(infile, 'r') as f:
            stack = f.readlines()
            f.close()
            return stack
    except:
        print('Unable to open input file: ' + infile)
        return None


def scan(domains: list) -> tuple:
    """Scans a list of domains for relevant metadata.

    Parameters
    ----------
    domains : list
        A list of domains to scan for metadata.

    Returns
    -------
    tuple
        Returns a tuple of results if successful, ``None`` otherwise.
    """
    while domains:
        try:
            # Pop the first domain from the stack
            domain = domains.pop().strip()

            # Make a GET request to the domain
            r = requests.get('http://' + domain + '/')
            statuscode = r.status_code

            # Store the elements to a tree to reference later
            root = html.fromstring(r.content)

            # Store the address of the page title element
            title = root.xpath('/html/head/title')

            # Store the address of the meta description content element
            desc = root.xpath('/html/head/meta[@name="description"]/@content')

            # Return a tuple of the domain, title and description
            return domain, title, desc, statuscode
        except:
            return None

    return None


def write_result(results: tuple) -> bool:
    #urltitle = title[0].text
    #urltitle = str(None)
    #url_desc = desc[0]
    #url_desc = str(None)

    print(str(results))
    return False