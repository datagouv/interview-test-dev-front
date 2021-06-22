import hashlib


def hash_str(string, algorithm):
    h = getattr(hashlib, algorithm)()
    h.update(string.encode('utf-8'))
    return h.hexdigest()
