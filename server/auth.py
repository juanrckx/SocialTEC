# Autenticación con Passlib
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import base64

# Para hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Para encriptación simétrica de comunicación
def generate_key():
    return Fernet.generate_key()

class AuthManager:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def encrypt_data(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        return self.cipher.decrypt(encrypted_data.encode()).decode()