'''getdir.py [options] [args]

Usage:
    getdatadir.py -d <folder>
    getdatadir.py -c <folder>

Options:
    -d    Open data directory
    -c    Open cache directory

'''

from xml.sax.saxutils import unescape
import re
import getpass
from docopt import docopt

args=docopt(__doc__)
folder=args.get('<folder>')

with open(folder+'/info.plist') as f:
    for line in f:
        if '>bundleid<' in line:
            bundleid=unescape(re.sub('<[^>]+>', '', next(f)).strip())
            break

if args.get('-d'):
    print '/Users/'+getpass.getuser()+'/Library/Application Support/Alfred 2/Workflow Data/'+bundleid+'/'
elif args.get('-c'):
    print '/Users/'+getpass.getuser()+'/Library/Caches/com.runningwithcrayons.Alfred-2/Workflow Data/'+bundleid+'/'
