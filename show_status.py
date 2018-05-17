#!/usr/bin/python

# @desc     Tired of having to go into each sub dir to find out whether or
#           not you did a git commit? Tire no more, just use this!
#           This version is a fork off of Mike Pearce's version. I have made 
#           updates such as migrating the project to Python3 and some feature
#           enhancements that I wanted.
#
# @author   Cameron Pickle <cmpickle@gmail.com>
# @since    5/17/2018

# @desc     Tired of having to go into each sub dir to find out whether or
#           not you did a git commit? Tire no more, just use this!
#
# @author   Mike Pearce <mike@mikepearce.net>
# @since    18/05/2010

# Grab some libraries
import sys
import os
import glob
import subprocess
from argparse import ArgumentParser

# Setup some stuff
dirname = './'
gitted = False
mini = True


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    CYAN = '\033[96m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


parser = ArgumentParser(description="\
Show Status is awesome. If you tell it a directory to look in, it'll scan \
through all the sub dirs looking for a .git directory. When it finds one \
it'll look to see if there are any changes and let you know. \
It can also push and pull to/from a remote location (like github.com) \
(but only if there are no changes.) \
Contact cmpickle@gmail.com for any support.")
parser.add_argument("-d", "--dir",
                  dest="dirname",
                  action="store",
                  help="The directory to parse sub dirs from",
                  default=os.path.abspath("./")+"/"
                  )

parser.add_argument("-v", "--verbose",
                  action="store_true",
                  dest="verbose",
                  default=False,
                  help="Show the full detail of git status"
                  )

parser.add_argument("-r", "--remote",
                  action="store",
                  dest="remote",
                  default="",
                  help="Set the remote name (remotename:branchname)"
                  )

parser.add_argument("--push",
                  action="store_true",
                  dest="push",
                  default=False,
                  help="Do a 'git push' if you've set a remote with -r it will push to there"
                  )

parser.add_argument("-p", "--pull",
                  action="store_true",
                  dest="pull",
                  default=False,
                  help="Do a 'git pull' if you've set a remote with -r it will pull from there"
                  )

# Now, parse the args
args = parser.parse_args()

# -------------------


def show_error(error="Undefined Error!"):
    # -------------------
    """Writes an error to stderr"""
    sys.stderr.write(error)
    sys.exit(1)


# -------------------
# Now, onto the main event
# -------------------
if __name__ == "__main__":
    os.system('')
    os.environ['LANGUAGE'] = 'en_US:en'
    os.environ['LANG'] = 'en_US.UTF-8'

    sys.stdout.write('Scanning sub directories of %s\n' % args.dirname)

    # See whats here
    for infile in glob.glob(os.path.join(args.dirname, '*')):

        # is there a .git file
        if os.path.exists(os.path.join(infile, ".git")):

            # Yay, we found one!
            gitted = True

            remote = False

            # OK, contains a .git file. Let's descend into it
            # and ask git for a status
            out = subprocess.check_output('cd ' + infile + ' && git status', shell=True).decode("utf-8")
            
            remoteBranch = subprocess.check_output('cd ' + infile + ' && git remote', shell=True).decode("utf-8")
            if (remoteBranch != ''):
                remote = True

            # Mini?
            if False == args.verbose:

                j = out.find('On branch')
                k = out.find('\n')
                branch = str(out)[j+10:k]
                branchColor = bcolors.CYAN

                if branch == 'master':
                    branchColor = bcolors.CYAN

                branch = bcolors.WARNING + "[" + branchColor + branch
                if(remote):
                    branch += " ≡"
                branch += bcolors.WARNING + "]" + bcolors.ENDC

                if -1 != out.find('nothing'):
                    result = bcolors.OKGREEN + "No Changes" + bcolors.ENDC

                    # Pull from the remote
                    if False != args.pull:
                        push = str(subprocess.check_output(
                            'cd ' + infile +
                            '; git pull ' +
                            ' '.join(args.remote.split(":"))
                        ))
                        result = result + " (Pulled) \n" + push

                    # Push to the remote
                    if False != args.push:
                        push = str(subprocess.check_output(
                            'cd ' + infile +
                            '; git push ' +
                            ' '.join(args.remote.split(":"))
                        ))
                        result = result + " (Pushed) \n" + push

                else:
                    result = bcolors.FAIL + "Changes" + bcolors.ENDC

                # Write to screen
                sys.stdout.write(bcolors.OKBLUE + infile.ljust(35) +
                                 bcolors.ENDC + branch + " : " + result + "\n")

            else:
                # Print some repo details
                sys.stdout.write("\n---------------- " +
                                 infile + " -----------------\n")
                sys.stdout.write(out)
                sys.stdout.write("\n---------------- " +
                                 infile + " -----------------\n")

            # Come out of the dir and into the next
            subprocess.check_output('cd ../', shell=True)

    if False == gitted:
        show_error("Error: None of those sub directories had a .git file.\n")
