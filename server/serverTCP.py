# Socket Principal, manejo de clientes
import socket
import threading
import json
from graph_manager import SocialGraph
from database import UserDataBase
from auth import *

class SocialtecServer:
    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET,  socket.SOCK_STREAM)
        self.clients = []
        self.graph = SocialGraph()
        self.db = UserDataBase()
        self.auth = AuthManager(generate_key())
        self._load_existing_users()

    def _load_existing_users(self):
        """"Carga usuarios existentes en el grafo"""
        for username in self.db.data["users"]:
            self.graph.add_user(username)
            # Cargar amistades existentes
            for friend in self.db.data["users"][username]["friends"]:
                self.graph.add_friendship(username, friend)

    def start(self):
        """"Inicia el servidor"""
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Servidor SocialTEC escuchando en {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            print("Nuevo cliente conectado: {address}")
            cliente_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket,)
            )
            cliente_thread.start()

    def handle_client(self, client_socket):
        """Maneja comunicación con un cliente"""
        with client_socket:
            while True:
                try:
                    # Recibir datos (encriptados)
                    encrypted_data = client_socket.recv(4096).decode()
                    if not encrypted_data:
                        break

                    # Desencriptar
                    data = self.auth.decrypt_data(encrypted_data)
                    request = json.loads(data)

                    # Procesar solicitud
                    response = self.process_request(request)

                    # Encriptar y enviar respuesta
                    response_json = json.dumps(response)
                    encrypted_response = self.auth.encrypt_data(response_json)
                    client_socket.send(encrypted_response.encode())
                
                except Exception as e:
                    print(f"Error con el cliente en 'self.handle_client': {e}")
                    break
    
    def process_request(self, request: dict) -> dict:
        """Procesa diferentes tipos de solicitudes"""
        action = request.get("action")

        if action == "login":
            return self._handle_login(request)
        elif action == "register":
            return self._handle_register(request)
        elif action == "add_friend":
            return self._handle_add_friend(request)
        elif action == "remove_friend":
            return self._handle_remove_friend(request)
        elif action == "find_path":
            return self._handle_find_path(request)
        elif action == "get_stats":
            return self._handle_get_stats(request)
        else:
            return {"status": "error", "message": "Acción no válida"}

    def _handle_login(self, request: dict) -> dict:
        username = request.get("username")
        password = request.get("password")
        user_data = self.db.get_user(username)

        if user_data and self.auth.verify_password(password, user_data["password_hash"]):
            return {"status": "success", "user_data": user_data}
        return {"status": "error", "message": "Credenciales incorrectas"}

    def _handle_register(self, request: dict) -> dict:
        username = request.get("username")
        password = request.get("password")
        name = request.get("name")
        photo = request.get("photo", "")

        if self.db.add_user(username, self.auth.hash_password(password), name, photo):
            self.graph.add_user(username)
            return {"status": "success", "message": "Usuario registrado"}
        return {"status": "error", "message": "Usuario ya existe"}

    def _handle_add_friend(self, request: dict) -> dict:
        user1 = request.get("user1")
        user2 = request.get("user2")

        if self.graph.add_friendship(user1, user2):
            self.db.add_friend(user1, user2)
            return {"status": "success", "message": "Amistad agregada"}
        return {"status": "error", "message": "No se pudo agregar amistad"}

    def _handle_remove_friend(self, request: dict) -> dict:
        user1 = request.get("user1")
        user2 = request.get("user2")

        if self.graph.remove_friendship(user1, user2):
            self.db.remove_friend(user1, user2)
            return {"status": "success", "message": "Amistad eliminada"}
        return {"status": "error", "message": "No se pudo eliminar amistad"}

    def _handle_find_path(self, request: dict) -> dict:
        start = request.get("start")
        end = request.get("end")
        path = self.graph.find_friend_path(start, end)

        if path:
            return {"status": "success", "path": path}
        return {"status": "error", "message": "No hay camino"}

    def _handle_get_stats(self, request: dict) -> dict:
        stats = self.graph.get_statistics()
        return {"status": "success", "stats": stats}