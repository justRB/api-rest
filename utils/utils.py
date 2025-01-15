import bcrypt

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf8'), salt)
    return hashed_password

def check_password(hashed_password: bytes, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf8'), hashed_password)
