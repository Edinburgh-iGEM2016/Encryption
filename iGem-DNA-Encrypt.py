
#Encryption program using RSA to encrypt the passcode used as a seed in a random generating function in order to produce keys for encrypting text using the Stream Cipher method
#University of Edinburgh iGEM 2016
#Catalina Rotaru & Freddie Starkey 


import random
import fractions
import gmpy
import sympy
import numpy
from multiprocessing import Pool



sequence = raw_input('Introduce your word: ')
passC = raw_input('Introduce your pass code number: ')
wordNumber = 2  #You can modify the words number, depending on how many words you want to encode or the number of sentences

passCode = int(passC)


def encryptPassCode(passCode):
    #Encrypt the passcode using RSA
    ((publicOne, coprime), privateKey) = rsa(passCode)
    encrypted = pow(passCode, coprime, publicOne)
    return (encrypted, privateKey, publicOne)


def rsa(passCode):
    #Function for RSA, generating 2 random large primes
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
    return (publicKey, privateKey)
    

def extractKey(passCode, wordNumber):
    #Function for introducing all the keys into an array
    key = generateFromKey(passCode, wordNumber)
    array_key = []
    for i in key:
        sizeKey = str(convertKey(i))
        if len(sizeKey) == 5:
            array_key.append(sizeKey)
        elif len(sizeKey) < 5:
            array_key.append(wordPad(sizeKey))
    return array_key

def encrypt(sequence):
    #Function for encrypting the sequence, using the function below
    ekey_array = extractKey(passCode, wordNumber)
    #this line needs to be adjusted in order to use how many keys for how many sentences
    ekey = ekey_array.pop(0)
    key_base4 = transform_key(ekey)
    list = change(sequence)
    zip_all = zip(list, key_base4)
    crypto_numbers = apply_xor(zip_all)
    crypto_final = ''.join(translate_crypto(crypto_numbers))
    return crypto_final

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
    #Getting the keys in order to decrypt the message
    return pow(encrypted, privateKey, publicOne)



def generateFromKey(passCode, wordNumber):
    #Random generating function and introducing the passcode as a seed
    random.seed(passCode)
    mapping = []
    for i in xrange(wordNumber):
        mapping.append(random.randint(0, 1023))
    return mapping



# def convertKey(key)
#convert base 10 to base 4 !!!
def convertKey(key):
    return int(numpy.base_repr(int(str(key), base=10), 4))

def wordPad(unlengthB4):
    # increases the size of a dna code up to 5 bases
    #returns a string, you need to convert it into an int !!!!
    return ('0' * (5 - len(str(unlengthB4)))) + str(unlengthB4)

def transform_key(key):
    mapped = []
    for i in key:
        int_key = int(i)
        mapped.append(int_key)
    return mapped


####Word conversion####


def change(sequence):
    #Correspondence numbers with DNA bases
    xcode = []
    for letter in sequence:
            if letter =='A':
                xcode.append(0)
            elif letter == 'T':
                xcode.append(1)
            elif letter == 'G':
                xcode.append(2)
            elif letter == 'C':
                xcode.append(3)
    return xcode



def xor(num1, num2, offset):
    #Function for applying XOR
    offset = offset or 0
    return (4 - (offset + num1 + num2) % 4) % 4




def apply_xor(zip_all):
    #Applying XOR
    crypto = []
    for (l,k) in zip_all:
        crypto.append(xor(l,k,0))
    return crypto



def translate_crypto(crypto_numbers):
    xco = []
    for c in crypto_numbers:
        if c == 0:
            xco.append('A')
        elif c == 1:
            xco.append('T')
        elif c == 2:
            xco.append('G')
        elif c == 3:
            xco.append('C')
    return xco

(k, l , m) = encryptPassCode(passCode)
p = tuple()
p= (k, l ,m) 
encryptK = str(p[0])
privateK = str(p[1])
publicK = str(p[2])
print ('Encrypted key: ' + encryptK)
print ('Private key: ' + privateK)
print ('Public key: ' + publicK)
print ('Your cipher text is: ' + encrypt(sequence))

#Reference:
#http://cwestblog.com/2013/08/20/javascript-xor-in-any-base/  - Applying XOR in base 4 