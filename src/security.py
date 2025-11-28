import os
from pwdlib import PasswordHash

SECRET_KEY = os.getenv(
	'SECRET_KEY', '3451923f1a545ea6fe648d5a2ff6eca91a5522d9652d742df632779c8a75c8ce'
)
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30)

password_hash = PasswordHash.recommended()


def getPasswordHash(password):
	return password_hash.hash(password)


def verifyPassword(plain_password, hashed_password):
	return password_hash.verify(plain_password, hashed_password)
