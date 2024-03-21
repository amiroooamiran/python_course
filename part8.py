import hashlib

string_to_hash = "Hello, amirooo"
sha256 = hashlib.sha256(string_to_hash.encode()).hexdigest()
print(sha256)