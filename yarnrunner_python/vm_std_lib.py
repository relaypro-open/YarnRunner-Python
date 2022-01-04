functions = {
    'Add': (2, lambda p: p[0] + p[1]),
    'Minus': (2, lambda p: p[0] - p[1]),
    'UnaryMinus': (1, lambda p: -p[0]),
    'Divide': (2, lambda p: p[0] / p[1]),
    'Multiply': (2, lambda p: p[0] * p[1]),
    'Modulo': (2, lambda p: p[0] % p[1]),
    'EqualTo': (2, lambda p: p[0] == p[1]),
    'NotEqualTo': (2, lambda p: p[0] != p[1]),
    'GreaterThan': (2, lambda p: p[0] > p[1]),
    'GreaterThanOrEqualTo': (2, lambda p: p[0] >= p[1]),
    'LessThan': (2, lambda p: p[0] < p[1]),
    'LessThanOrEqualTo': (2, lambda p: p[0] <= p[1]),
    'And': (2, lambda p: p[0] and p[1]),
    'Or': (2, lambda p: p[0] or p[1]),
    'Xor': (2, lambda p: p[0] ^ p[1]),
    'Not': (1, lambda p: not p[0])
}

typeMethods = {
    'Boolean': ['EqualTo',
                'NotEqualTo',
                'And',
                'Or',
                'Xor',
                'Not'],
    'Number': ['EqualTo',
               'NotEqualTo',
               'Add',
               'Minus',
               'Divide',
               'Multiply',
               'Modulo',
               'UnaryMinus',
               'GreaterThan',
               'GreaterThanOrEqualTo',
               'LessThan',
               'LessThanOrEqualTo'],
    'String': ['EqualTo',
               'NotEqualTo',
               'Add']
}

for type, methods in typeMethods.items():
    for method in methods:
        functions[f'{type}.{method}'] = functions[method]
