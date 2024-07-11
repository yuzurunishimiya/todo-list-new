"""Security Files"""

from typing import Union
from passlib.context import CryptContext


context = CryptContext(schemes="bcrypt")


def hash_text(plain_text: str) -> str:
    """to hash text"""

    hashed = context.hash(plain_text)
    return hashed


def verify_hashed(plain_text: str, hashed_text: Union[str, bytes]) -> bool:
    """verify hashed text"""

    is_verified = context.verify(plain_text, hashed_text)
    return is_verified
