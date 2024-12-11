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
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        if self.discriminant == 0:
            raise ValueError('Discriminant cannot be 0')
    
    def __str__(self):
        return f'y^2 = x^3 + {self.a}x + {self.b} (mod {self.p})'
    
    @property
    def discriminant(self):
        return 4 * pow(self.a, 3) + 27 * pow(self.b, 2)

    def testPoint(self, x, y):
        return pow(y, 2, self.p) == (pow(x, 3, self.p) + self.a * x + self.b) % self.p
    
    def findAllPoints(self):
        y_squares = {}
        for y in range(self.p):
            y_squares.setdefault(pow(y, 2, self.p), []).append(y)
        x_outputs = [(pow(x, 3, self.p) + self.a * x + self.b) % self.p for x in range(self.p)]
        points = ['O']
        for x, x_out in enumerate(x_outputs):
            [points.append((x, i)) for i in y_squares.get(x_out, [])]
        return points
    
    def invert(self, P):
        if P == "O": return "O"
        return (P[0], self.p - P[1])

    def add(self, P, Q):
        # case 1: point at infinity
        if P == "O": return Q
        if Q == "O": return P
        # case 2: points are mutual inverses
        if P == self.invert(Q):
            return "O"
        # case 3: distinct points
        Px, Py = P
        Qx, Qy = Q
        if P != Q:
            s = ((Qy - Py) * pow(Qx - Px, self.p - 2)) % self.p
        # case 4: p == q
        else:
            s = ((3 * pow(Px, 2) + self.a) * pow(2 * Py, self.p - 2)) % self.p

        Rx = (pow(s, 2) - Px - Qx) % self.p
        Ry = (s * (Px - Rx) - Py) % self.p
        return (Rx, Ry)
    
c = EllipticCurve(3, 4, 7)
print("1. Given the elliptic curve", c)
print("  a. Its discriminant is", c.discriminant)
print("  b. (5, 2) is ", "" if c.testPoint(5, 2) else "not ", "on the curve", sep="")
print("  c. (4, 3) is ", "" if c.testPoint(4, 3) else "not ", "on the curve", sep="")
print("  d. The points on the curve are", c.findAllPoints())
print()
c = EllipticCurve(3, 5, 47)
p = (4, 9)
q = (11, 10)
print("2. P =", p, "and Q =", q, " are both points on the curve", c)
print("  a. -P =", c.invert(p))
print("  b. P + Q =", c.add(p, q))
print("  c. 2P =", c.add(p, p))
