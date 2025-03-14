from passlib.context import CryptContext

# Use sha256_crypt instead of bcrypt to avoid compatibility issues
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Hash a password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)