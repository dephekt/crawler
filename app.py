import crawler
import argparse
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count


parser = argparse.ArgumentParser()
parser.add_argument('--scan', help='perform a scan', action='store_true')
parser.add_argument('--threaded', help='distribute scanning tasks over multiple threads', action='store_true')
parser.add_argument('--chunks', help='indicates the number of domains each chunk should contain', type=int)
parser.add_argument('--workers', help='indicates the number of workers to give the processing pool', type=int)
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
    timeout = 10

if args.scan is True and args.threaded is False:
    domain = None
    if infile:
        stack = crawler.read_infile(args.infile)
    else:
        stack = crawler.read_infile()

    try:
        if stack.__len__() and stack[0] is not None:
            while stack:
                domain = stack.pop().strip()
                if domain is not None:
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

if args.threaded is True and args.scan is True:
    if args.workers is not None:
        pool = Pool(args.workers)
        if args.debug:
            print('Created a worker pool with ' + str(args.workers) + ' workers...')
    else:
        pool = Pool(cpu_count())
        if args.debug:
            print('Created a worker pool with ' + cpu_count().__str__() + ' workers...')

    if infile and args.chunks:
        domain_chunks = crawler.read_infile_threaded(args.infile, args.chunks)
        if args.debug:
            print('Mapping ' + str(args.chunks) + ' domains per chunk to the worker pool...')
    elif infile:
        domain_chunks = crawler.read_infile_threaded(args.infile)
    else:
        domain_chunks = crawler.read_infile_threaded()

    print('This workload contains ' + domain_chunks.__len__().__str__() + ' chunks to be processed...')
    chunk_counter = 0
    for domains in domain_chunks:
        chunk_counter += 1
        print('Sent ' + str(chunk_counter * domains.__len__()) + ' domains to processing so far...')
        results = pool.map(crawler.scan, domains)
        print('Processed domains: ' + str(domains))
        for result in results:
            if outfile:
                crawler.write_outfile(result, args.outfile, clobber)
            else:
                crawler.write_outfile(result, clobber=clobber)
            if args.debug:
                print(str(result))
