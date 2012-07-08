#!/usr/bin/python

# Simple python script to clean local git branches
# Lists local branches, check from Jira if they are 'closed'
# and generate remove branch command

import SOAPpy, os,argparse

class GitBranchCleaner():
    def __init__(self):
        try:
            # parse arguments
            args = self.parse_arguments()
            self.verbose = args.verbose

            # try to login SOAP
            self.login(args.url, args.username, args.password)

            # branch list can be read from arguments
            if args.branches:
                branches = args.branches.split(",")
            else:
                # if no branches args set
                # try to get it using system call
                branches = self.get_branches()

            # closed status can be set from arguments
            if args.closed_status:
                closed_status = args.closed_status
            else:
                closed_status = self.get_closed_status()

            closed_issues = []

            # get local branches
            for i in branches:
                # if issue is closed add it to closed issue list
                if self.get_issue_status(i) == closed_status:
                    closed_issues.append(i)

            # generate remove string
            if len(closed_issues) > 0:
                cmd_string = "Found branches that can be removed. Try :\ngit branch -D "
                for i in closed_issues:
                    cmd_string += i + " "
                print cmd_string
            else:
                print " >>> No closed issue by now <<< "

        except Exception, error:
            print "Something went wrong : ", error

    def get_closed_status(self):
        statuses = self.soap.getStatuses(self.auth)
        for i in statuses:
            if i.name == "Closed":
                return i.id

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Settings')
        parser.add_argument('-u', '--username', dest='username', required=True, help='Jira username')
        parser.add_argument('-p', '--password', dest='password', required=True, help='Jira password')
        parser.add_argument('--url', metavar='URL', dest='url', help='Jira server url', default='https://jira.atlassian.com')
        parser.add_argument('--closed_status', dest='closed_status', help='Jira status code for \'Closed\' issues. If not set, it will be looked up by SOAP query')
        parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False, help='Verbose exceptions')
        parser.add_argument('--branchese', dest='branches', help='Comma separated branch list. If not set, tried to get it using system call')
        return parser.parse_args()

    def get_branches(self) :
        branches = []
        branches_tmp = os.popen('git branch').read().split('\n')
        for i in branches_tmp:
            branch_name = i.replace("*","").strip()
            if len(branch_name) > 0 and branch_name != "master":
                branches.append(branch_name)
        return branches

    def get_issue_status(self, code):
        try:
            issue = self.soap.getIssue(self.auth, code)
            return issue.status
        except Exception, error:
            return None

    def login(self, url, username, password):
        try:
            self.soap = SOAPpy.WSDL.Proxy(url + '/rpc/soap/jirasoapservice-v2?wsdl')
            self.auth = self.soap.login(username, password)
        except Exception, error:
            if self.verbose == True:
                raise Exception(error)
            else:
                raise Exception("Login failed!")

if __name__ == "__main__":
    GitBranchCleaner()
