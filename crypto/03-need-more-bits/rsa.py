from collections import namedtuple
from math import log
from binascii import hexlify, unhexlify
import sys
import math

from multinv import *

KeyPair = namedtuple('KeyPair', 'public private')
Key = namedtuple('Key', 'exponent modulus')

def encode(msg, pubkey, verbose=False):
    chunksize = int(log(pubkey.modulus, 256))
    outchunk = chunksize + 1
    outfmt = '%%0%dx' % (outchunk * 2,)
    bmsg = msg.encode()
    result = []
    prev = False
    for start in range(0, len(bmsg), chunksize):
        chunk = bmsg[start:start+chunksize]
        chunk += b'\x00' * (chunksize - len(chunk))
        plain = int(hexlify(chunk), 16)
	# If prev exists, then xor with that (prev = cipher of previous block)
	if prev != False:
		plain = plain^prev

        coded = pow(plain, *pubkey)
	# Remember this ciphertext for next block
        prev = coded

	bcoded = unhexlify((outfmt % coded).encode())
        if verbose: print('Encode:', chunksize, chunk, plain, coded, bcoded)
        result.append(bcoded)
    return b''.join(result)

def decode(bcipher, privkey, verbose=False):
    chunksize = int(log(pubkey.modulus, 256))
    outchunk = chunksize + 1 # 16
    outfmt = '%%0%dx' % (chunksize * 2,)

    result = []

    prev = False
    for start in range(0, len(bcipher), outchunk): # For each 16 byte block in our cipher
	bcoded = bcipher[start: start + outchunk]

	coded = int(hexlify(bcoded), 16) # Convert to hex, then convert to int base 16

        plain = pow(coded, *privkey)
	if prev != False:
		plain = plain^prev

	prev = coded
        chunk = unhexlify((outfmt % plain).encode())
        if verbose: print('Decode:', chunksize, chunk, plain, coded, bcoded)
        result.append(chunk)
    return b''.join(result).rstrip(b'\x00').decode()

# I love this one!
def crack_key(key):
	exp, mod = key
	p = long(raw_input("Factorize "+str(mod)+", and give me one prime factor: "))
	if (mod % p) != 0 or p < 2:
		print "liar"
		return 0
	q = mod / p
	# p & q

	tot = (q-1)*(p-1)
	d = multinv(tot,exp)
	return Key(d, mod)


if __name__ == '__main__':
    #import doctest
    #print(doctest.testmod())

    pubkey = Key(28806617666072351940591555263157654721, 40497789112468128662933233861484902553)
    token = "Ron Rivest does not approve!"
    msg = '64 bits is a little too low for cryptography these days. Token: '+token
    h = encode(msg, pubkey, 0)

    privkey = crack_key(pubkey)
    print privkey
#    privkey = Key(18144556919192175292668077935484856001L, 40497789112468128662933233861484902553L)

    p = decode(h, privkey, 1)
    print p
