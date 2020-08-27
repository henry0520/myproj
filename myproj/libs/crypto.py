"""
*************************************************
© YYYY - 2020 InterVenn. All Rights Reserved.
*************************************************
"""
import string
import M2Crypto.Rand

def random(count):
    return M2Crypto.Rand.rand_bytes(count)

def random_alnum(count):
    bytes = random(count)
    chars = string.ascii_letters + string.digits
    chars_len = len(chars)
    return ''.join([chars[(byte) % chars_len] for byte in bytes])
