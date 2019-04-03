posts = list()

def createChatGame(print):
    name = yield "What is your name? "
    print("Welcome to the chatroom, " + name)
    while True:
        for name, message in posts:
            print(name, message)
        print("")
        response = yield "Type your message or press enter to refresh"
        if response is not "":
            post = (name, response)
            posts.append(post)
            if len(posts) > 10: # make posts ephemeral
                posts[:] = posts[1:]
