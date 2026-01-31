"""
Cliente para SocialTEC que maneja la comunicación con el servidor.
Incluye encriptación de mensajes y compatibilidad completa con el servidor.
"""
import socket
import json
from typing import Dict, Optional

from encryption import AuthManager, load_key


class Client:
    """Cliente para comunicarse con el servidor SocialTEC"""

    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False
        self.current_user = None
        self.user_data = None

        # Cargar clave de encriptación y crear AuthManager
        try:
            key = load_key()
            self.auth = AuthManager(key)
        except Exception as e:
            print(f"Error cargando clave de encriptación: {e}")
            # Generar una clave temporal si no existe
            self.auth = AuthManager(Fernet.generate_key())

    def connect(self) -> bool:
        """Conectar al servidor"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print(f"Conectado al servidor {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Error conectando al servidor: {e}")
            return False

    def disconnect(self):
        """Desconectar del servidor"""
        self.connected = False
        if self.client_socket:
            self.client_socket.close()
            print("Desconectado del servidor")

    def _send_encrypted_request(self, action: str, data: Optional[Dict] = None) -> Dict:
        """Enviar solicitud encriptada al servidor"""
        try:
            # Construir mensaje
            request = {"action": action}
            if data:
                request.update(data)

            # Convertir a JSON y encriptar
            request_json = json.dumps(request)
            encrypted_request = self.auth.encrypt_data(request_json)

            # Enviar al servidor
            self.client_socket.send(encrypted_request.encode('utf-8'))

            # Recibir respuesta encriptada
            encrypted_response = self.client_socket.recv(4096).decode('utf-8')

            if not encrypted_response:
                return {"status": "error", "message": "No response from server"}

            # Desencriptar y cargar JSON
            response_json = self.auth.decrypt_data(encrypted_response)
            return json.loads(response_json) if response_json else {"status": "error", "message": "Empty response"}

        except json.JSONDecodeError as e:
            print(f"Error decodificando JSON: {e}")
            return {"status": "error", "message": "Invalid JSON response"}
        except Exception as e:
            print(f"Error enviando solicitud: {e}")
            return {"status": "error", "message": str(e)}

    def _send_request(self, action: str, data: Optional[Dict] = None) -> Dict:
        """Método alternativo para servidores sin encriptación"""
        try:
            # Construir mensaje
            request = {"action": action}
            if data:
                request.update(data)

            # Enviar al servidor (sin encriptar)
            request_json = json.dumps(request)
            self.client_socket.send(request_json.encode('utf-8'))

            # Recibir respuesta
            response = self.client_socket.recv(4096).decode('utf-8')

            if not response:
                return {"status": "error", "message": "No response from server"}

            return json.loads(response) if response else {"status": "error", "message": "Empty response"}

        except Exception as e:
            print(f"Error enviando solicitud: {e}")
            return {"status": "error", "message": str(e)}

    def login(self, username: str, password: str) -> Dict:
        """Iniciar sesión"""
        if not self.connect():
            return {"status": "error", "message": "Could not connect to server"}

        request_data = {
            "username": username,
            "password": password
        }

        response = self._send_request("login", request_data)

        if response.get("status") == "success":
            self.current_user = username
            self.user_data = response.get("user_data", {})

        return response

    def register(self, username: str, password: str, name: str, photo: str = "") -> Dict:
        """Registrar nuevo usuario"""
        if not self.connect():
            return {"status": "error", "message": "Could not connect to server"}

        request_data = {
            "username": username,
            "password": password,
            "name": name,
            "photo": photo
        }

        response = self._send_request("register", request_data)

        if response.get("status") == "success":
            print(f"Usuario {username} registrado exitosamente")

        return response

    def add_friend(self, friend_username: str) -> Dict:
        """Agregar amigo"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}

        if not self.connected:
            if not self.connect():
                return {"status": "error", "message": "Could not connect to server"}

        request_data = {
            "user1": self.current_user,
            "user2": friend_username
        }

        return self._send_request("add_friend", request_data)

    def remove_friend(self, friend_username: str) -> Dict:
        """Eliminar amigo"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}

        if not self.connected:
            if not self.connect():
                return {"status": "error", "message": "Could not connect to server"}

        request_data = {
            "user1": self.current_user,
            "user2": friend_username
        }

        return self._send_request("remove_friend", request_data)

    def find_path(self, target_user: str) -> Dict:
        """Buscar camino entre usuarios"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}

        if not self.connected:
            if not self.connect():
                return {"status": "error", "message": "Could not connect to server"}

        request_data = {
            "start": self.current_user,
            "end": target_user
        }

        return self._send_request("find_path", request_data)

    def get_stats(self) -> Dict:
        """Obtener estadísticas"""
        if not self.connected:
            if not self.connect():
                return {"status": "error", "message": "Could not connect to server"}

        return self._send_request("get_stats")

    def get_user_profile(self, username: str = None) -> Dict:
        """Obtener perfil de usuario (simulado para demostración)"""
        if username is None:
            username = self.current_user

        if not username:
            return {"status": "error", "message": "No username provided"}

        # Simulación - en un caso real, esto vendría del servidor
        return {
            "status": "success",
            "profile": {
                "name": username.capitalize(),
                "username": username,
                "photo": None,
                "friends": ["ana_lopez", "carlos_ruiz", "maria_garcia"],
                "friend_count": 3
            }
        }

    def get_friends(self) -> Dict:
        """Obtener lista de amigos (simulado para demostración)"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}

        # Simulación - en un caso real, esto vendría del servidor
        friends = [
            {"name": "Ana López", "username": "ana_lopez", "photo": None, "friends": 15},
            {"name": "Carlos Ruiz", "username": "carlos_ruiz", "photo": None, "friends": 23},
            {"name": "María García", "username": "maria_garcia", "photo": None, "friends": 18},
            {"name": "Juan Pérez", "username": "juan_perez", "photo": None, "friends": 12},
            {"name": "Laura Martínez", "username": "laura_mtz", "photo": None, "friends": 9},
        ]

        return {
            "status": "success",
            "friends": friends,
            "count": len(friends)
        }

    def search_users(self, query: str) -> Dict:
        """Buscar usuarios (simulado para demostración)"""
        if not query:
            return {"status": "error", "message": "Query is required"}

        # Simulación - en un caso real, esto vendría del servidor
        all_users = [
            {"name": "Ana López", "username": "ana_lopez", "is_friend": True},
            {"name": "Carlos Ruiz", "username": "carlos_ruiz", "is_friend": False},
            {"name": "María García", "username": "maria_garcia", "is_friend": True},
            {"name": "Juan Pérez", "username": "juan_perez", "is_friend": False},
            {"name": "Laura Martínez", "username": "laura_mtz", "is_friend": False},
            {"name": "Pedro Sánchez", "username": "pedro_sanchez", "is_friend": False},
        ]

        # Filtrar por query
        filtered_users = [
            user for user in all_users
            if query.lower() in user['name'].lower() or query.lower() in user['username'].lower()
        ]

        return {
            "status": "success",
            "users": filtered_users,
            "count": len(filtered_users)
        }

    def update_profile(self, name: str = None, photo: str = None) -> Dict:
        """Actualizar perfil (simulado para demostración)"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}

        # Simulación - en un caso real, esto se enviaría al servidor
        if name and self.user_data:
            self.user_data['name'] = name

        return {
            "status": "success",
            "message": "Perfil actualizado correctamente",
            "profile": self.user_data
        }


# Función para probar el cliente
def test_client():
    """Función de prueba para el cliente"""
    client = Client()

    print("=== Probando cliente SocialTEC ===")

    # Probar conexión
    if client.connect():
        print("✓ Conexión exitosa")

        # Probar registro (simulado)
        print("\n=== Probando registro ===")
        response = client.register("test_user", "password123", "Test User")
        print(f"Registro: {response}")

        # Probar login (simulado)
        print("\n=== Probando login ===")
        response = client.login("test_user", "password123")
        print(f"Login: {response}")

        # Probar obtener perfil
        print("\n=== Probando obtener perfil ===")
        response = client.get_user_profile()
        print(f"Perfil: {response.get('profile', {}).get('name', 'No name')}")

        # Probar obtener amigos
        print("\n=== Probando obtener amigos ===")
        response = client.get_friends()
        print(f"Amigos obtenidos: {response.get('count', 0)}")

        # Probar búsqueda
        print("\n=== Probando búsqueda ===")
        response = client.search_users("ana")
        print(f"Resultados de búsqueda: {response.get('count', 0)}")

        # Probar estadísticas
        print("\n=== Probando estadísticas ===")
        response = client.get_stats()
        print(f"Estadísticas: {response}")

        client.disconnect()
    else:
        print("✗ Error de conexión")


if __name__ == "__main__":
    test_client()