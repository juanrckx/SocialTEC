"""
Cliente para SocialTEC - Versión 100% compatible con servidor
"""
import os
import socket
import json
from typing import Dict, Optional
from cryptography.fernet import Fernet


# ========== AUTH MANAGER IDÉNTICO AL SERVIDOR ==========
class AuthManager:
    """EXACTAMENTE el mismo que en server/auth.py"""
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)  # ← ¡CORRECTO! No recursión

    def encrypt_data(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        return self.cipher.decrypt(encrypted_data.encode()).decode()


# ========== CLIENTE PRINCIPAL ==========
class Client:
    def __init__(self, host: str = "localhost", port: int = 8080):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False
        self.current_user = None
        self.user_data = None
        
        # Cargar clave COMPARTIDA con servidor
        key_file = "../shared/secret.key"  # ← ¡IMPORTANTE! Misma que servidor
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                key = f.read()
                print(f"Clave cargada desde {key_file}")
        else:
            print(f"ERROR: No existe {key_file}")
            print("Ejecuta en terminal: python3 -c \"from cryptography.fernet import Fernet; key = Fernet.generate_key(); open('../shared/secret.key', 'wb').write(key)\"")
            key = Fernet.generate_key()  # Temporal para pruebas
        
        self.auth = AuthManager(key)
        
    def _ensure_connection(self) -> bool:
        """Asegura que haya conexión antes de enviar"""
        try:
            if not self.connected or not self.client_socket:
                return self.connect()
            # Probar si la conexión sigue activa
            self.client_socket.settimeout(0.1)
            self.client_socket.recv(1, socket.MSG_PEEK)
            self.client_socket.settimeout(10)
            return True
        except:
            # Reconectar si hay error
            return self.connect()
    
    def connect(self) -> bool:
        """Conectar al servidor"""
        try:
            if self.client_socket:
                self.client_socket.close()
            
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(10)  # Timeout de 10 segundos
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            print(f"Conectado al servidor {self.host}:{self.port}")
            return True
        except ConnectionRefusedError:
            print(f"Servidor no disponible en {self.host}:{self.port}")
            return False
        except Exception as e:
            print(f"Error conectando: {e}")
            return False
    
    def _send_encrypted_request(self, action: str, data: Optional[Dict] = None) -> Dict:
        """Envía solicitud con protocolo de longitud fija"""
        try:
            # 1. Asegurar conexión
            if not self._ensure_connection():
                return {"status": "error", "message": "No se pudo conectar al servidor"}
            
            # 2. Construir mensaje (LIMITAR foto si es muy grande)
            request = {"action": action}
            if data:
                request_data = data.copy()
                # Si hay foto, limitar tamaño
                if "photo" in request_data and request_data["photo"]:
                    if len(request_data["photo"]) > 50000:  # 50KB en base64
                        print("Foto demasiado grande, recortando...")
                        request_data["photo"] = request_data["photo"][:50000]
                request.update(request_data)
            
            # 3. Convertir a JSON y ENCRIPTAR
            request_json = json.dumps(request, ensure_ascii=False)
            print(f"JSON tamaño: {len(request_json)} chars")
            
            encrypted_request = self.auth.encrypt_data(request_json)
            print(f"Encriptado: {len(encrypted_request)} chars")
            
            # 4. ENVIAR CON PROTOCOLO DE LONGITUD
            # Primero enviamos la longitud (4 bytes, big-endian)
            message_length = len(encrypted_request)
            self.client_socket.send(message_length.to_bytes(4, 'big'))
            
            # Luego enviamos el mensaje completo
            self.client_socket.sendall(encrypted_request.encode('utf-8'))
            print(f"Enviados {message_length} bytes")
            
            # 5. RECIBIR RESPUESTA CON PROTOCOLO DE LONGITUD
            # Primero recibir longitud (4 bytes)
            length_bytes = self.client_socket.recv(4)
            if not length_bytes:
                return {"status": "error", "message": "Servidor cerró conexión"}
            
            response_length = int.from_bytes(length_bytes, 'big')
            print(f"Esperando respuesta de {response_length} bytes")
            
            # Recibir mensaje completo
            encrypted_response = b""
            while len(encrypted_response) < response_length:
                chunk = self.client_socket.recv(min(4096, response_length - len(encrypted_response)))
                if not chunk:
                    break
                encrypted_response += chunk
            
            if len(encrypted_response) != response_length:
                print(f"Respuesta incompleta: {len(encrypted_response)}/{response_length} bytes")
                return {"status": "error", "message": "Respuesta incompleta del servidor"}
            
            print(f"Respuesta completa recibida")
            
            # 6. Desencriptar y parsear
            response_json = self.auth.decrypt_data(encrypted_response.decode('utf-8'))
            return json.loads(response_json)
            
        except socket.timeout:
            return {"status": "error", "message": "Timeout del servidor"}
        except Exception as e:
            print(f"Error en comunicación: {type(e).__name__}: {e}")
            return {"status": "error", "message": f"Error de comunicación: {str(e)}"}
    
    # ========== MÉTODOS PRINCIPALES ==========
    
    def login(self, username: str, password: str) -> Dict:
        """Iniciar sesión - LLAMA AL SERVIDOR REAL"""
        request_data = {
            "username": username.strip(),
            "password": password
        }
        response = self._send_encrypted_request("login", request_data)
        
        if response.get("status") == "success":
            self.current_user = username
            self.user_data = response.get("user_data", {})
            print(f"Login exitoso: {username}")
        
        return response
    
    def register(self, username: str, password: str, name: str, photo: str = "") -> Dict:
        """Registrar usuario - LLAMA AL SERVIDOR REAL"""
        request_data = {
            "username": username.strip(),
            "password": password,
            "name": name.strip(),
            "photo": photo
        }
        return self._send_encrypted_request("register", request_data)
    
    def add_friend(self, friend_username: str) -> Dict:
        """Agregar amigo - LLAMA AL SERVIDOR REAL"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}
        
        request_data = {
            "user1": self.current_user,
            "user2": friend_username.strip()
        }
        return self._send_encrypted_request("add_friend", request_data)
    
    def remove_friend(self, friend_username: str) -> Dict:
        """Eliminar amigo - LLAMA AL SERVIDOR REAL"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}
        
        request_data = {
            "user1": self.current_user,
            "user2": friend_username.strip()
        }
        return self._send_encrypted_request("remove_friend", request_data)
    
    def find_path(self, target_user: str) -> Dict:
        """Buscar camino - LLAMA AL SERVIDOR REAL"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}
        
        request_data = {
            "start": self.current_user,
            "end": target_user.strip()
        }
        return self._send_encrypted_request("find_path", request_data)
    
    def update_profile(self, name: str = None, photo: str = None) -> Dict:
        """Actualizar perfil del usuario"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}
        
        request_data = {
            "username": self.current_user,
            "name": name,
            "photo": photo if photo is not None else ""
        }

        # Filtrar campos None
        request_data = {k: v for k, v in request_data.items() if v is not None}
        
        response = self._send_encrypted_request("update_profile", request_data)
        
        if response.get("status") == "success":
            self.user_data = response.get("user_data", {})
        
        return response
    
    def change_password(self, old_password: str, new_password: str) -> Dict:
        """Cambiar contraseña del usuario"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}
        
        request_data = {
            "username": self.current_user,
            "old_password": old_password,
            "new_password": new_password
        }
        
        return self._send_encrypted_request("change_password", request_data)
    
    def search_user(self, query: str) -> Dict:
        """Buscar usuario por nombre de usuario"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}
        
        request_data = {
            "query": query,
            "current_user": self.current_user
        }
        return self._send_encrypted_request("search_user", request_data)
    
    def get_stats(self) -> Dict:
        """Obtener estadísticas - LLAMA AL SERVIDOR REAL"""
        return self._send_encrypted_request("get_stats")
    
    def get_suggestions(self) -> Dict:
        """Obtener sugerencias de amigos - LLAMA AL SERVIDOR REAL"""
        if not self.current_user:
            return {"status": "error", "message": "No hay usuario autenticado"}
        
        request_data = {
            "username": self.current_user
        }
        return self._send_encrypted_request("get_suggestions", request_data)
    
    def disconnect(self):
        """Desconectar"""
        self.connected = False
        if self.client_socket:
            self.client_socket.close()
            self.client_socket = None
        print("Desconectado del servidor")
    
    def __del__(self):
        """Destructor - cierra conexión"""
        self.disconnect()