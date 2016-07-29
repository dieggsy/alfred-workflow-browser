'''workflowsearch.py (path) [options]

Usage:
    workflowsearch.py <query> (-c|-b|-r|-a) <keyword> [--pardir=<dirpath>]
    workflowsearch.py <query> -w [--pardir=<dirpath>]

Options:
    -c  Filter by category
    -b  Filter by bundleid
    -r  Filter by readme
    -a  Filter by createdby
    -w  Show all

    --pardir=<dirpath>   Workflow directory (optional)
'''
from xml.sax.saxutils import unescape
from workflow import Workflow3
from docopt import docopt
import os
import sys
import re
import plistlib

def wfFilter(filename):
    args=docopt(__doc__)
    plist = plistlib.readPlist(filename)
    name = plist['name']
    disabled = plist['disabled']

    if args.get('-r'):
        field='readme'   #'>readme<'
    elif args.get('-a'):
        field='createdby' #'>createdby<'
    elif args.get('-b'):
        field='bundleid' #'>bundleid<'
    elif args.get('-c'):
        field='category' #'>category<'

    if disabled:
        return name,False
    elif (not args.get('<keyword>')
          and args.get('-w')):
        return name,True
    else:
        keyword=args.get('<keyword>')
        if keyword in plist[field]:
            return name,True
        else:
            return name,False

def workflow_subdirectories():
    args=docopt(__doc__)
    if not args.get('--pardir'):
        a_dir=os.path.dirname(os.path.dirname(os.path.abspath('info.plist')))
    else:
        a_dir = args.get('--pardir')
    my_workflows=[]
    for folder in os.listdir(a_dir):
        folderpath=os.path.join(a_dir,folder)
        plistfile = os.path.join(a_dir,folder,'info.plist')
        if os.path.isfile(plistfile):
            name,show=wfFilter(plistfile)
            if show:
                my_workflows.append((name,folderpath))
    return my_workflows


def main(wf):
    args=docopt(__doc__)
    query=args.get('<query>')
    quer=re.compile(query,re.IGNORECASE)
    my_workflows=workflow_subdirectories()
    my_workflows.sort(key=lambda tup: tup[0].lower())

    for i in my_workflows:
        if quer.search(i[0]):
            wf.add_item(i[0],
                        'Go to workflow directory in Terminal',
                        arg=i[1],
                        valid=True,
                        icon=i[1]+'/icon.png')

    wf.send_feedback()

if __name__==u"__main__":
    wf=Workflow3()
    sys.exit(wf.run(main))
