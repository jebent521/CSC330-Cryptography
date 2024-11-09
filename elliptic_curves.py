"""
Jonah Ebent, 11/11/24, HW 16, elliptic_curves.py

1. Given the elliptic curve y^2 = x^3 +3x + 4 (mod 7)
    a. What is its discriminant?
    b. Is (5,2) a point on the curve?
    c. What about (4,3)?
    d. 2 points extra credit: find all points on this curve
2. P = (4,9) and Q = (11,10) are both points on the curve y^2 = x^3 +3x + 5 (mod 47)
    a. What is -P?
    b. What is P+Q?
    c. What is 2P?
3. Extra credit: write a Python program to do your homework for you

"""
class EllipticCurve:
    def __init__(self, a, b, p=None):
        self.a = a
        self.b = b
        self.p = p
        if self.discriminant == 0:
            raise ValueError('Discriminant cannot be 0')
    
    @property
    def discriminant(self):
        return 4 * pow(self.a, 3) + 27 * pow(self.b, 2)