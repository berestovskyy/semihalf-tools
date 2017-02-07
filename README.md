# Tools
A set of tiny Semihalf tools and scripts.


## Installation
bin/ - put the binary files to /usr/local/bin
etc/ - put the configuration files to /usr/local/etc

**Hint:** You might whant to add links instead, so once you update the repo,
the binaries will be updated as well and vice versa.


## backup
Incremental backup tool stores local directories specified in config file
to the specified remote host.
Example usage:
    backup l5.conf


## backup-host
Remote host backup tool fetches remote host files to the current directory.
Example usage:
    backup-host l1 l2 l3


## backup-periodic
Periodic incremental backup tool is to be installed in /etc/cron.hourly
to periodically store local directories to the specified remote host.


## passwordless
To setup a passwordless ssh connection with the specified host(s).
Example usage:
    passwordless a@l5
