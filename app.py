import crawler
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('--scan', help='perform a scan', action='store_true')
parser.add_argument('--infile', help='set a custom domain input file location')
parser.add_argument('--outfile', help='set a custom output log file location')
args = parser.parse_args()


while args.scan:
    infile_present = os.path.exists(args.infile)
    outfile_present = os.path.exists(args.outfile)
    
    infile = args.infile
    outfile = args.outfile
    
    if (infile_present and outfile_present):
        stack = crawler.read_infile(infile)
        scan_results = crawler.scan(stack)
        log_status = crawler.write_outfile(outfile)
    elif infile_present = False:
        print('Input file does not exist... doing nothing.')
    elif outfile_present = False:
        print('Output file does not exist... doing nothing.')