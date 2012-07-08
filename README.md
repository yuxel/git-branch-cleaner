git-branch-cleaner
==================

Simple Python script to clean local git branches by Jira status.
If you have lots of local git branches and you remove them when they are closed on Jira, this can be handy.

usage
=====
<pre>
usage: git-branch-cleaner.py [-h] -u USERNAME -p PASSWORD [--url URL]
                             [--closed_status CLOSED_STATUS] [-v]
                             [--branchese BRANCHES]

Settings

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Jira username
  -p PASSWORD, --password PASSWORD
                        Jira password
  --url URL             Jira server url
  --closed_status CLOSED_STATUS
                        Jira status code for 'Closed' issues. If not set, it will be looked up by SOAP query
  -v, --verbose         Verbose exceptions
  --branchese BRANCHES  Comma separated branch list. If not set, tried to get it using system call
</pre>

example output
==============
<pre>$ python git-branch-cleaner.py -u osman.yuksel -pyoureadmypassword --url https://jira.rocket-internet.de/
Found branches that can be removed. Try :
git branch -D TURPAR-15 </pre>

