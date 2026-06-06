from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Function to verify if the password is correct, comparing the plain text password entered by the user and the password hash that will be saved in the database during account creation.
def check_password(password: str, hash_password: str) -> bool:
    if not password or not hash_password:
        return False
    
    return pwd_context.verify(password, hash_password)

# Function that generates and returns the password hash
def generate_password_hash(password: str) -> str:
    return pwd_context.hash(password)

