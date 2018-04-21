# crawler
Takes a text file, `scanner_domains.txt`, of domains separated by newlines as input, then crawls through the list, gathering the page title and meta-description for each domain.

Writes results as a tuple to `scanner_log.txt` by default and optionally to `stdout` if `--debug` is provided.

### Obtaining the Application

Clone this repository using `git clone https://github.com/dephekt/crawler.git` or download the latest release from the [releases](https://github.com/dephekt/crawler/releases) tab. Then, change into the application directory and proceed to install Python runtime dependencies.

### Installing Runtime Dependencies

#### Using Pipenv:

Change to the application's root directory (where `app.py` is located), then run the following.

    python -m pipenv install

#### Installing Pipenv:

If `pipenv` is not installed, it can be installed with `pip`.

    python -m pip install pipenv

#### Dependencies

* Python 3.x - [Anaconda for Windows](https://www.anaconda.com/download/#download)
* [lxml](https://pypi.org/project/lxml/)
* [requests](https://pypi.org/project/requests/)

### Running the Application

Basic usage instructions can be found with:

    python app.py --help

Ensure that `scanner_domains.txt` exists in the same directory as `app.py` and contains at least one domain name. Additional domains should be on new lines.
Optionally, one can pass `--infile <input file>` or `--outfile <output file>` to specify a custom path and filename.

Then run:

    python app.py --scan

By default, the application will log scan results to  `scanner_log.txt` if `--outfile` is not passed.

To enable logging to the console pass `--debug` to `app.py`, for example:

    python app.py --scan --debug --infile C:\domains.txt --outfile C:\scan_log.txt
