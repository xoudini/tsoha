import bcrypt
import re

class PasswordUtility:

    def validate_string(self, unvalidated: str) -> str:
        invalid = '\0'
        return re.sub('[%s]' % invalid, '', unvalidated)

    def encode_string(self, unencoded: str) -> bytes:
        validated = self.validate_string(unencoded)
        return bytes(validated, encoding='utf-8')
    
    def decode_string(self, encoded: bytes) -> str:
        return encoded.decode('utf-8')

    def generate_hash(self, password: str) -> bytes:
        encoded = self.encode_string(password)
        return bcrypt.hashpw(encoded, bcrypt.gensalt())

    def matches(self, password: str, hash_string: str) -> bool:
        encoded_password = self.encode_string(password)
        encoded_hash = bytes(hash_string, encoding='utf-8')
        return bcrypt.checkpw(encoded_password, encoded_hash)
