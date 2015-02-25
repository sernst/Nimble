from __future__ import print_function, absolute_import, unicode_literals, division

import functools

def f(x, y):
    return '%s*%s = %s' % (x, y, x*y)

# Compose function and freeze x=3
g = functools.partial(f, 3)

def h(y):
    x = 3
    return f(x, y)

print('f:', f(3, 2))
print('g:', g(2))
print('h:', h(2))

