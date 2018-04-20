# crawler
Takes a text file of domains separated by newlines as input, then crawls through the list, gathering the page title and meta-description for each domain.

Writes results as a tuple to stdout and to `scanner_log.txt`.

### Setting up the Virtual Environment

#### Using Pipenv:

Change to the application's root directory (where `app.py` is located), then run the following.

    python -m pipenv install

#### Installing Pipenv:

If `pipenv` is not installed, it can be installed with `pip`.

    python -m pip install pipenv

