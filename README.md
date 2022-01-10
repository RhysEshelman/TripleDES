# TripleDES
A Python implementation of Triple DES

The program takes an input string of 24 ASCII characters (24 bytes), and then generates all the subkeys for 3DES from that key. My program uses 3-key 3DES, meaning each round of DES uses a different key. The first 8 characters of the input string are used for the first round of DES, the next 8 are used for the second round, and so on. So all you need to do is create a TripleDES object with the only field being the 24 character input string. For example, T = TripleDES('12345678abcdefg87654321') would be a valid object. After that just call the encrypt function with whatever message you would like to encrypt; for example, T.encrypt('here is an example message') will then return the encrypted ciphertext. Then just call the decrypt function with the ciphertext and you will get the original plaintext.
