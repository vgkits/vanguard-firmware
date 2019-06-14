posts = list()

def createSequence(print):

    # store this session user's name
    myname = yield "What is your name? "
    print("Welcome to the chatroom, " + myname)

    while True:
        # show post history
        for name, message in posts:
            print("<b><i>", name, "</i></b>", message)

        # ask for next post
        print("")
        mymessage = yield "Type your message or press enter to refresh"

        # handle the post
        if mymessage is not "":
            mypost = (myname, mymessage)
            posts.append(mypost)

        posts[:] = posts[-10:] # keep only the last 10 posts
