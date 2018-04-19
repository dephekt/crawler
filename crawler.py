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

            # Store the elements to a tree to reference later
            root = html.fromstring(r.content)

            # Store the address of the page title element
            title_path = root.xpath('/html/head/title')
            if type(title_path) is list:
                title = title_path[0].text
            else:
                title = None

            # Store the address of the meta description content element
            desc_path = root.xpath('/html/head/meta[@name="description"]/@content')
            if type(desc_path) is list:
                desc = desc_path[0]
            else:
                title = None

            # Return a tuple of the domain, title, description and HTTP status code
            return domain, title, desc, r.status_code
        except:
            return None

    return None


def write_outfile(results: tuple) -> bool:
    """Writes results as tuples to the output log file.
    
    Parameters
    ----------
    results : tuple
        A tuple of metadata to be logged.
    
    Returns
    -------
    bool
        Returns ``True`` if the operation was successful, ``False`` otherwise.
    """
    try:
        # Open the output log file and write incoming tuples to it.
        with open(scanner_domains.txt, 'a') as f:
            print(str(results), file=f)
            f.close()
            return True
    except:
        print('Unable to open output file: ' + outfile)
        return False

    return False