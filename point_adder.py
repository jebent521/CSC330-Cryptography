#point_adder.py, Dr. John Coleman

#Adds two points on an elliptic curve.
#The point at infinity is represented by
#the string 'O'

#The following function adds two points
#It does *not* check if the assumptions
#are valid (e.g. p prime, P,Q on the curve)
#Note that b isn't needed in the computation

def addPoints(P,Q,a,p):
    if P == 'O':
        return Q
    elif Q == 'O':
        return P
    else:
        x_P, y_P = P
        x_Q, y_Q = Q
        if x_P == x_Q:
            if y_Q != y_P:
                #must be P = -Q, so
                return 'O'
            else:
                #must be P = Q, so
                s = (3*pow(x_P,2,p) + a) % p #numerator
                s = s * pow(2*y_P,p-2,p) % p #times inverse of denom
        else:
            #compute s in distinct points case:
            s = (y_Q - y_P) % p 
            s = s * pow(x_Q - x_P,p-2,p) % p
        x_R = (pow(s,2,p) - x_P - x_Q) % p
        y_R = (-y_P + s*(x_P - x_R) ) % p
        return (x_R,y_R)

def doublePoint(P,a,p):
    return addPoints(P,P,a,p)

def multiplyPoint(k,P,a,p):
    D = P #successive doubles
    S = 'O' #will be returned as final answer

    while k > 1:
        k,r = divmod(k,2)
        if r == 1: S = addPoints(S,D,a,p)
        D = doublePoint(D,a,p)
    S = addPoints(S,D,a,p)
    return S

#It helps to have a curve for examples:

def findCurve(a,b,p):
    #finds all points (x,y) in Z_p x Z_P
    #with y^3 = x^2+ax+b (mod p)
    #uses shortcut under assumption
    #that p is an odd prime

    #first make a dictionary of square roots

    squareRoots = {} #empty dictionary to hold square roots
    for y in range((p+1)//2):
        squareRoots[pow(y,2,p)] = y
               
    points = []
    for x in range(p):
        RHS = (pow(x,3,p) + a*x % p + b) % p
        if RHS in squareRoots:
            y = squareRoots[RHS]
            if y == 0:
                points.append((x,y))
            else:
                points.extend([(x,y),(x,p-y)])
    return points

#Might a well have something to test D:

def D(a,b,p): return (4*pow(a,3,p) + 27*pow(b,2,p)) % p


        
        


    
