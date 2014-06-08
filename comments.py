"""New idea: Connect subreddits if a user comments in them"""

import praw
from dbmodel import DBModel
from sys import stdout

def main():
    model = DBModel.get()
    print "[ ] Connecting.."
    r = praw.Reddit(user_agent="/u/benediktkr/")
    print "[ ] Logging in.."
    r.login(username="bkbot", password="ostur.kaka.123!")
    print "[ ] Starting.."
    try:
        while True:
            # praw follows the guidelines on ratelimits
            print "  [ ] Fetching comments.."
            comments = list(r.get_comments("all", limit=None))
            print "    [+] Fetched: {0} comments.".format(len(comments))
            print "    [ ] Processing"
            for comment in comments:
                username = str(comment.author)
                subreddit = "/r/" + str(comment.subreddit).lower() + "/"
                model.save_comment(username, subreddit)
            print "    [+] Done"
    except KeyboardInterrupt:
        model.close()
        print "\n[!]Exiting"

if __name__ == "__main__":
    main()
