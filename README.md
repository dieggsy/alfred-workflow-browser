# WorkflowFileBrowser
An Alfred workflow to browse workflow files
## Usage:
### Workflow

    wf       -access filtered workflows (see script usage)
    awf      -access all workflows
    
    enter    -cd into workflow directory in Terminal
    ⌘-enter  -Browse workflow directory in Alfred
    ⌥-enter  -Browse data directory in Alfred
    ⌃-enter  -Browse cache directory in Alfred

Workflows can be searched by name, with regex search supported.

### Script
Usage:

    workflowsearch.py <query> [-c|-b|-r|-a|-w] [<keyword>]
    
Options:

    -c    Filter by category
    -b    Filter by bundleid
    -r    Filter by readme (in progress, only currently works with line on top of readme)
    -a    Filter by createdby
    -w    Show all
