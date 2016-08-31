import random
import fractions
import gmpy
import sympy
from multiprocessing import Pool

def rsa(passCode):
    pool = Pool(processes=2)
    primes = pool.map(primeGenerator, [3072, 3072])
    primeOne = primes[0]
    primeTwo = primes[1]
    pool.close()
    pool.join()
    print "first prime chosen: " + str(primeOne)
    print "second prime chosen: " + str(primeTwo)
    publicOne = primeOne * primeTwo
    print "first part of the public key is: " + str(publicOne)
    totient = eulerPhi(primeOne, primeTwo)
    print "the totient is: " + str(totient)
    coprime = getCoprime(totient, passCode)
    print "the coprime selected is: " + str(coprime)
    publicKey = (publicOne, coprime)
    print "public key: " + str(publicKey)
    privateKey = modularMulInv(coprime, totient)
    encrypted = pow(passCode, coprime, publicOne)
    return (encrypted, privateKey, publicOne)

def primeGenerator(size):
    while True:
        potentialPrime = random.SystemRandom().getrandbits(size)
        print "number being considered is : " + str(potentialPrime)
        if sympy.isprime(potentialPrime):
            break
    return potentialPrime

def eulerPhi(primeOne, primeTwo):
    return (primeOne - 1) * (primeTwo -1)

def getCoprime(totient, passCode):
    coprime = random.SystemRandom().getrandbits(25)
    while True:
        print "the potential coprime under consideration is: " + str(coprime)
        if fractions.gcd(totient, coprime) == 1L:
            return coprime
            break
        coprime = coprime + 1

def modularExp(passCode, coprime):
    if coprime < 0:
      passCode = 1 / passCode
      coprime = -coprime
    if coprime == 0:
        return 1
    y = 1
    while coprime > 1:
      if coprime % 2 == 0:
        passCode = passCode * passCode
        coprime = coprime / 2
      else:
        y = passCode * y
        passCode = passCode * passCode
        coprime = (coprime - 1)/2
    return passCode * y

def modularMulInv(coprime, totient):
    return int(gmpy.invert(coprime, totient))

def rsaDecrypt(encrypted, privateKey, publicOne):
    return pow(encrypted, privateKey, publicOne)

def generateFromKey(passCode, unitNumber):
    random.seed(passCode)
    mapping = []
    for i in xrange(unitNumber):
        mapping.append(random.randint(0, 1023))
    return mapping


