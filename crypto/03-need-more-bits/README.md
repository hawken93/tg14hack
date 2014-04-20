Need more bits!
===============

Description
-----------

You have stumbled over a new message! Unfortunately, you only managed to get the public key. Can you still decrypt it?

`{0x0b, 0x0b, 0x85, 0x72, 0x0c, 0x9d, 0x2e, 0x85, 0xb8, 0x8a, 0xf9, 0xc4, 0x7a, 0x94, 0xd3, 0x3e, 0x14, 0x0f, 0x78, 0x5e, 0x04, 0x0f, 0x5a, 0xdd, 0xd1, 0xea, 0x03, 0xb1, 0xf8, 0x9d, 0x3d, 0xef, 0x0c, 0xbe, 0xaa, 0x5a, 0x06, 0x19, 0x4f, 0x93, 0x63, 0xfc, 0xc5, 0xcc, 0xe9, 0x7c, 0x5e, 0xd7, 0x0d, 0x7d, 0xc1, 0x24, 0x38, 0xf1, 0x9e, 0xa9, 0x5d, 0x86, 0x5e, 0x7e, 0x98, 0x89, 0xaa, 0xd0, 0x1c, 0x66, 0x34, 0x2f, 0x71, 0xde, 0x0f, 0x98, 0xba, 0x89, 0x97, 0x6f, 0x26, 0x42, 0x2b, 0x40, 0x0d, 0xad, 0xc2, 0xb8, 0xeb, 0x25, 0x43, 0x0f, 0x8f, 0x7c, 0xd8, 0xd3, 0x36, 0xa4, 0x0b, 0xdc, 0x1b, 0x13, 0xff, 0xb7, 0xae, 0x06, 0x0e, 0xcf, 0xc3, 0x28, 0x5b, 0xaf, 0xf6, 0x23, 0xe4, 0xd8}`

`Pubkey: Key(exponent=28806617666072351940591555263157654721L, modulus=40497789112468128662933233861484902553L)`

Solution
--------
* If you'd rather read code, rsa.py is for you.
* First, crack the RSA. Here are the steps:
 * Factorize the modulus. (Online tools 3) The factors are called p and q. `p=5467663316330766641, q=7406781794978067433`
 * Compute the totient: `totient=(p-1)\*(q-1) = (5467663316330766641-1)\*(7406781794978067433-1) = 40497789112468128650058788750176068480`
 * run [modular inverse](http://en.wikipedia.org/wiki/Modular_multiplicative_inverse) of your exponent, modulus the totient: `multinv(28806617666072351940591555263157654721, 40497789112468128650058788750176068480) = 18144556919192175292668077935484856001` see multinv.py (Note that arguments are reversed)
 * Congrats, your private key is the following: `Key(exponent=18144556919192175292668077935484856001L, modulus=40497789112468128662933233861484902553L)`
* Second, decrypt the data.
 * Data is 112 bytes long, we factorize to get 7 \* 2^4. It makes sense if one block is 16 bytes and there are 7 of them.
 * The logarithm hint: (You can skip this the first time you read it)
    * The modulus is the number of unique values we can have per (huge) integer that we encrypt.
    * If we are interested in storing bytes, then we should find out how many bytes we can have and still be under our modulus
    * Turns out that:
      * `256^15 = 1329227995784915872903807060280344576`
      * `256^16 = 340282366920938463463374607431768211456`
      * `modulus= 40497789112468128650058788750176068480`
      * We can store 15 bytes within our modulus, but 16 bytes is too much.
      * Our modulus equals around 15.6 bytes, so we need to use 16 bytes per integer that we store. Hence, we will be storing in 16 byte blocks that we extract 15 bytes from.
 * What you might have skipped is just one way of understanding that the block size is 16 bytes.
 * So, to prove it, we will convert the 16 first bytes into a number:
 * `0x0b, 0x0b, 0x85, 0x72, 0x0c, 0x9d, 0x2e, 0x85, 0xb8, 0x8a, 0xf9, 0xc4, 0x7a, 0x94, 0xd3, 0x3e`
 * We will just treat this as a 128 bit MSB integer, and get `14681329815469611171265110655343317822`
   * (in python, `int("0b0b85720c9d2e85b88af9c47a95d33e", 16)` would reproduce this ^
 * Then we multipy by the private key exponent and apply our modulus
   * (python: `pow(14681329815469611171265110655343317822, 18144556919192175292668077935484856001, 40497789112468128662933233861484902553)` )
    * The reason this is fast, is because it uses [Modular exponentiation](http://en.wikipedia.org/wiki/Modular_exponentiation)
   * We get: `281441281418489127035953670741060713`
 * This can be converted back, see convertback.py
 * Doing this to the next block seems to produce junk, because we need to do [CBC](http://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher-block_chaining_.28CBC.29)
  * Once we get that junk, just xor it with the ciphertext of the previous block.
 * See rsa.py for the solution.
