def all(objective, job=None, result=None):
    """ use all providers available. """
    pass


def free(objective, job=None, result=None):
    """ use only fully free accounts. """
    pass


def accounted(objective, job=None, result=None):
    """ prefer a paid account, if there's some of the free tier left. """
    pass


def score(objective, job=None, result=None):
    """ try to reach the score. """
    pass
