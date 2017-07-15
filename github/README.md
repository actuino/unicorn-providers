# Github provider

A Unicorn Dipslay provider. 
See https://github.com/actuino/unicorn-display

# What it does

Converts data from Github API into a Unicorn frame and sends it to the display server. 

Watches a git repo and display binary count of 
* stars
* watchers
* forks
* issues 
 
On the RGB display. 

In it's current state, only 4 lines are used, so it's ok for small unicorn displays.

This python script is to be called via cron. 

# Exemple display

(TODO)

# Installation

(No Docker image yet, nor config file)

Needs `requests` python lib.

Set DISPLAY_SERVER_HOST and DISPLAY_SERVER_PORT env var. 
The target Unicorn display must have a "github" channel defined in its config.

Edit the `TO_WATCH` constant at the beginning of file, test by calling the script once 
`python github.py` 
then add it as a crontab entry 
`crontab -e` 
add a line: 
`*/5 * * * /usr/bin/python /path/to/github.py`



# TODO

* Config file or watched repo as an environement variable
* Docker image ?
* Dynamic range management to scale for big repos. 