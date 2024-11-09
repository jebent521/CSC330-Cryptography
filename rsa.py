p = 21023
q = 32869
n = 691004987
phi_n = (p-1)*(q-1)
e = 5
d = pow(e, -1, phi_n)
c = 168340685

def encrypt(m):
    return pow(m, e, n)

def decrypt(c):
    return pow(c, d, n)

def meetInTheMiddle(c, r):
    # precompute table
    m2s = {encrypt(m2): m2 for m2 in range(1,r)}

    # attack
    for m1 in range(1,r):
        c1 = encrypt(m1)
        c1_inverse = pow(c1, -1, n)
        c2 = (c1_inverse * c) % n
        m2 = m2s.get(c2)
        if m2 is not None:
            return (m1, m2, m1 * m2)

m = meetInTheMiddle(c, 2000)[2]
print(m)
print(decrypt(c))
print(d)
    