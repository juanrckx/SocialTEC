# Socket Principal, manejo de clientes
import socket
import os
import threading
import json
from graph_manager import SocialGraph
from database import UserDataBase
from auth import *

class SocialtecServer:
    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.graph = SocialGraph()
        self.db = UserDataBase()
        
        # Cargar clave desde archivo compartido
        key_file = "../shared/secret.key"
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
            print(f"Clave cargada desde {key_file}")
        else:
            # Generar y guardar clave si no existe
            key = generate_key()
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(key)
            print(f"Clave generada y guardada en {key_file}")
        
        self.auth = AuthManager(key)
        self._load_existing_users()  # Cargar usuarios existentes

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
        print(f"Servidor SocialTEC escuchando en {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Nuevo cliente conectado: {address}")
            cliente_thread = threading.Thread(
                target=self.handle_client,
                args=(client_socket,)
            )
            cliente_thread.start()

    def handle_client(self, client_socket):
        """Maneja comunicación con un cliente - CON PROTOCOLO DE LONGITUD"""
        self.clients.append(client_socket)
        client_address = client_socket.getpeername()

        with client_socket:
            while True:
                try:
                    # 1. RECIBIR LONGITUD DEL MENSAJE (4 bytes)
                    length_bytes = client_socket.recv(4)
                    if not length_bytes:
                        print("Cliente desconectado")
                        break
                    
                    message_length = int.from_bytes(length_bytes, 'big')
                    print(f"Esperando mensaje de {message_length} bytes")
                    
                    # 2. RECIBIR MENSAJE COMPLETO
                    encrypted_data = b""
                    while len(encrypted_data) < message_length:
                        chunk = client_socket.recv(min(4096, message_length - len(encrypted_data)))
                        if not chunk:
                            break
                        encrypted_data += chunk
                    
                    if len(encrypted_data) != message_length:
                        print(f"Mensaje incompleto: {len(encrypted_data)}/{message_length} bytes")
                        # Enviar error al cliente
                        error_response = json.dumps({
                            "status": "error", 
                            "message": "Mensaje incompleto recibido"
                        })
                        encrypted_error = self.auth.encrypt_data(error_response)
                        error_length = len(encrypted_error)
                        client_socket.send(error_length.to_bytes(4, 'big'))
                        client_socket.send(encrypted_error.encode())
                        continue
                    
                    print(f"Mensaje completo recibido ({len(encrypted_data)} bytes)")
                    
                    # 3. DESENCRIPTAR
                    try:
                        data = self.auth.decrypt_data(encrypted_data.decode())
                        request = json.loads(data)
                    except Exception as e:
                        print(f"Error desencriptando/parseando: {e}")
                        # Enviar error
                        error_response = json.dumps({
                            "status": "error", 
                            "message": f"Error procesando mensaje: {str(e)}"
                        })
                        encrypted_error = self.auth.encrypt_data(error_response)
                        error_length = len(encrypted_error)
                        client_socket.send(error_length.to_bytes(4, 'big'))
                        client_socket.send(encrypted_error.encode())
                        continue
                    
                    # 4. PROCESAR SOLICITUD
                    response = self.process_request(request)
                    
                    # 5. ENVIAR RESPUESTA CON PROTOCOLO DE LONGITUD
                    response_json = json.dumps(response)
                    encrypted_response = self.auth.encrypt_data(response_json)
                    response_length = len(encrypted_response)
                    
                    # Enviar longitud
                    client_socket.send(response_length.to_bytes(4, 'big'))
                    # Enviar mensaje
                    client_socket.sendall(encrypted_response.encode())
                    print(f"Respuesta enviada ({response_length} bytes)")
                
                except json.JSONDecodeError as e:
                    print(f"Error JSON: {e}")
                    # Enviar error JSON
                    error_response = json.dumps({
                        "status": "error", 
                        "message": "JSON inválido recibido"
                    })
                    encrypted_error = self.auth.encrypt_data(error_response)
                    error_length = len(encrypted_error)
                    try:
                        client_socket.send(error_length.to_bytes(4, 'big'))
                        client_socket.send(encrypted_error.encode())
                    except:
                        pass
                except Exception as e:
                    print(f"Error con el cliente: {client_address}: {e}")
                finally:
                    if client_socket in self.clients:
                        self.clients.remove(client_socket)
                    print(f"Cliente {client_address} desconectado")
    
    def process_request(self, request: dict) -> dict:
        """Procesa diferentes tipos de solicitudes"""
        action = request.get("action")

        if action == "login":
            return self._handle_login(request)
        elif action == "register":
            return self._handle_register(request)
        elif action == "update_profile":
            return self._handle_update_profile(request)
        elif action == "change_password":
            return self._handle_change_password(request)
        elif action == "add_friend":
            return self._handle_add_friend(request)
        elif action == "remove_friend":
            return self._handle_remove_friend(request)
        elif action == "get_friends":
            return self._handle_get_friends(request)
        elif action == "find_path":
            return self._handle_find_path(request)
        elif action == "get_suggestions":
            return self._handle_get_suggestions(request)
        elif action == "search_user":
            return self._handle_search_users(request)
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
    
    def _handle_update_profile(self, request: dict) -> dict:
        """Actualiza el perfil del usuario"""
        username = request.get("username")
        name = request.get("name")
        photo = request.get("photo", None)

        user_data = self.db.get_user(username)
        if not user_data:
            return {"status": "error", "message": "Usuario no encontrado"}
        
        # Actualizar nombre
        if name:
            user_data["name"] = name

        # Actualizar foto solo si se proporciona una nueva
        if photo is not None:
            user_data["photo"] = photo

        self.db._save_data()
        return {"status": "success", "message": "Perfil actualizado", "user_data": user_data}
    
    def _handle_change_password(self, request: dict) -> dict:
        """Cambia la contraseña del usuario"""
        username = request.get("username")
        old_password = request.get("old_password")
        new_password = request.get("new_password")

        user_data = self.db.get_user(username)
        if not user_data:
            return {"status": "error", "message": "Usuario no encontrado"}
        
        if not self.auth.verify_password(old_password, user_data["password_hash"]):
            return {"status": "error", "message": "Contraseña actual incorrecta"}
        
        user_data["password_hash"] = self.auth.hash_password(new_password)
        self.db._save_data()
        return {"status": "success", "message": "Contraseña cambiada con éxito"}

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
    
    def _handle_get_friends(self, request: dict) -> dict:
        """Maneja solicitud de obtener amigos"""
        username = request.get("username")
        user_data = self.db.get_user(username)

        if not user_data:
            return {"status": "error", "message": "Usuario no encontrado"}
        
        friends_list = []
        for friend_username in user_data.get("friends", []):
            friend_data = self.db.get_user(friend_username)
            if friend_data:
                friends_list.append({
                    "name": friend_data.get("name", ""),
                    "username": friend_username,
                    "photo": friend_data.get("photo", ""),
                    "friend_count": len(friend_data.get("friends", []))
                })

        return {"status": "success", "friends": friends_list}

    def _handle_find_path(self, request: dict) -> dict:
        start = request.get("start")
        end = request.get("end")
        path = self.graph.find_friend_path(start, end)

        if path:
            return {"status": "success", "path": path}
        return {"status": "error", "message": "No hay camino"}
    
    def _handle_get_suggestions(self, request: dict) -> dict:
        """Maneja la obtención de sugerencias de amigos basadas en amigos en común"""
        username = request.get("username")
        
        user_data = self.db.get_user(username)
        if not user_data:
            return {"status": "error", "message": "Usuario no encontrado"}
        
        current_friends = set(user_data.get("friends", []))
        suggestions_map = {}
        
        # Algoritmo: Para cada amigo, ver los amigos de ese amigo
        for friend_username in current_friends:
            friend_data = self.db.get_user(friend_username)
            if friend_data:
                for friend_of_friend in friend_data.get("friends", []):
                    # No incluir al usuario mismo ni a sus amigos actuales
                    if friend_of_friend != username and friend_of_friend not in current_friends:
                        if friend_of_friend not in suggestions_map:
                            suggestions_map[friend_of_friend] = {
                                "common_friends": 1,
                                "data": self.db.get_user(friend_of_friend)
                            }
                        else:
                            suggestions_map[friend_of_friend]["common_friends"] += 1
        
        # Ordenar por número de amigos en común (mayor primero)
        sorted_suggestions = sorted(
            suggestions_map.items(),
            key=lambda x: x[1]["common_friends"],
            reverse=True
        )
        
        # Preparar respuesta
        suggestions = []
        for username_suggestion, info in sorted_suggestions[:10]:  # Limitar a 10 sugerencias
            user_info = info["data"]
            if user_info:
                suggestions.append({
                    "name": user_info.get("name", username_suggestion),
                    "username": username_suggestion,
                    "photo": user_info.get("photo", ""),
                    "friend_count": len(user_info.get("friends", [])),
                    "common_friends": info["common_friends"]
                })
        
        return {"status": "success", "suggestions": suggestions} 

    def _handle_search_users(self, request: dict) -> dict:
        """Maneja búsqueda de usuarios"""
        query = request.get("query", "").lower()
        current_user = request.get("current_user", "")

        results = []
        current_user_data = self.db.get_user(current_user)
        current_friends = current_user_data.get("friends", []) if current_user_data else []

        for username, user_data in self.db.data["users"].items():
            if username == current_user:
                continue

            name = user_data.get("name", "").lower()
            if query in username.lower() or query in name:
                results.append({
                    "name": user_data.get("name", ""),
                    "username": username,
                    "photo": user_data.get("photo", ""),
                    "friend_count": len(user_data.get("friends", [])),
                    "is_friend": username in current_friends
                })

        return {"status": "success", "users": results}

    def _handle_get_stats(self, request: dict) -> dict:
        stats = self.graph.get_statistics()
        return {"status": "success", "stats": stats}