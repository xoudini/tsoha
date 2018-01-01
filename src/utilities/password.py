import bcrypt
import re

class PasswordUtility:

    def validate_string(self, unvalidated: str) -> str:
        invalid = '\0'
        return re.sub('[%s]' % invalid, '', unvalidated)

    def encode_string(self, unencoded: str) -> bytes:
        validated = self.validate_string(unencoded)
        return bytes(validated, encoding='utf-8')

    def generate_hash(self, password: str) -> str:
        encoded = self.encode_string(password)
        return bcrypt.hashpw(encoded, bcrypt.gensalt())

    def matches(self, password: str, passwordhash: str) -> bool:
        encoded = self.encode_string(password)
        return bcrypt.checkpw(encoded, passwordhash)
