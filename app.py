import crawler
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--scan', help='perform a scan', action='store_true')
parser.add_argument('--infile', help='set a custom domain input file location')
parser.add_argument('--outfile', help='set a custom output log file location')
parser.add_argument('--debug', help='enable debugging output', action='store_true')
args = parser.parse_args()

if args.infile:
    infile = True
    if args.debug:
        print('Using user provided location for domain input file...')
else:
    infile = False

if args.outfile:
    outfile = True
    if args.debug:
        print('Using user provided location for output log file...')
else:
    outfile = False

if args.scan:
    if infile:
        stack = crawler.read_infile(args.infile)
    else:
        stack = crawler.read_infile()

    try:
        while stack:
            domain = stack.pop().strip()
            scan_results = crawler.scan(domain)
            if outfile:
                log_status = crawler.write_outfile(scan_results, args.outfile)
            else:
                log_status = crawler.write_outfile(scan_results)
            if args.debug:
                print(str(scan_results))
    except AttributeError:
        if args.debug:
            print('Unable to pop a domain off the stack... Does file: `' + str(args.infile) + '` contain domains?')
