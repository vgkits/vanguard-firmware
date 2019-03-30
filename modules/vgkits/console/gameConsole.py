def prompt(msg):
    return input(msg)


def show(line):
    print(line)


def hostGame(game, show=show, prompt=prompt):
    game(show, prompt)
