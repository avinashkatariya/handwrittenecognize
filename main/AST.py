symbols = ['!', '(', ')', '+', ',', '-', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '=', 'A', 'alpha', 'ascii_124', 'b', 'beta', 'C', 'cos', 'd', 'Delta', 'div', 'e', 'exists', 'f', 'forall', 'forward_slash', 'G', 'gamma', 'geq', 'gt', 'H', 'i', 'in', 'infty', 'int', 'j', 'k', 'l', 'lambda', 'ldots', 'leq', 'lim', 'log', 'lt', 'M', 'mu', 'N', 'neq', 'o', 'p', 'phi', 'pi', 'pm', 'prime', 'q', 'R', 'rightarrow', 'S', 'sigma', 'sin', 'sqrt', 'sum', 'T', 'tan', 'theta', 'times', 'u', 'v', 'w', 'X', 'y', 'z', '[', ']', '{', '}']

class AST():
    binary_ops = ['!','sin','cos','tan','cot','cosec','sec','log','sqrt','log','lim','int']
    secondary_ops=['+','-','times','div','=','neq','geq','leg','lt','gt']
    consts = ['0','1','2','3','4','5','6','7','8','9','e','infty','pi']
    var = ['alpha','beta','gamma','lambda','theta','mu','phi','A','b','c','d','f','G','H','i','j','k','l','m','N','p','q','R','S','T','u','v','x','y','z']
    brackets = ('(',')')


class EqSymbol(object):
    def __init__(self,symbol,point_a,point_b):
        self.symbol = symbol
        self.point_a = point_a
        self.point_b = point_b



