# run_server.py - Archivo principal para ejecutar el servidor con GUI
import sys
import threading
from PyQt6.QtWidgets import QApplication, QSizePolicy
from PyQt6.QtCore import QTimer
from serverTCP import SocialtecServer
from gui_server import ServerWindow

def main():
    # Crear instancia del servidor
    server = SocialtecServer(host="localhost", port=8080)
    server._load_existing_users()
    
    # Iniciar servidor en un hilo separado
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    
    # Crear aplicación PyQt
    app = QApplication(sys.argv)
    
    # Crear ventana principal del servidor
    window = ServerWindow(server)
    window.show()

    QTimer.singleShot(1000, window.update_graph)
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()