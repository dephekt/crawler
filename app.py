import crawler
import argparse
import logging
import warnings
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from functools import partial

parser = argparse.ArgumentParser()
parser.add_argument('--scan', help='perform a scan', action='store_true')
parser.add_argument('--threaded', help='distribute scanning tasks over multiple threads', action='store_true',)
parser.add_argument('--chunks', help='indicates the number of domains each chunk should contain', type=int,)
parser.add_argument('--workers', help='indicates the number of workers to give the processing pool', type=int,)
parser.add_argument('--scansig',
                    help='indicates we are scanning for a signature match rather than metadata',
                    action='store_true',
                    )
parser.add_argument('--sig', help='sig', action='store')
parser.add_argument('--infile', help='set a custom domain input file location [default: scanner_domains.txt]',)
parser.add_argument('--outfile', help='set a custom output log file location [default: scanner_log.txt]',)
parser.add_argument('--clobber', help='wipe and reuse the log instead of appending to it', action='store_true',)
parser.add_argument('--debug', help='enable debugging output to the console', action='store_true',)
parser.add_argument('--verbose', help='enable informational output to the console', action='store_true',)
parser.add_argument('--timeout', help='number of seconds to wait for a scan response before timing out', type=int,)
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
    warnings.warn('Debug logging enabled ...')
elif args.verbose:
    logging.basicConfig(level=logging.INFO)
    logging.info('Informative logging to console is enabled ...')

if args.scansig is True and args.sig is None:
    warnings.warn('If `--scansig` is passed you must pass a signature to scan for using `--sig <signature>`')
    exit(1)

if args.scan is True and args.scansig is True:
    warnings.warn('`--scan` and `--scansig` are mutually exclusive ... You must specify one or the other!')
    exit(1)

if args.infile:
    logging.info('Using user provided domain input file %s ...', args.infile)
else:
    logging.info('Using default domain input file as `--infile` was not provided at runtime ...')

if args.outfile:
    logging.info('Using user provided output log file %s ...', args.outfile)
else:
    logging.info('Using default scan output file as `--outfile` was not provided at runtime ...')

if args.clobber:
    logging.info('Clobbering log file since `--clobber` was provided at runtime ...')
else:
    logging.info('Output file will be appended to if it exists as `--clobber` was not provided at runtime ...')

if args.timeout:
    timeout = args.timeout
    logging.info('Using user-provided network timeout of %i ...', args.timeout)
else:
    timeout = 10
    logging.info('Using default network timeout of %i ...', timeout)

if args.scan is True and args.threaded is False and args.scansig is False:
    if args.infile:
        stack = crawler.read_infile(args.infile)
    else:
        stack = crawler.read_infile()

    try:
        if stack.__len__() and stack[0] is not None:
            while stack:
                domain = stack.pop().strip()
                if domain is not None:
                    scan_results = crawler.scan(domain, timeout=timeout)
                    if args.outfile:
                        log_status = crawler.write_outfile(scan_results, args.outfile, args.clobber)
                    else:
                        log_status = crawler.write_outfile(scan_results, clobber=args.clobber)
                    if args.debug:
                        try:
                            print(str(scan_results))
                        except UnicodeEncodeError:
                            pass
    except AttributeError:
        warnings.warn('Unable to pop a domain off the stack ... Does infile contain domains?')

if args.threaded is True and args.scan is True or args.scansig is True:
    if args.workers is not None:
        pool = Pool(args.workers)
        print('Created a worker pool with %i workers ...' % args.workers)
    else:
        pool = Pool(cpu_count())
        print('Created a worker pool with %i workers ...' % cpu_count())

    if args.infile and args.chunks:
        domain_chunks = crawler.read_infile_threaded(args.infile, args.chunks)
        print('Mapping %i domains per chunk to worker pool ...' % args.chunks)
    elif args.infile:
        domain_chunks = crawler.read_infile_threaded(args.infile)
    else:
        domain_chunks = crawler.read_infile_threaded()

    if domain_chunks[0] is None:
        warnings.warn('Unable to read any domain chunks from the provided domain input file %s ...' % args.infile)
        exit(1)
    else:
        print('This workload contains %i chunks to be processed ...' % domain_chunks.__len__())

    chunk_counter = 0
    log_result = False
    for domains in domain_chunks:
        chunk_counter += 1
        print('Sent %s domains to processing so far ...' % str(chunk_counter * domains.__len__()))

        if args.scansig is True and args.scan is False:
            logging.info('Signature scanning because `--scansig` was given at runtime ...')
            map_results = pool.map(partial(crawler.scansig, signature=args.sig, timeout=timeout), domains)
            if args.outfile:
                log_result = crawler.write_outfile_async(map_results, outfile=args.outfile)
            else:
                log_result = crawler.write_outfile_async(map_results)

        elif args.scan is True and args.scansig is False:
            logging.info('Metadata scanning because `--scan` was given at runtime ...')
            map_results = pool.map(partial(crawler.scan, timeout=timeout), domains)

        if log_result:
            logging.info('Successfully wrote a batch of results to the output log ...')
        else:
            logging.info('Failed to write a batch of results to the output log ...')
