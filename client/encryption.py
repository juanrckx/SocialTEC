"""
Módulo de encriptación para el cliente SocialTEC.
Maneja la encriptación y desencriptación de mensajes para la comunicación con el servidor.
"""
import json
import os
from cryptography.fernet import Fernet


def load_key(key_file: str = "shared/secret.key") -> bytes:
    """
    Carga la clave de encriptación desde un archivo.
    Si el archivo no existe, genera una nueva clave y la guarda.

    Args:
        key_file: Ruta al archivo de clave (por defecto 'shared/secret.key')

    Returns:
        bytes: Clave de encriptación
    """
    # Asegurarse de que el directorio existe
    os.makedirs(os.path.dirname(key_file), exist_ok=True)

    if os.path.exists(key_file):
        with open(key_file, 'rb') as f:
            return f.read()
    else:
        # Generar una nueva clave
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
        print(f"Clave generada y guardada en {key_file}")
        return key


class AuthManager:
    """
    Manager para encriptación y desencriptación usando Fernet (cryptography).
    Compatible con el servidor SocialTEC.
    """

    def __init__(self, key: bytes = None):
        if key is None:
            key = load_key()
        self.cipher = Fernet(key)

    def encrypt_data(self, data: str) -> str:
        """
        Encripta una cadena de texto.

        Args:
            data: Texto a encriptar

        Returns:
            str: Texto encriptado (en base64)
        """
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Desencripta una cadena de texto previamente encriptada.

        Args:
            encrypted_data: Texto encriptado (en base64)

        Returns:
            str: Texto desencriptado
        """
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def encrypt_message(self, message_dict: dict) -> str:
        """
        Encripta un diccionario completo (convierte a JSON primero).

        Args:
            message_dict: Diccionario con el mensaje

        Returns:
            str: Mensaje encriptado
        """
        message_json = json.dumps(message_dict)
        return self.encrypt_data(message_json)

    def decrypt_message(self, encrypted_message: str) -> dict:
        """
        Desencripta un mensaje y lo convierte de vuelta a diccionario.

        Args:
            encrypted_message: Mensaje encriptado

        Returns:
            dict: Mensaje desencriptado como diccionario
        """
        try:
            decrypted_json = self.decrypt_data(encrypted_message)
            return json.loads(decrypted_json)
        except Exception as e:
            print(f"Error desencriptando mensaje: {e}")
            return {"status": "error", "message": "Failed to decrypt message"}


# Instancia global para uso en toda la aplicación
auth_manager = AuthManager()


# Funciones de conveniencia
def encrypt_data(data: str) -> str:
    """Encripta datos simples"""
    return auth_manager.encrypt_data(data)


def decrypt_data(encrypted_data: str) -> str:
    """Desencripta datos simples"""
    return auth_manager.decrypt_data(encrypted_data)


def encrypt_message(message_dict: dict) -> str:
    """Encripta un mensaje completo"""
    return auth_manager.encrypt_message(message_dict)


def decrypt_message(encrypted_message: str) -> dict:
    """Desencripta un mensaje completo"""
    return auth_manager.decrypt_message(encrypted_message)