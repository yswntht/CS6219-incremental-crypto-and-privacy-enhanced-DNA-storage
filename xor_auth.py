'''
this file is for complete xor based Incremental authentication implmenation from section 3.2 of 
Incremental Cryptography and Application to Virus Protection from Proceedings of the 27th ACM Symposium on the Theory of Computing, May 1995

I breifly describle the algorithm and strcture of the code. for proofs and more details take a look at above reference.
Wherever possible I used avalibale opensoure or python packages (E.g. Data Encryption Standard (DES) or MD5 hashing) and
cited appropirates links for the code. 

Algorithm is divided into two phases:
phase1: authentication on original document
phase2: for every new update on orignal document, authentication is made only update and is independent on the size of 
		orginal document.
Expected result: authentication-tag appended next to the update when it is stored.

'''

import sys
from os.path import dirname
sys.path.append(dirname("/Users/yash/Documents/dna_project/project"))

from pydes import des, desprp
from base64 import b64encode

import random
random.seed(3)

'''
phase1:
i) randomise
ii) chain and hash
iii) final hash = tag
'''

orgStrings = []
randorgStrings = []
insertStrings = []
randomInsertStrings = []

def string_to_bit_array(text):#Convert a string into a list of bits
    array = list()
    for char in text:
        binval = binvalue(char, 8)#Get the char value on one byte
        array.extend([int(x) for x in list(binval)]) #Add the bits to the final list
    return array


def bit_array_to_string(array): #Recreate the string from the bit array
    res = ''.join([chr(int(y,2)) for y in [''.join([str(x) for x in _bytes]) for _bytes in  nsplit(array,8)]])   
    return res

def binvalue(val, bitsize): #Return the binary value as a string of the given size 
    binval = bin(val)[2:] if isinstance(val, int) else bin(ord(val))[2:]
    if len(binval) > bitsize:
        raise "binary value larger than the expected size"
    while len(binval) < bitsize:
        binval = "0"+binval #Add as many 0 as needed to get the wanted size
    return binval


def nsplit(s, n):#Split a list into sublists of size "n"
    return [s[k:k+n] for k in range(0, len(s), n)]


def utf8_lead_byte(b):
    '''A UTF-8 intermediate byte starts with the bits 10xxxxxx.'''
    return (b & 0xC0) != 0x80

def utf8_byte_truncate(text, max_bytes):
    '''If text[max_bytes] is not a lead byte, back up until a lead byte is
    found and truncate before that character.'''
    utf8 = text.encode('utf8')
    if len(utf8) <= max_bytes:
        return utf8
    i = max_bytes
    while i > 0 and not utf8_lead_byte(utf8[i]):
        i -= 1
    return utf8[:i]


#phase1.i
def randomiseFunc(orgStrings):
	for i in orgStrings[:-1]:
		two_i  = i + i
		pos = random.randint(1, 8)
		number = random.randint(1, 8)
		randorgStrings.append(i + two_i[pos:number+1])
		#print(str(i), str(i + two_i[pos:number+1]))

#phase1.ii
def chainAndHash(randorgStrings):
	hashval = ""
	newval = ""
	for i in range (0,len(randorgStrings)-1):
		r = d.encrypt(utf8_byte_truncate(randorgStrings[i], 8).decode("utf-8"),utf8_byte_truncate(randorgStrings[i+1], 8).decode("utf-8"),padding=True)
		if (i == 0):
			hashval = string_to_bit_array(r)
			#print(hashval)
		else:
			#print("Ciphered: %r" % r)
			newval = string_to_bit_array(r)
			#print(newval)
		
			#print("len hasval= ",len(hashval), "len newval= ",len(newval))
			for p in range(len(hashval)):
				hashval[p] = hashval[p] ^ newval[p]
	return bit_array_to_string(hashval)


#phase1.iii
def computeTag(val):
	h = ""
	h = d1.encrypt("secret_k","escret_k","cseret_k",val,padding=True)
	return h
		

#class des is opensource github code
d = des()

#i implemented desprp (premutation generation); made by three rounds for des and a random function
# more details can be found in the paper mentioned in current file header
d1 = desprp()



'''
phase2: incremental update: assume that a block is added after ith position in the original documet
To recompute the hash on updated document
i) coupte back the hash from the tag 
ii) get the rand value for the new block = R'
iii) compute new has hash
'''

#phase2.i
def computeTagInv(val):
	h = ""
	h = d1.decrypt("secret_k","escret_k","cseret_k",val,padding=True)
	return h

def randomiseFuncIns(insertStrings):
	for i in insertStrings:
		two_i  = i + i
		pos = random.randint(1, 8)
		number = random.randint(1, 8)
		randomInsertStrings.append(i + two_i[pos:number+1])


#block "hello wo" inserted at positon
def computeHashDash(randomInsertStrings, positon, randorgStrings, oldhash):
	resultxor = []
	for i in range (0,len(randomInsertStrings)):
		
		r1 = d.encrypt(utf8_byte_truncate(randorgStrings[positon], 8).decode("utf-8"),utf8_byte_truncate(randorgStrings[positon+1], 8).decode("utf-8"),padding=True)
		
		r2 = d.encrypt(utf8_byte_truncate(randorgStrings[positon], 8).decode("utf-8"),utf8_byte_truncate(randomInsertStrings[i], 8).decode("utf-8"),padding=True)

		r3 = d.encrypt(utf8_byte_truncate(randomInsertStrings[i], 8).decode("utf-8"),utf8_byte_truncate(randorgStrings[positon+1], 8).decode("utf-8"),padding=True)

		b1 = string_to_bit_array(r1)
		b2 = string_to_bit_array(r2)
		b3 = string_to_bit_array(r3)
		b4 = string_to_bit_array(oldhash)

		for l in range(0,len(b1)):
			resultxor.append(b1[l] ^ b2[l] ^ b3[l] ^ b4[l])

	return(bit_array_to_string(resultxor))




if __name__ == '__main__':
	file = open("story.txt", "rb")
	key = "secret_k"
	byte = file.read(8)
	
	while byte:
		bytestring = byte.decode("utf-8") 
		orgStrings.append(bytestring)
		# print("8byte: ",byte)#text= "Hello wo"
		# r = d.encrypt(key,bytestring,padding=True)
		# r2 = d.decrypt(key,r) #prints in bytes. can be use to store in file directly
		# print("Ciphered: %r" % r)
		# print("Deciphered: ", r2)
		
		byte = file.read(8)
	randomiseFunc(orgStrings)
	hashval = chainAndHash(randorgStrings)
	print("hashval: %r" % hashval)
	tagval = computeTag(hashval)
	print("Tag: %r" % tagval)
	print("hashVal = TagInv: %r" % computeTagInv(tagval))

	insertStrings.append("Hello wo")

	randomiseFuncIns(insertStrings)
	newhash = computeHashDash(randomInsertStrings, 30, randorgStrings, hashval)
	print("newhash: %r" % newhash)

	newtagval = computeTag(newhash)
	print("newtag: %r" % newtagval)


'''
phase2:
expected output
yash@Yaswanths-MacBook-Air project % python3 xor_auth.py
hashval: '·\x1e¬2$N\x06@\x1c*¹ZH+SÊ'
Tag: 'ü\x8f\x94+IÎE\x02ßtC\x07ÕLqºNôÐö+jñA'
hashVal = TagInv: '·\x1e¬2$N\x06@\x1c*¹ZH+SÊ'
newhash: '\x06]Ö£ãwF\xa0¦±ö\x884Ð44'
newtag: 'm]ü!C®E¹\rß\x80ýq¢tÙNôÐö+jñA'
'''



