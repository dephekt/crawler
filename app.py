import crawler
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--scan', help='perform a scan', action='store_true')
parser.add_argument('--infile', help='set a custom domain input file location [default: scanner_domains.txt]')
parser.add_argument('--outfile', help='set a custom output log file location [default: scanner_log.txt]')
parser.add_argument('--clobber', help='wipe and reuse the log instead of appending to it', action='store_true')
parser.add_argument('--debug', help='enable debugging output', action='store_true')
parser.add_argument('--timeout', help='number of seconds to wait for a scan response before timing out [default: 30]')
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

if args.clobber:
    clobber = True
    if args.debug:
        print('Clobbering log file since `--clobber` was passed at runtime...')
else:
    clobber = False

if args.timeout:
    timeout = int(args.timeout)
else:
    timeout = 30

if args.scan:
    if infile:
        stack = crawler.read_infile(args.infile)
    else:
        stack = crawler.read_infile()

    try:
        while stack:
            domain = stack.pop().strip()
            scan_results = crawler.scan(domain, timeout=timeout)
            if outfile:
                log_status = crawler.write_outfile(scan_results, args.outfile, clobber)
            else:
                log_status = crawler.write_outfile(scan_results, clobber=clobber)
            if args.debug:
                try:
                    print(str(scan_results))
                except UnicodeEncodeError:
                    pass

    except AttributeError:
        if args.debug:
            print('Unable to pop a domain off the stack... Does file: `' + str(args.infile) + '` contain domains?')
