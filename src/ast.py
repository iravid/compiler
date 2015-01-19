__author__ = 'iravid'

class Node(object):
    def __init__(self):
        pass

class NExpression(Node):
    pass

class NAddExpression(NExpression):
    pass

class NMultExpression(NExpression):
    pass

class NIdentifier(NExpression):
    pass

class NInteger(NExpression):
    pass

class NFloat(NExpression):
    pass

class NStatement(Node):
    pass