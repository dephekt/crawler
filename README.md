# crawler
[![pipeline status](https://gitlab.com/dephekt/crawler/badges/master/pipeline.svg)](https://gitlab.com/dephekt/crawler/commits/master)

Takes a text file of domains as input, then iterates through the list, gathering the page title, meta-description and HTTP status of each domain.

It can also handle very large data sets by running many scan processes concurrently, with facilities for user-defined process workers `--workers` and domains-per-chunk `--chunks`.

Writes results to `scanner_log.txt` by default and (in the future) optionally to CSV.



### Running the Application
Basic usage instructions can be found with:

    $ python app.py --help
    
    usage: app.py [-h] [--scan] [--infile INFILE] [--outfile OUTFILE] [--clobber]
              [--debug]

    optional arguments:
      -h, --help         show this help message and exit
      --scan             perform a scan
      --threaded         distribute scanning tasks over multiple threads
      --chunks CHUNKS    indicates the number of domains each chunk should contain
      --workers WORKERS  indicates the number of workers to give the processing pool
      --infile INFILE    set a custom domain input file location
      --outfile OUTFILE  set a custom output log file location
      --clobber          wipe and reuse the log instead of appending to it
      --debug            enable debugging output to the console
      --verbose          enable informational output to the console
      --timeout TIMEOUT  number of seconds to wait for a scan response before timing out


Ensure that `scanner_domains.txt` exists in the same directory as `app.py` that it contains at least one domain name. Additional domains should be on new lines.

Optionally, one can pass `--infile <input file>` or `--outfile <output file>` to specify a custom path and filename.

Then run:

    python app.py --scan

By default, the application will log scan results to  `scanner_log.txt` if `--outfile` is not passed.

To enable logging to the console pass `--verbose` to `app.py`, for example:

    python app.py --scan --verbose --infile C:\domains.txt --outfile C:\scan_log.txt

### Obtaining the Application

##### Using Git
Clone this repository using Git:

    git clone git@code.dephekt.net:dephekt/crawler.git

Then change into the `crawler/` directory git created.

    cd crawler

Checkout the release version you intend to run:

    git checkout <release tag>

### Setting up a Python Virtual Environment
This is an optional, but highly recommended, standard practice to keep per-project Python dependencies isolated from system-wide installed modules.

##### With Pipenv:
To use Pipenv, install it with:

    python3 -m pip install --user pipenv

##### MacOS:
Alternatively, pipenv may be installed on MacOS with Homebrew using:

    brew install pipenv

##### Ubuntu 17.10:
Ubuntu 17.10 users can install it with `apt` using the APT PPA repository:

    sudo apt-get install software-properties-common python-software-properties
    sudo add-apt-repository ppa:pypa/ppa
    sudo apt-get update
    sudo apt-get install pipenv

When Pipenv is installed, change to the crawler app's root directory `crawler/` and run:

    python3 -m pipenv install

This will create a new virtual environment and install all the Python modules necessary to run the application.

You may need to activate the `pipenv shell` in your terminal to be in the proper environment context. You can do that from the project root directory `crawler/` with:

    python3 -m pipenv shell

For more information on using Pipenv, you can review its documentation [here](https://docs.pipenv.org/).  

### Manual Dependency List:
You can alternatively use other Python environment and package management tools, such as `conda`, `virtualenv` or `venv` as well as directly installing modules using `pip`.

The following is a list of dependencies that need to be installed one way or another:

* Python 3.x
* [lxml](https://pypi.org/project/lxml/)
* [requests](https://pypi.org/project/requests/)

This list may or may not be current. Always check `Pipfile` in the application root directory for the most up-to-date information.

##### Expecting Python 2.x Support?
There will never be Python 2.x support for this; Python 2.7 support sunsets on January 1, 2020. See [this statement](http://python3statement.org/) regarding the move to Python 3.

### Bugs and Issues
Please report any problems or feature requests using the issue tracker on GitLab. Please include the domain which triggered the problem as well as the full Python traceback if an exception was encountered.
