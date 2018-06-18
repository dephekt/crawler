# crawler
[![pipeline status](https://gitlab.com/dephekt/crawler/badges/master/pipeline.svg)](https://gitlab.com/dephekt/crawler/commits/master)

Takes a text file of domains as input, then iterates through the list, gathering the page title, meta-description and HTTP status of each domain.

It can also handle very large data sets by running many scan processes concurrently.

Writes results to `scanner_log.txt` by default.

### Running the Application
Basic usage instructions can be found with:

    $ python scan.py -h
    usage: scan.py [-h] [-i FILE] [-o FILE] [--sig TEXT] [-d]
    
    optional arguments:
      -h, --help            show this help message and exit
      -i FILE, --infile FILE
                            set a custom domain input file location
      -o FILE, --outfile FILE
                            set a custom output log file location
      --sig TEXT            provide a signature string to scan each target for
      -d, --debug           enable debugging output to the console


Ensure that `scanner_domains.txt` exists in the same directory as `scan.py` that it contains at least one domain name. Additional domains should be on new lines.

Optionally, one can pass `-i <input file>` or `-o <output file>` to specify a custom path and filename.

Then run:

    python scan.py

By default, the application will log scan results to  `scanner_log.txt` if `-o` is not passed.

### Obtaining the Application

##### Using Git
Clone this repository using Git:

    git clone https://@gitlab.com:dephekt/crawler.git

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
