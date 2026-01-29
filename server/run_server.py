# run_server.py - Archivo principal para ejecutar el servidor con GUI
import sys
import threading
from PyQt6.QtWidgets import QApplication
from serverTCP import SocialtecServer
from gui_server import ServerWindow

def main():
    # Crear instancia del servidor
    server = SocialtecServer(host="localhost", port=8080)
    
    # Iniciar servidor en un hilo separado
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    
    # Crear aplicación PyQt
    app = QApplication(sys.argv)
    
    # Crear ventana principal del servidor
    window = ServerWindow(server)
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()