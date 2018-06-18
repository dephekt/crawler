import crawler
import argparse
import logging
import warnings

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help='set a custom domain input file location',
                        default='scanner_domains.txt', metavar='FILE')
    parser.add_argument('-o', '--outfile', help='set a custom output log file location', default='scanner_log.txt',
                        metavar='FILE')
    parser.add_argument('--sig', help='provide a signature to scan each target for', action='store', default='None',
                        metavar='TEXT')
    parser.add_argument('-d', '--debug', help='enable debugging output to the console', action='store_true',)
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        warnings.warn('Debug logging enabled ...')

    crawler.scan(infile=args.infile, outfile=args.outfile, signature=args.sig)
