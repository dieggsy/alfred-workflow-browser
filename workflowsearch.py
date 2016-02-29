'''workflowsearch.py (path) [options]

Usage:
    workflowsearch.py <query> [-c|-b|-r|-a|-w] [<keyword>]

Options:
    -c    Filter by category
    -b    Filter by bundleid
    -r    Filter by readme
    -a    Filter by createdby
    -w    Show all
'''
from xml.sax.saxutils import unescape
from workflow import Workflow
from docopt import docopt
import os
import sys
import re
import getpass


def wfFilter(filename):
    args=docopt(__doc__)
    
    if args.get('-r'):
        field='>readme<'
    elif args.get('-a'):
        field='>createdby<'
    elif args.get('-b'):
        field='>bundleid<'
    elif args.get('-c'):
        field='>category<'
    elif args.get('-w'):
        field=''
       
    if args.get('<keyword>'):
        keyword=args.get('<keyword>')
    else:
        keyword=''
        
    with open(filename) as f:
        namefound,show=False,False
        for line in f:
            if '>name<' in line and not namefound:
                name=unescape(re.sub('<[^>]+>', '', next(f)).strip())
                namefound=True    
            if field in line and not show:
                if keyword in next(f):
                    show=True
    return name,show

def workflow_subdirectories():
    a_dir=os.path.dirname(os.path.dirname(os.path.abspath('info.plist')))
    my_workflows=[]
    for folder in os.listdir(a_dir):
        folderpath=os.path.join(a_dir,folder)
        if os.path.isdir(folderpath):
            name,show=wfFilter(os.path.join(a_dir,folder,'info.plist'))
            if show:
                my_workflows.append((name,folderpath))
    return my_workflows
    

def main(wf):
    args=docopt(__doc__)
    query=args.get('<query>')
    quer=re.compile('.*'+query+'.*',re.IGNORECASE)
    my_workflows=workflow_subdirectories()
    my_workflows.sort(key=lambda tup: tup[0].lower())
    for i in my_workflows:
        if quer.match(i[0]):
            wf.add_item(i[0],
                        'Browse workflow directory',
                        arg=i[1],
                        valid=True,
        
                        icon=i[1]+'/icon.png')
    wf.send_feedback()
    
if __name__==u"__main__":
    wf=Workflow()
    sys.exit(wf.run(main))
