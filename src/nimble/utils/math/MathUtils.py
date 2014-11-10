# MathUtils.py
# (C)2014
# Scott Ernst

from __future__ import print_function, absolute_import, unicode_literals, division

import math

#___________________________________________________________________________________________________ MathUtils
class MathUtils(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ crossProduct
    @classmethod
    def crossProduct(cls, a, b):
        """ Computes the cross product of two 3D lists and returns a list containing the resulting
            vector """
        return [
            a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0] ]

#___________________________________________________________________________________________________ equivalent
    @classmethod
    def equivalent(cls, a, b, tol =0.001):
        """ Determines if the two values are the same, i.e. differ byt less than the specified
            tolerance value """
        return abs(a - b) < tol

#___________________________________________________________________________________________________ dotProduct
    @classmethod
    def dotProduct(cls, a, b):
        """ Computes the dot product of the two 3D lists and returns the scalar result """
        return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

#___________________________________________________________________________________________________ normalize
    @classmethod
    def normalize(cls, v):
        """ Normalizes the specified 3D list and returns a new normalized 3D list as a result """

        mag = math.sqrt(cls.dotProduct(v, v))
        out = []
        for item in v:
            out.append(item/mag)
        return out
