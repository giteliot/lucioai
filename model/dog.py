import random

moves = {
    "STOP",
    "STAY",
    "UP",
    "LEFT",
    "RIGHT",
    "DOWN",
    "STAND",
    "SIT"
}

itom = {i: m for i, m in enumerate(moves)}
mtoi = {m: i for i, m in enumerate(moves)}


def get_random_action():
    return itom[random.randint(0, len(moves)-1)]


def get_random_seq():
    r = get_random_action()
    print(r)
    if r == "STOP":
        return [r]
    return [r]+get_random_seq()
