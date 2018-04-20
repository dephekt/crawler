# crawler
Takes a text file of domains separated by newlines, `scanner_domains.txt`, as input, then crawls through the list, gathering the page title and meta-description for each domain.

Writes results as a tuple to stdout and to `scanner_log.txt`.

### Setting up the Virtual Environment

#### Using Pipenv:

Change to the application's root directory (where `app.py` is located), then run the following.

    python -m pipenv install

#### Installing Pipenv:

If `pipenv` is not installed, it can be installed with `pip`.

    python -m pip install pipenv

### Running the Application

Ensure that `scanner_domains.txt` exists in the same directory as `app.py` and contains at least one domain name. Additional domains should be on new lines. Then run:

    python app.py --scan

The application should log to `stdout` and to `scanner_log.txt`.