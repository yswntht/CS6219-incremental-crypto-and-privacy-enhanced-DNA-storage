#privacy is by obfuscation

import sys
from os.path import dirname
sys.path.append(dirname("/Users/yash/Documents/dna_project/project"))

from doubleLL import Node, DoublyLinkedList


import random
random.seed(3)

randAddr = []
flipcoin = []
addrKeeper = []

dataKeeper = {}


#with a seed , generate random addresees
def randgenAddr():
    for i in range (1024 * 10):
        randAddr.append(random.randint(1, 1024))

randgenAddr()

random.seed(33)

#with a seed, generate random list of coin flips
def randgencoins():
    for i in range (1024 * 10):
        flipcoin.append(random.randint(0, 1))

randgencoins()
maxupdates = 500
counter = 0

#coin toss - 0 push, 1 append
llist = DoublyLinkedList()

'''
the algorithm user three structures: 1) a hash table 2) a linked list 3) a list

step1: get random address from the pre-generated addresses list. add to hash table as a key and for value, get 
the data/update from file (random chunk), here I get atmost 10 bytes for every update.

step2: now, after adding key and value to the hash table, we now flip a coin and basing on the outcome
we push or append random-address from step1 to linkedlist. push is to add address to head-node 
while append is to add to the tail node. this step creates obfuscation.

step3: keep a track on order of random-addresses
'''

if __name__ == '__main__':
    file = open("story.txt", "rb")
    byte = file.read(8)
    while byte:
        bytestring = ""
        bytestring = byte.decode("utf-8")
        for ele in randAddr:
            if ele not in dataKeeper:
                dataKeeper[ele] = bytestring
                addrKeeper.append(ele)
                byte = file.read(random.randint(1, 10))
                bytestring = byte.decode("utf-8")
                toss = flipcoin[counter]
                if(toss == 0):
                    llist.push(ele)
                if(toss == 1):
                    llist.append(ele)
                counter = counter + 1
            if(counter == 500):
                break
        break
    llist.printList(llist.head)
    print(addrKeeper)


		


