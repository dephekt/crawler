# crawler
Takes a text file, `scanner_domains.txt`, of domains separated by newlines as input, then crawls through the list, gathering the page title and meta-description for each domain.

Writes results as a tuple to `scanner_log.txt` by default and optionally to `stdout` if `--debug` is provided.

### Obtaining the Application

##### Using Git
Clone this repository using Git:

    git clone https://github.com/dephekt/crawler.git

Then change into the `crawler/` directory git created.

    cd crawler

Checkout the release version you intend to run:

    git checkout v1.2-alpha

##### Downloading a Release Archive  
Alternatively to using Git, one can download the latest release from the [releases](https://github.com/dephekt/crawler/releases) tab. Download a release, extract the archive, then change into the application directory and proceed to install a Python virtual environment and runtime dependencies.

### Setting up a Python Virtual Environment
This is an optional, but highly recommended, standard practice to keep per-project Python dependencies isolated from system-wide installed modules.

##### With Pipenv:
To use Pipenv, install it with:

    python -m pip install pipenv

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

    python -m pipenv install

This will create a new virtual environment and install all the Python modules necessary to run the application.

You may need to activate the `pipenv shell` in your terminal to be in the proper environment context. You can do that from the project root directory `crawler/` with:

    python -m pipenv shell

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

### Running the Application

Basic usage instructions can be found with:

    $ python app.py --help
    
    usage: app.py [-h] [--scan] [--infile INFILE] [--outfile OUTFILE] [--clobber]
              [--debug]

    optional arguments:
      -h, --help         show this help message and exit
      --scan             perform a scan
      --infile INFILE    set a custom domain input file location
      --outfile OUTFILE  set a custom output log file location
      --clobber          wipe and reuse the log instead of appending to it
      --debug            enable debugging output


Ensure that `scanner_domains.txt` exists in the same directory as `app.py` and contains at least one domain name. Additional domains should be on new lines.
Optionally, one can pass `--infile <input file>` or `--outfile <output file>` to specify a custom path and filename.

Then run:

    python app.py --scan

By default, the application will log scan results to  `scanner_log.txt` if `--outfile` is not passed.

To enable logging to the console pass `--debug` to `app.py`, for example:

    python app.py --scan --debug --infile C:\domains.txt --outfile C:\scan_log.txt

### Bugs and Issues
Please report any problems or feature requests using the [issues tab](https://github.com/dephekt/crawler/issues) on the GitHub project. Please include the domain which triggered the problem as well as the full Python traceback if an exception was encountered.
