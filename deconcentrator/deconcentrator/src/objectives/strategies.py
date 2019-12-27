def all(objective, *args, **kwArgs):
    """ use all providers available. """
    pass


def free(objective, *args, **kwArgs):
    """ use only fully free accounts. """
    pass


def accounted(objective, *args, **kwArgs):
    """ prefer a paid account, if there's some of the free tier left. """
    pass


def score(objective, *args, **kwArgs):
    """ try to reach the score. """
    pass