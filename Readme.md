# Get Status
Ever wanted to get the status of repos in multiple sub directories? Yeah, me 
too.

## Credit
Mike Pearce is the original author and creator of this project. This is a fork
that I have made with improvements to the project such as upgrading it to Python3
and adding features that I wanted. Original repo can be found [here](https://github.com/MikePearce/Git-Status).

## Installation
Copy the file to /usr/bin

%> cp show_status /usr/bin (or /usr/sbin)

Give it execute permissions

%> chmod +x /usr/bin/show_status

## Usage
Usage: show_status [options]

Show Status is awesome. If you tell it a directory to look in, it'll scan
through all the sub dirs looking for a .git directory. When it finds one it'll
look to see if there are any changes and let you know. It can also push and
pull to/from a remote location (like github.com) (but only if there are no
changes.) Contact cmpickle@gmail.com for any support.

```
Options:
  -h, --help            show this help message and exit
  -d DIRNAME, --dir=DIRNAME
                        The directory to parse sub dirs from
  -v, --verbose         Show the full detail of git status
  -r REMOTE, --remote=REMOTE
                        Push to the master (remotename:branchname)
  -p PULL, --pull=PULL  Pull from the master (remotename:branchname)
```


## Warranties/Guarantees
None, you're on your own. If you'd like some help, mail me on cmpickle@gmail.com
