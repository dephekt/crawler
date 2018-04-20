import crawler
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--scan', help='perform a scan', action='store_true')
parser.add_argument('--infile', help='set a custom domain input file location')
parser.add_argument('--outfile', help='set a custom output log file location')
args = parser.parse_args()

if args.scan:
    stack = crawler.read_infile()

    if type(stack) is list:
        while stack:
            domain = stack.pop().strip()
            scan_results = crawler.scan(domain)
            log_status = crawler.write_outfile(scan_results)
            print(str(scan_results))
