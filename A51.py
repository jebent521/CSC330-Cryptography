#A51.py
#partially implements A5/1

class LFSR:
    def __init__(self,powers):
        self.poly = powers
        self.n = max(powers)
        self.taps = [self.n-p for p in powers]
        self.state = [0]*self.n

    def clock(self):
        feedback = sum(self.state[i] for i in self.taps) % 2
        self.state.append(feedback)
        output = self.state[0]
        self.state = self.state[1:]
        return output

#Utility functions

def int2bits(m,n):
    return [int(i) for i in bin(m)[2:].zfill(n)]

def bits2int(bits):
    return int(''.join(str(i) for i in bits), base = 2)

#Functions to encrypt/decrypt text using a list
#of keystream bits
#assumes that the list of bits is long enough

def encrypt(plaintext,bits):
    ciphertext = [] #will just be a list of numbers
    for i,p in enumerate(plaintext):
        k = bits[8*i:8*(i+1)] #slices off next 8 bits
        k = bits2int(k)
        ciphertext.append(ord(p)^k)
    return ciphertext

def decrypt(ciphertext,bits):
    plaintext = []
    for i,c in enumerate(ciphertext):
        k = bits[8*i:8*(i+1)]
        k = bits2int(k)
        plaintext.append(chr(c^k))
    return ''.join(plaintext)

class A51:
    def __init__(self):
        self.r1 = LFSR([14,17,18,19])
        self.r2 = LFSR([21,22])
        self.r3 = LFSR([8,21,22,23])
        #clock bits = [10,11,12] , 0-based from the left
        #just use these values
        #self.r1.state[10], for example, gives the first-register value

    def set_state(self,a,b,c):
        self.r1.state = int2bits(a,19)
        self.r2.state = int2bits(b,22)
        self.r3.state = int2bits(c,23)
                 
    def display(self):
        s = ['| | |     |         *                ',
             '| |                   *                    ',
             '| | |                   *     |              ']
        states = [self.r1.state,self.r2.state,self.r3.state]
             
        for i in range(3):
            print(' '.join(str(b) for b in states[i]))
            print(s[i])

    def clock(self):
        majorityOnes = sum([self.r1.state[10], self.r2.state[11], self.r3.state[12]]) >= 2
        if majorityOnes == self.r1.state[10]: self.r1.clock()
        if majorityOnes == self.r2.state[11]: self.r2.clock()
        if majorityOnes == self.r3.state[12]: self.r3.clock()
        return sum([self.r1.state[0], self.r2.state[0], self.r3.state[0]]) % 2
        

#test code:

cipher = A51()
cipher.set_state(121419,2929401,573023)
test_bits = [cipher.clock() for i in range(100)]
target = [0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0,
          1, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1,
          1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1,
          1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1,
          1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1]

if test_bits == target:
    print("Test passed!")
else:
    print("Need to debug")
