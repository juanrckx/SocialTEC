"""
SocialTEC Client - PyQt6 GUI
Interfaz gráfica inspirada en Facebook con PyQt6
"""
import sys
import base64
import os
from typing import Dict, List

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PIL import Image, ImageQt

from clientTCP import Client
from merge_sort import sort_friends_by_name


class LoginWindow(QMainWindow):
    """Ventana de inicio de sesión"""

    def __init__(self):
        super().__init__()
        self.client = Client()
        self.setup_ui()

    def setup_ui(self):
        """Configurar interfaz de login"""
        self.setWindowTitle("SocialTEC - Iniciar Sesión")
        self.setFixedSize(900, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f2f5;
            }
        """)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Panel izquierdo (imagen/logo)
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background-color: #1877f2;
                border-radius: 0px;
            }
        """)
        left_panel.setFixedWidth(400)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo
        logo_label = QLabel("SocialTEC")
        logo_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 48px;
                font-weight: bold;
                font-family: 'Arial';
            }
        """)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(logo_label)

        # Subtítulo
        subtitle = QLabel("Conecta con tus compañeros\nComparte experiencias\nConstruye tu red profesional")
        subtitle.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-family: 'Arial';
                padding: 20px;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        left_layout.addWidget(subtitle)

        # Panel derecho (formulario)
        right_panel = QFrame()
        right_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 0px;
            }
        """)

        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.setSpacing(20)

        # Título del formulario
        form_title = QLabel("Iniciar Sesión")
        form_title.setStyleSheet("""
            QLabel {
                color: #1c1e21;
                font-size: 28px;
                font-weight: bold;
                font-family: 'Arial';
            }
        """)
        form_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(form_title)

        # Campos del formulario
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)

        # Campo usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 1px solid #dddfe2;
                border-radius: 6px;
                font-family: 'Arial';
                color: #1c1e21;
                background-color: #f5f6f7;
            }
            QLineEdit:focus {
                border: 1px solid #1877f2;
            }
            QLineEdit::placeholder {
                color: #8d949e;
            }
        """)
        self.username_input.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        form_layout.addWidget(self.username_input)

        # Campo contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 1px solid #dddfe2;
                border-radius: 6px;
                font-family: 'Arial';
                color: #1c1e21;
                background-color: #f5f6f7;
            }
            QLineEdit:focus {
                border: 1px solid #1877f2;
            }
            QLineEdit::placeholder {
                color: #8d949e;
            }
        """)
        self.password_input.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        form_layout.addWidget(self.password_input)

        # Botón iniciar sesión
        login_btn = QPushButton("Iniciar Sesión")
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #1877f2;
                color: white;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #166fe5;
            }
            QPushButton:pressed {
                background-color: #1461c9;
            }
        """)
        login_btn.clicked.connect(self.login)
        form_layout.addWidget(login_btn)

        right_layout.addWidget(form_widget)

        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background-color: #dadde1;")
        separator.setFixedHeight(1)
        right_layout.addWidget(separator)

        # Botón crear cuenta
        create_account_btn = QPushButton("Crear Nueva Cuenta")
        create_account_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        create_account_btn.setStyleSheet("""
            QPushButton {
                background-color: #42b72a;
                color: white;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #36a420;
            }
            QPushButton:pressed {
                background-color: #2b9217;
            }
        """)
        create_account_btn.clicked.connect(self.show_register)
        right_layout.addWidget(create_account_btn)

        # Agregar paneles al layout principal
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)

    def login(self):
        """Manejar inicio de sesión CORREGIDO"""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Por favor ingresa usuario y contraseña")
            return
        
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        
        try:
            # EL CLIENTE SE CONECTA AUTOMÁTICAMENTE
            response = self.client.login(username, password)
            
            if response.get('status') == 'success':
                QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso")
                self.main_window = MainWindow(self.client, username, response.get('user_data', {}))
                self.main_window.show()
                self.close()
            else:
                error_msg = response.get('message', 'Error desconocido')
                QMessageBox.critical(self, "Error", f"Inicio de sesión fallido:\n{error_msg}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Excepción: {str(e)}")
        finally:
            QApplication.restoreOverrideCursor()

    def show_register(self):
        """Mostrar ventana de registro"""
        self.register_window = RegisterWindow(self.client)
        self.register_window.show()

class RegisterWindow(QMainWindow):
    """Ventana de registro de nuevo usuario"""

    def __init__(self, client=None):
        super().__init__()
        self.client = client if client else Client()
        self.photo_data = None
        self.setup_ui()

    def setup_ui(self):
        """Configurar interfaz de registro"""
        self.setWindowTitle("SocialTEC - Crear Cuenta")
        self.setFixedSize(800, 700)

        # Widget central con scroll
        scroll_widget = QScrollArea()
        scroll_widget.setWidgetResizable(True)
        scroll_widget.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f0f2f5;
            }
        """)

        central_widget = QWidget()
        scroll_widget.setWidget(central_widget)
        self.setCentralWidget(scroll_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Header
        header = QLabel("Crear Nueva Cuenta")
        header.setStyleSheet("""
            QLabel {
                color: #1c1e21;
                font-size: 32px;
                font-weight: bold;
                font-family: 'Arial';
                padding: 30px;
                background-color: white;
            }
        """)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header)

        # Formulario
        form_widget = QWidget()
        form_widget.setStyleSheet("""
            QWidget {
                background-color: white;
            }
        """)

        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(40, 40, 40, 40)

        # Campos
        fields = [
            ("Nombre Completo", "name"),
            ("Usuario", "username"),
            ("Contraseña", "password"),
            ("Confirmar Contraseña", "confirm_password")
        ]

        self.inputs = {}
        for label_text, field_name in fields:
            # Label
            label = QLabel(label_text)
            label.setStyleSheet("""
                QLabel {
                    color: #1c1e21;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Arial';
                }
            """)
            form_layout.addWidget(label)

            # Input
            input_widget = QLineEdit()

            if "Contraseña" in label_text:
                input_widget.setEchoMode(QLineEdit.EchoMode.Password)

            input_widget.setStyleSheet("""
                QLineEdit {
                    padding: 10px;
                    font-size: 14px;
                    border: 1px solid #dddfe2;
                    border-radius: 6px;
                    font-family: 'Arial';
                    color: #1c1e21;
                    background-color: #f5f6f7;
                }
                QLineEdit:focus {
                    border: 1px solid #1877f2;
                }
                QLineEdit::placeholder {
                    color: #8d949e;
                }
            """)
            input_widget.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
            form_layout.addWidget(input_widget)

            # Guardar referencia
            self.inputs[field_name] = input_widget

        # Foto de perfil
        photo_layout = QHBoxLayout()

        photo_label = QLabel("Foto de Perfil (Opcional)")
        photo_label.setStyleSheet("""
            QLabel {
                color: #1c1e21;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Arial';
            }
        """)
        photo_layout.addWidget(photo_label)

        self.photo_btn = QPushButton("Seleccionar Foto")
        self.photo_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.photo_btn.setStyleSheet("""
            QPushButton {
                background-color: #e4e6eb;
                color: #1c1e21;
                padding: 8px 16px;
                font-size: 14px;
                border: none;
                border-radius: 6px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #d8dadf;
            }
        """)
        self.photo_btn.clicked.connect(self.select_photo)
        photo_layout.addWidget(self.photo_btn)

        self.photo_status = QLabel("No se ha seleccionado foto")
        self.photo_status.setStyleSheet("color: #65676b; font-size: 12px;")
        photo_layout.addWidget(self.photo_status)
        photo_layout.addStretch()

        form_layout.addLayout(photo_layout)

        # Botones
        button_layout = QHBoxLayout()

        # Botón cancelar
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e4e6eb;
                color: #1c1e21;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #d8dadf;
            }
        """)
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)

        # Botón registrar
        register_btn = QPushButton("Crear Cuenta")
        register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        register_btn.setStyleSheet("""
            QPushButton {
                background-color: #42b72a;
                color: white;
                padding: 12px 24px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #36a420;
            }
            QPushButton:pressed {
                background-color: #2b9217;
            }
        """)
        register_btn.clicked.connect(self.register)
        button_layout.addWidget(register_btn)

        form_layout.addLayout(button_layout)

        main_layout.addWidget(form_widget)

    def select_photo(self):
        """Seleccionar foto de perfil - CON LÍMITE DE TAMAÑO"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Foto de Perfil",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.gif *.bmp);;Todos los archivos (*)"
        )
        
        if file_path:
            try:
                # VERIFICAR TAMAÑO MÁXIMO (100KB = 102400 bytes)
                file_size = os.path.getsize(file_path)
                MAX_SIZE = 100 * 1024  # 100KB
                
                if file_size > MAX_SIZE:
                    QMessageBox.warning(
                        self, 
                        "Imagen demasiado grande",
                        f"La imagen no debe superar los 100KB.\n"
                        f"Tamaño actual: {file_size/1024:.1f}KB\n\n"
                        f"Recomendación: Usa una imagen más pequeña o comprímela."
                    )
                    self.photo_data = None
                    self.photo_status.setText("Imagen muy grande - selecciona otra")
                    return
                
                # Leer y convertir a base64
                with open(file_path, 'rb') as f:
                    self.photo_data = base64.b64encode(f.read()).decode('utf-8')
                
                # Actualizar estado
                file_name = os.path.basename(file_path)
                self.photo_status.setText(f"{file_name} ({file_size/1024:.1f}KB)")
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo cargar la imagen: {str(e)}")
                self.photo_data = None

        if file_path:
            try:
                # Leer y convertir a base64
                with open(file_path, 'rb') as f:
                    self.photo_data = base64.b64encode(f.read()).decode('utf-8')

                # Actualizar estado
                file_name = os.path.basename(file_path)
                self.photo_status.setText(f"Foto seleccionada: {file_name}")

            except Exception as e:
                QMessageBox.warning(self, "Error", f"No se pudo cargar la imagen: {str(e)}")

    def register(self):
        """Manejar registro de nuevo usuario"""
        # Obtener datos del formulario
        name = self.inputs['name'].text().strip()
        username = self.inputs['username'].text().strip()
        password = self.inputs['password'].text()
        confirm_password = self.inputs['confirm_password'].text()

        # Validaciones
        if not all([name, username, password, confirm_password]):
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Error", "La contraseña debe tener al menos 6 caracteres")
            return

        if len(username) < 3:
            QMessageBox.warning(self, "Error", "El usuario debe tener al menos 3 caracteres")
            return

        # Mostrar indicador de carga
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        
        try:
            # EL CLIENTE SE CONECTA AUTOMÁTICAMENTE
            response = self.client.register(username, password, name, self.photo_data or "")
            if response.get('status') == 'success':
                QMessageBox.information(self, "Éxito", "Cuenta creada exitosamente")
                self.close()
            else:
                error_msg = response.get('message', 'Error desconocido')
                QMessageBox.critical(self, "Error", f"Registro fallido:\n{error_msg}")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Excepción: {str(e)}")
        finally:
            QApplication.restoreOverrideCursor()


class MainWindow(QMainWindow):
    """Ventana principal de la aplicación"""

    def __init__(self, client: Client, username: str, user_data: Dict):
        super().__init__()
        self.client = client
        self.username = username
        self.user_data = user_data
        self.current_content = None
        self.editin_photo_data = None

        self.setup_ui()
        self.load_user_friends()

    def setup_ui(self):
        """Configurar interfaz principal"""
        self.setWindowTitle(f"SocialTEC - {self.username}")
        self.setGeometry(100, 100, 1200, 800)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Panel lateral izquierdo
        self.setup_left_panel(main_layout)

        # Panel central
        self.setup_center_panel(main_layout)

        # Panel lateral derecho (opcional)
        self.setup_right_panel(main_layout)

    def setup_left_panel(self, main_layout: QHBoxLayout):
        """Configurar panel lateral izquierdo (navegación)"""
        left_panel = QFrame()
        left_panel.setFixedWidth(280)
        left_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-right: 1px solid #dddfe2;
            }
        """)

        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Perfil del usuario
        profile_frame = self.create_profile_frame()
        left_layout.addWidget(profile_frame)

        # Navegación
        nav_frame = QFrame()
        nav_frame.setStyleSheet("QFrame { background-color: white; }")

        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setSpacing(2)

        # Botones de navegación
        nav_items = [
            ("Mis Amigos", self.show_friends),
            ("Buscar Usuarios", self.show_search),
            ("Estadísticas", self.show_stats),
            ("Ver Conexiones", self.show_connections),
            ("Configuración", self.show_settings)
        ]

        for icon_text, callback in nav_items:
            btn = QPushButton(icon_text)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding: 12px 20px;
                    font-size: 15px;
                    color: #1c1e21;
                    background-color: white;
                    border: none;
                    font-family: 'Arial';
                }
                QPushButton:hover {
                    background-color: #f0f2f5;
                }
            """)
            btn.clicked.connect(callback)
            nav_layout.addWidget(btn)

        left_layout.addWidget(nav_frame)
        left_layout.addStretch()

        main_layout.addWidget(left_panel)

    def create_profile_frame(self) -> QFrame:
        """Crear frame del perfil del usuario - VERSIÓN CORREGIDA"""
        profile_frame = QFrame()
        profile_frame.setFixedHeight(200)
        profile_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 1px solid #dddfe2;
            }
        """)

        profile_layout = QVBoxLayout(profile_frame)
        profile_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Foto de perfil
        photo_label = QLabel()
        photo_label.setFixedSize(80, 80)

        if self.user_data.get('photo'):
            try:
                # Método directo sin PIL
                import io
                from PyQt6.QtGui import QImage, QPixmap
                
                photo_bytes = base64.b64decode(self.user_data['photo'])
                
                # Crear QImage desde bytes
                image = QImage()
                image.loadFromData(photo_bytes)
                
                if not image.isNull():
                    # Escalar manteniendo proporción
                    pixmap = QPixmap.fromImage(image)
                    pixmap = pixmap.scaled(80, 80, 
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation)
                    
                    # Crear imagen circular
                    circular_pixmap = QPixmap(80, 80)
                    circular_pixmap.fill(Qt.GlobalColor.transparent)
                    
                    painter = QPainter(circular_pixmap)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
                    
                    # Crear ruta circular
                    path = QPainterPath()
                    path.addEllipse(0, 0, 80, 80)
                    painter.setClipPath(path)
                    
                    # Dibujar pixmap
                    painter.drawPixmap(0, 0, pixmap)
                    painter.end()
                    
                    photo_label.setPixmap(circular_pixmap)
                else:
                    raise Exception("Imagen inválida")
                    
            except Exception as e:
                print(f"Error cargando foto: {e}")
                # Mostrar ícono como fallback
                photo_label.setText("")
                photo_label.setStyleSheet("""
                    QLabel {
                        font-size: 40px;
                        border: 2px solid #1877f2;
                        border-radius: 40px;
                        background-color: #f0f2f5;
                    }
                """)
                photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            photo_label.setText("")
            photo_label.setStyleSheet("""
                QLabel {
                    font-size: 40px;
                    border: 2px solid #1877f2;
                    border-radius: 40px;
                    background-color: #f0f2f5;
                }
            """)
            photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        profile_layout.addWidget(photo_label)

        # Nombre
        actual_name = self.user_data.get('name', self.username)
        name_label = QLabel(actual_name)
        name_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1c1e21;
                font-family: 'Arial';
            }
        """)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_layout.addWidget(name_label)

        # Username
        username_label = QLabel(f"@{self.username}")
        username_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #65676b;
                font-family: 'Arial';
            }
        """)
        username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        profile_layout.addWidget(username_label)

        # Botón editar perfil
        edit_btn = QPushButton("Editar Perfil")
        edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_btn.setFixedWidth(120)
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #e4e6eb;
                color: #1c1e21;
                padding: 6px 12px;
                font-size: 14px;
                border: none;
                border-radius: 6px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #d8dadf;
            }
        """)
        edit_btn.clicked.connect(self.edit_profile)
        profile_layout.addWidget(edit_btn)

        return profile_frame

    def setup_center_panel(self, main_layout: QHBoxLayout):
        """Configurar panel central (contenido principal)"""
        self.center_panel = QScrollArea()
        self.center_panel.setWidgetResizable(True)
        self.center_panel.setStyleSheet("""
            QScrollArea {
                background-color: #f0f2f5;
                border: none;
            }
        """)

        self.center_content = QWidget()
        self.center_content.setStyleSheet("background-color: #f0f2f5;")
        self.center_layout = QVBoxLayout(self.center_content)

        self.center_panel.setWidget(self.center_content)
        main_layout.addWidget(self.center_panel, 1)

    def setup_right_panel(self, main_layout: QHBoxLayout):
        """Configurar panel lateral derecho"""
        right_panel = QFrame()
        right_panel.setFixedWidth(300)
        right_panel.setStyleSheet("""
            QFrame {
                background-color: white;
                border-left: 1px solid #dddfe2;
            }
        """)

        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        right_layout.setContentsMargins(5, 5, 5, 5)

        # Título
        title = QLabel("Sugerencias")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #1c1e21;
                font-family: 'Arial';
            }
        """)
        right_layout.addWidget(title)

        # Botón para refrescar sugerencias
        refresh_btn = QPushButton("Actualizar Sugerencias")
        refresh_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #e4e6eb;
                color: #1c1e21;
                padding: 8px;
                font-size: 12px;
                border: none;
                border-radius: 6px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #d8dadf;
            }
        """)
        refresh_btn.clicked.connect(self.load_suggestions)
        right_layout.addWidget(refresh_btn)

        # Scroll area para sugerencias
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedHeight(500)  # Altura fija
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
        """)

        # Widget para sugerencias
        self.suggestions_widget = QWidget()
        self.suggestions_layout = QVBoxLayout(self.suggestions_widget)
        self.suggestions_layout.setSpacing(10)
        self.suggestions_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        scroll_area.setWidget(self.suggestions_widget)
        right_layout.addWidget(scroll_area)

        # Cargar sugerencias inicialmente
        self.load_suggestions()

        # Botón cerrar sesión
        logout_btn = QPushButton("Cerrar Sesión")
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        right_layout.addWidget(logout_btn)

        main_layout.addWidget(right_panel)

    def load_suggestions(self):
        """Cargar sugerencias de amigos desde el servidor"""
        # Limpiar sugerencias anteriores
        while self.suggestions_layout.count():
            item = self.suggestions_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not self.client.current_user:
            return

        # Obtener sugerencias del servidor
        response = self.client.get_suggestions()

        if response.get("status") != "success":
            error_label = QLabel("No se pudieron cargar las sugerencias")
            error_label.setStyleSheet("color: #65676b; font-size: 14px; padding: 10px;")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.suggestions_layout.addWidget(error_label)
            return

        suggestions = response.get("suggestions", [])

        if not suggestions:
            no_suggestions = QLabel("No hay sugerencias disponibles.\n\n¡Agrega más amigos para recibir sugerencias!")
            no_suggestions.setStyleSheet("""
                QLabel {
                    color: #65676b;
                    font-size: 14px;
                    padding: 20px;
                    font-family: 'Arial';
                }
            """)
            no_suggestions.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_suggestions.setWordWrap(True)
            self.suggestions_layout.addWidget(no_suggestions)
            return

        for suggestion in suggestions:
            suggestion_card = self.create_suggestion_card(suggestion)
            self.suggestions_layout.addWidget(suggestion_card)

        # Espacio al final
        self.suggestions_layout.addStretch()

    def create_suggestion_card(self, suggestion: Dict) -> QFrame:
        """Crear tarjeta para una sugerencia de amigo"""
        card = QFrame()
        card.setFixedHeight(120)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dddfe2;
                border-radius: 8px;
                padding: 10px;
            }
            QFrame:hover {
                border: 1px solid #1877f2;
                background-color: #f7f9fa;
            }
        """)

        card_layout = QHBoxLayout(card)
        card_layout.setSpacing(10)

        # Foto de perfil
        photo_label = QLabel()
        photo_label.setFixedSize(50, 50)

        if suggestion.get('photo'):
            try:
                import io
                photo_bytes = base64.b64decode(suggestion['photo'])
                image = QImage()
                if image.loadFromData(photo_bytes):
                    pixmap = QPixmap.fromImage(image)
                    pixmap = pixmap.scaled(50, 50, 
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation)
                    
                    # Hacerla circular
                    circular_pixmap = QPixmap(50, 50)
                    circular_pixmap.fill(Qt.GlobalColor.transparent)
                    
                    painter = QPainter(circular_pixmap)
                    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
                    path = QPainterPath()
                    path.addEllipse(0, 0, 50, 50)
                    painter.setClipPath(path)
                    painter.drawPixmap(0, 0, pixmap)
                    painter.end()
                    
                    photo_label.setPixmap(circular_pixmap)
            except Exception as e:
                print(f"Error cargando foto de sugerencia: {e}")
                photo_label.setText("")
                photo_label.setStyleSheet("font-size: 25px;")
                photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            photo_label.setText("")
            photo_label.setStyleSheet("font-size: 25px;")
            photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout.addWidget(photo_label)

        # Información del usuario
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(5)

        # Nombre
        name_label = QLabel(suggestion['name'])
        name_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #1c1e21;
                font-family: 'Arial';
            }
        """)
        info_layout.addWidget(name_label)

        # Username
        username_label = QLabel(f"@{suggestion['username']}")
        username_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #65676b;
                font-family: 'Arial';
            }
        """)
        info_layout.addWidget(username_label)

        # Amigos en común
        common_label = QLabel(f"Amigos en común: {suggestion.get('common_friends', 0)}")
        common_label.setStyleSheet("""
            QLabel {
                font-size: 11px;
                color: #42b72a;
                font-family: 'Arial';
            }
        """)
        info_layout.addWidget(common_label)

        card_layout.addWidget(info_widget, 1)

        # Botón agregar
        add_btn = QPushButton("+")
        add_btn.setFixedSize(40, 40)
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setToolTip(f"Agregar a {suggestion['name']} como amigo")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #42b72a;
                color: white;
                font-size: 20px;
                font-weight: bold;
                border: none;
                border-radius: 20px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #36a420;
            }
            QPushButton:pressed {
                background-color: #2b9217;
            }
        """)
        add_btn.clicked.connect(lambda: self.add_suggested_friend(suggestion['username']))
        card_layout.addWidget(add_btn)

        return card

    def add_suggested_friend(self, username: str):
        """Agregar un amigo desde las sugerencias"""
        reply = QMessageBox.question(
            self,
            "Agregar Amigo",
            f"¿Quieres agregar a {username} como amigo?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            response = self.client.add_friend(username)

            if response.get('status') == 'success':
                QMessageBox.information(self, "Éxito", f"¡Ahora eres amigo de {username}!")
                # Recargar sugerencias y lista de amigos
                self.load_suggestions()
                self.show_friends()  # Actualizar vista de amigos
            else:
                QMessageBox.critical(self, "Error", 
                                response.get('message', 'No se pudo agregar amigo'))

    def load_user_friends(self):
        """Cargar amigos del usuario desde el servidor"""
        if not self.client.current_user:
            return
        
        response = self.client._send_encrypted_request("get_friends", {"username": self.username})
        
        if response.get("status") == "success":
            self.user_data["friends"] = response.get("friends", [])
        else:
            self.user_data["friends"] = []

    def clear_center_content(self):
        """Limpiar contenido del panel central"""
        while self.center_layout.count():
            item = self.center_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_friends(self):
        """Mostrar lista de amigos REAL desde el servidor"""
        self.clear_center_content()

        # Título
        title = QLabel("Mis Amigos")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1c1e21;
                font-family: 'Arial';
                padding: 20px;
            }
        """)
        self.center_layout.addWidget(title)

        # Obtener amigos del servidor
        response = self.client._send_encrypted_request("get_friends", {"username": self.username})

        if response.get("status") != "success":
            error_label = QLabel(f"Error al cargar amigos: {response.get('message', 'Error desconocido')}")
            error_label.setStyleSheet("color: #ff4444; font-size: 16px; padding: 40px;")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.center_layout.addWidget(error_label)
            return

        friends_data = response.get("friends", [])

        if not friends_data:
            no_friends = QLabel("Aún no tienes amigos. ¡Busca y agrega amigos!")
            no_friends.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    color: #65676b;
                    font-family: 'Arial';
                    padding: 40px;
                }
            """)
            no_friends.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.center_layout.addWidget(no_friends)
            return

        # Ordenar amigos usando Merge Sort
        sorted_friends = sort_friends_by_name(friends_data)

        # Crear grid de amigos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #f0f2f5; }")

        friends_widget = QWidget()
        friends_widget.setStyleSheet("background-color: #f0f2f5;")

        grid_layout = QGridLayout(friends_widget)
        grid_layout.setSpacing(20)
        grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Agregar tarjetas de amigos
        for i, friend in enumerate(sorted_friends):
            row = i // 3
            col = i % 3

            friend_card = self.create_friend_card(friend)
            grid_layout.addWidget(friend_card, row, col)

        scroll_area.setWidget(friends_widget)
        self.center_layout.addWidget(scroll_area)


    def create_friend_card(self, friend: Dict) -> QFrame:
        """Crear tarjeta para mostrar un amigo REAL - VERSIÓN CORREGIDA"""
        card = QFrame()
        card.setFixedSize(220, 280)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dddfe2;
                border-radius: 8px;
            }
            QFrame:hover {
                border: 1px solid #1877f2;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        card_layout.setSpacing(10)

        # Foto
        photo_label = QLabel()
        photo_label.setFixedSize(100, 100)

        if friend.get('photo'):
            try:
                # Método simplificado
                photo_bytes = base64.b64decode(friend['photo'])
                
                # Crear QImage directamente
                image = QImage()
                if image.loadFromData(photo_bytes):
                    pixmap = QPixmap.fromImage(image)
                    pixmap = pixmap.scaled(100, 100, 
                        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                        Qt.TransformationMode.SmoothTransformation)
                    
                    photo_label.setPixmap(pixmap)
                else:
                    raise Exception("No se pudo cargar imagen")
                    
            except Exception as e:
                print(f"Error cargando foto de amigo: {e}")
                photo_label.setText("")
                photo_label.setStyleSheet("font-size: 50px;")
                photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            photo_label.setText("")
            photo_label.setStyleSheet("font-size: 50px;")
            photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        photo_label.setStyleSheet("""
            QLabel {
                border-radius: 50px;
                background-color: #f0f2f5;
            }
        """)
        card_layout.addWidget(photo_label, 0, Qt.AlignmentFlag.AlignHCenter)

        # Nombre
        name_label = QLabel(friend['name'])
        name_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #1c1e21;
                font-family: 'Arial';
            }
        """)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        card_layout.addWidget(name_label)

        # Username
        username_label = QLabel(f"@{friend['username']}")
        username_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #65676b;
                font-family: 'Arial';
            }
        """)
        username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(username_label)

        # Número de amigos
        friend_count = friend.get('friend_count', 0)
        count_label = QLabel(f"Amigos: {friend_count}")
        count_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #8a8d91;
                font-family: 'Arial';
            }
        """)
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(count_label)

        # Botones de acción
        btn_frame = QWidget()
        btn_layout = QHBoxLayout(btn_frame)
        btn_layout.setSpacing(5)

        # Botón eliminar
        remove_btn = QPushButton("Eliminar")
        remove_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                padding: 6px 12px;
                font-size: 12px;
                border: none;
                border-radius: 4px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #e53935;
            }
        """)
        remove_btn.clicked.connect(lambda: self.remove_friend(friend['username']))
        btn_layout.addWidget(remove_btn)

        card_layout.addWidget(btn_frame)
        card_layout.addStretch()

        return card


    def show_search(self):
        """Mostrar búsqueda de usuarios"""
        self.clear_center_content()

        # Título
        title = QLabel("Buscar Usuarios")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1c1e21;
                font-family: 'Arial';
                padding: 20px;
            }
        """)
        self.center_layout.addWidget(title)

        # Barra de búsqueda
        search_frame = QFrame()
        search_frame.setStyleSheet("background-color: white; padding: 20px;")

        search_layout = QHBoxLayout(search_frame)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nombre o usuario...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                font-size: 14px;
                border: 2px solid #1877f2;
                border-radius: 6px;
                font-family: 'Arial';
                color: #1c1e21;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #8d949e;
            }
        """)
        self.search_input.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        search_layout.addWidget(self.search_input, 1)

        search_btn = QPushButton("Buscar")
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #1877f2;
                color: white;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                font-family: 'Arial';
            }
            QPushButton:hover {
                background-color: #166fe5;
            }
        """)
        search_btn.clicked.connect(self.perform_search)
        search_layout.addWidget(search_btn)

        self.center_layout.addWidget(search_frame)

        # Resultados
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout(self.results_widget)
        self.results_layout.setSpacing(10)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.results_widget)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #f0f2f5; }")

        self.center_layout.addWidget(scroll_area, 1)

    def perform_search(self):
        """Realizar búsqueda REAL de usuarios"""
        query = self.search_input.text().strip()

        if not query:
            QMessageBox.warning(self, "Búsqueda", "Ingresa un término de búsqueda")
            return

        # Limpiar resultados anteriores
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Realizar búsqueda REAL
        response = self.client.search_user(query)

        if response.get("status") != "success":
            error_label = QLabel(f"Error en búsqueda: {response.get('message', 'Error desconocido')}")
            error_label.setStyleSheet("color: #ff4444; font-size: 14px; padding: 20px;")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_layout.addWidget(error_label)
            return

        results = response.get("users", [])

        if not results:
            no_results = QLabel("No se encontraron usuarios")
            no_results.setStyleSheet("color: #65676b; font-size: 16px; padding: 40px;")
            no_results.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.results_layout.addWidget(no_results)
            return

        for user in results:
            user_card = self.create_search_result_card(user)
            self.results_layout.addWidget(user_card)

        self.results_layout.addStretch()

    def create_search_result_card(self, user: Dict) -> QFrame:
        """Crear tarjeta para resultado de búsqueda REAL"""
        card = QFrame()
        card.setFixedHeight(100)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dddfe2;
                border-radius: 8px;
            }
        """)

        card_layout = QHBoxLayout(card)
        card_layout.setContentsMargins(15, 10, 15, 10)

        # Foto
        photo_label = QLabel()
        photo_label.setFixedSize(60, 60)
        
        if user.get('photo'):
            try:
                import io
                from PIL import Image
                photo_bytes = base64.b64decode(user['photo'])
                img = Image.open(io.BytesIO(photo_bytes))
                img.thumbnail((60, 60))
                
                from PIL.ImageQt import ImageQt
                qim = ImageQt(img)
                pixmap = QPixmap.fromImage(qim)
                photo_label.setPixmap(pixmap)
            except:
                photo_label.setText("")
                photo_label.setStyleSheet("font-size: 30px;")
                photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            photo_label.setText("")
            photo_label.setStyleSheet("font-size: 30px;")
            photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        photo_label.setStyleSheet("""
            QLabel {
                border-radius: 30px;
                background-color: #f0f2f5;
            }
        """)
        card_layout.addWidget(photo_label)

        # Información del usuario
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(5)

        name_label = QLabel(user['name'])
        name_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1c1e21;")
        info_layout.addWidget(name_label)

        username_label = QLabel(f"@{user['username']} • {user.get('friend_count', 0)} amigos")
        username_label.setStyleSheet("font-size: 14px; color: #65676b;")
        info_layout.addWidget(username_label)

        card_layout.addWidget(info_widget, 1)

        # Botones de acción
        btn_frame = QWidget()
        btn_layout = QHBoxLayout(btn_frame)

        if user.get('is_friend', False):
            action_btn = QPushButton("Eliminar")
            action_btn.setStyleSheet("""
                QPushButton {
                    background-color: #ff4444;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 4px;
                    font-family: 'Arial';
                }
                QPushButton:hover {
                    background-color: #e53935;
                }
            """)
            action_btn.clicked.connect(lambda: self.remove_friend(user['username']))
        else:
            action_btn = QPushButton("Agregar")
            action_btn.setStyleSheet("""
                QPushButton {
                    background-color: #42b72a;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 4px;
                    font-family: 'Arial';
                }
                QPushButton:hover {
                    background-color: #36a420;
                }
            """)
            action_btn.clicked.connect(lambda: self.add_friend(user['username']))

        action_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_layout.addWidget(action_btn)

        card_layout.addWidget(btn_frame)

        return card

    def edit_profile(self):
        """Editar perfil - IMPLEMENTACIÓN COMPLETA"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Perfil")
        dialog.setFixedSize(500, 400)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)

        # Título
        title = QLabel("Editar Información de Perfil")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1c1e21;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Campo nombre
        name_layout = QHBoxLayout()
        name_label = QLabel("Nombre:")
        name_label.setFixedWidth(120)
        name_layout.addWidget(name_label)

        self.name_edit = QLineEdit()
        self.name_edit.setText(self.user_data.get('name', self.username))
        self.name_edit.setPlaceholderText("Ingresa tu nombre completo")
        self.name_edit.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 1px solid #dddfe2;
                border-radius: 6px;
                color: #1c1e21;
                background-color: white;
            }
        """)
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)

        # Foto de perfil
        photo_group = QGroupBox("Foto de Perfil")
        photo_layout = QVBoxLayout(photo_group)

        # Vista previa
        preview_layout = QHBoxLayout()
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(100, 100)
        
        # Mostrar foto actual
        if self.user_data.get('photo'):
            try:
                import io
                from PIL import Image
                photo_bytes = base64.b64decode(self.user_data['photo'])
                img = Image.open(io.BytesIO(photo_bytes))
                img.thumbnail((100, 100))
                
                from PIL.ImageQt import ImageQt
                qim = ImageQt(img)
                pixmap = QPixmap.fromImage(qim)
                self.preview_label.setPixmap(pixmap)
            except:
                self.preview_label.setText("")
                self.preview_label.setStyleSheet("font-size: 40px;")
                self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            self.preview_label.setText("")
            self.preview_label.setStyleSheet("font-size: 40px;")
            self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.preview_label.setStyleSheet("""
            QLabel {
                border: 2px solid #1877f2;
                border-radius: 50px;
                background-color: #f0f2f5;
            }
        """)
        preview_layout.addWidget(self.preview_label)
        preview_layout.addStretch()
        photo_layout.addLayout(preview_layout)

        # Botones de foto
        button_layout = QHBoxLayout()
        
        upload_btn = QPushButton("Subir Nueva Foto")
        upload_btn.clicked.connect(lambda: self.upload_profile_photo(dialog))
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #1877f2;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
        """)
        button_layout.addWidget(upload_btn)

        remove_btn = QPushButton("Eliminar Foto")
        remove_btn.clicked.connect(lambda: self.remove_profile_photo())
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
            }
        """)
        button_layout.addWidget(remove_btn)

        photo_layout.addLayout(button_layout)
        layout.addWidget(photo_group)

        # Botones de acción
        button_box = QDialogButtonBox()
        save_btn = QPushButton("Guardar Cambios")
        save_btn.clicked.connect(lambda: self.save_profile_changes(dialog))
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(dialog.reject)

        button_box.addButton(save_btn, QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.addButton(cancel_btn, QDialogButtonBox.ButtonRole.RejectRole)

        layout.addWidget(button_box)
        dialog.exec()

    def upload_profile_photo(self, dialog):
        """Subir nueva foto de perfil"""
        file_path, _ = QFileDialog.getOpenFileName(
            dialog,
            "Seleccionar Foto de Perfil",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.gif *.bmp);;Todos los archivos (*)"
        )
        
        if file_path:
            try:
                import os
                # Verificar tamaño (máximo 100KB)
                file_size = os.path.getsize(file_path)
                MAX_SIZE = 100 * 1024
                
                if file_size > MAX_SIZE:
                    QMessageBox.warning(
                        dialog,
                        "Imagen muy grande",
                        f"La imagen no debe superar los 100KB.\n"
                        f"Tamaño actual: {file_size/1024:.1f}KB"
                    )
                    return
                
                # Leer y convertir a base64
                with open(file_path, 'rb') as f:
                    self.editing_photo_data = base64.b64encode(f.read()).decode('utf-8')
                
                # Actualizar vista previa
                from PIL import Image
                import io
                photo_bytes = base64.b64decode(self.editing_photo_data)
                img = Image.open(io.BytesIO(photo_bytes))
                img.thumbnail((100, 100))
                
                from PIL.ImageQt import ImageQt
                qim = ImageQt(img)
                pixmap = QPixmap.fromImage(qim)
                self.preview_label.setPixmap(pixmap)
                
            except Exception as e:
                QMessageBox.warning(dialog, "Error", f"No se pudo cargar la imagen: {str(e)}")

    def remove_profile_photo(self):
        """Eliminar foto de perfil"""
        self.editing_photo_data = ""  # String vacío para eliminar foto
        self.preview_label.setText("")
        self.preview_label.setPixmap(QPixmap())
        self.preview_label.setStyleSheet("""
            QLabel {
                border: 2px solid #1877f2;
                border-radius: 50px;
                background-color: #f0f2f5;
                font-size: 40px;
            }
        """)
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def save_profile_changes(self, dialog):
        """Guardar cambios del perfil en el servidor"""
        new_name = self.name_edit.text().strip()
        
        if not new_name:
            QMessageBox.warning(dialog, "Error", "El nombre no puede estar vacío")
            return
        
        # Determinar qué actualizar
        update_data = {"name": new_name}
        
        if hasattr(self, 'editing_photo_data') and self.editing_photo_data is not None:
            update_data["photo"] = self.editing_photo_data
        
        # Enviar al servidor
        response = self.client.update_profile(**update_data)
        
        if response.get("status") == "success":
            # Actualizar datos locales
            self.user_data['name'] = new_name
            if 'photo' in update_data:
                self.user_data['photo'] = update_data['photo']
            
            QMessageBox.information(dialog, "Éxito", "Perfil actualizado correctamente")
            
            # Actualizar interfaz
            self.update_profile_display()
            dialog.accept()
        else:
            QMessageBox.critical(dialog, "Error", 
                               response.get("message", "Error al actualizar el perfil"))

    def update_profile_display(self):
        """Actualizar la visualización del perfil en el panel izquierdo"""
        # Esta función actualizaría los elementos de la UI con los nuevos datos
        # Dado que la interfaz es estática, podríamos recargar ciertos componentes
        # o simplemente mostrar un mensaje de éxito
        
        # Para una implementación más completa, podrías emitir una señal
        # pero por ahora, solo cerramos el diálogo
        pass

    def change_password(self):
        """Cambiar contraseña - IMPLEMENTACIÓN COMPLETA"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Cambiar Contraseña")
        dialog.setFixedSize(400, 300)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)

        # Título
        title = QLabel("Cambiar Contraseña")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1c1e21;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Contraseña actual
        old_pass_group = QGroupBox("Contraseña Actual")
        old_pass_layout = QVBoxLayout(old_pass_group)
        
        self.old_pass_input = QLineEdit()
        self.old_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.old_pass_input.setPlaceholderText("Ingresa tu contraseña actual")
        self.old_pass_input.setStyleSheet("padding: 8px; border: 1px solid #dddfe2; border-radius: 4px;")
        old_pass_layout.addWidget(self.old_pass_input)
        layout.addWidget(old_pass_group)

        # Nueva contraseña
        new_pass_group = QGroupBox("Nueva Contraseña")
        new_pass_layout = QVBoxLayout(new_pass_group)
        
        self.new_pass_input = QLineEdit()
        self.new_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_pass_input.setPlaceholderText("Ingresa tu nueva contraseña")
        self.new_pass_input.setStyleSheet("padding: 8px; border: 1px solid #dddfe2; border-radius: 4px;")
        new_pass_layout.addWidget(self.new_pass_input)
        layout.addWidget(new_pass_group)

        # Confirmar nueva contraseña
        confirm_pass_group = QGroupBox("Confirmar Nueva Contraseña")
        confirm_pass_layout = QVBoxLayout(confirm_pass_group)
        
        self.confirm_pass_input = QLineEdit()
        self.confirm_pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_pass_input.setPlaceholderText("Confirma tu nueva contraseña")
        self.confirm_pass_input.setStyleSheet("padding: 8px; border: 1px solid #dddfe2; border-radius: 4px;")
        confirm_pass_layout.addWidget(self.confirm_pass_input)
        layout.addWidget(confirm_pass_group)

        # Botones
        button_box = QDialogButtonBox()
        change_btn = QPushButton("Cambiar Contraseña")
        change_btn.clicked.connect(lambda: self.save_password_change(dialog))
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(dialog.reject)

        button_box.addButton(change_btn, QDialogButtonBox.ButtonRole.AcceptRole)
        button_box.addButton(cancel_btn, QDialogButtonBox.ButtonRole.RejectRole)

        layout.addWidget(button_box)
        dialog.exec()

    def save_password_change(self, dialog):
        """Guardar el cambio de contraseña en el servidor"""
        old_password = self.old_pass_input.text()
        new_password = self.new_pass_input.text()
        confirm_password = self.confirm_pass_input.text()

        # Validaciones
        if not old_password or not new_password or not confirm_password:
            QMessageBox.warning(dialog, "Error", "Todos los campos son obligatorios")
            return

        if new_password != confirm_password:
            QMessageBox.warning(dialog, "Error", "Las nuevas contraseñas no coinciden")
            return

        if len(new_password) < 6:
            QMessageBox.warning(dialog, "Error", "La nueva contraseña debe tener al menos 6 caracteres")
            return

        if old_password == new_password:
            QMessageBox.warning(dialog, "Error", "La nueva contraseña debe ser diferente a la actual")
            return

        # Enviar al servidor
        response = self.client.change_password(old_password, new_password)

        if response.get("status") == "success":
            QMessageBox.information(dialog, "Éxito", "Contraseña cambiada correctamente")
            dialog.accept()
        else:
            QMessageBox.critical(dialog, "Error", 
                               response.get("message", "Error al cambiar la contraseña"))



    def show_stats(self):
        """Mostrar estadísticas"""
        self.clear_center_content()

        # Título
        title = QLabel("Estadísticas de la Red")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1c1e21;
                font-family: 'Arial';
                padding: 20px;
            }
        """)
        self.center_layout.addWidget(title)

        # Obtener estadísticas del servidor
        response = self.client.get_stats()

        if response.get('status') != 'success':
            error_label = QLabel("No se pudieron cargar las estadísticas")
            error_label.setStyleSheet("color: #ff4444; font-size: 16px; padding: 40px;")
            error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.center_layout.addWidget(error_label)
            return

        stats = response.get('stats', {})

        # Mostrar estadísticas
        stats_widget = QWidget()
        stats_widget.setStyleSheet("background-color: white; border-radius: 8px;")

        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.setSpacing(20)
        stats_layout.setContentsMargins(30, 30, 30, 30)

        # Usuario con más amigos
        if stats.get('max'):
            max_user, max_count = stats['max']
            max_frame = QFrame()
            max_layout = QHBoxLayout(max_frame)

            max_label = QLabel("Usuario con más amigos:")
            max_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            max_layout.addWidget(max_label)

            max_info = QLabel(f"{max_user} ({max_count} amigos)")
            max_info.setStyleSheet("font-size: 16px; color: #1877f2;")
            max_layout.addWidget(max_info)
            max_layout.addStretch()

            stats_layout.addWidget(max_frame)

        # Usuario con menos amigos
        if stats.get('min'):
            min_user, min_count = stats['min']
            min_frame = QFrame()
            min_layout = QHBoxLayout(min_frame)

            min_label = QLabel("Usuario con menos amigos:")
            min_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            min_layout.addWidget(min_label)

            min_info = QLabel(f"{min_user} ({min_count} amigos)")
            min_info.setStyleSheet("font-size: 16px; color: #65676b;")
            min_layout.addWidget(min_info)
            min_layout.addStretch()

            stats_layout.addWidget(min_frame)

        # Promedio
        if 'avg' in stats:
            avg_frame = QFrame()
            avg_layout = QHBoxLayout(avg_frame)

            avg_label = QLabel("Promedio de amigos por usuario:")
            avg_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            avg_layout.addWidget(avg_label)

            avg_info = QLabel(f"{stats['avg']:.2f}")
            avg_info.setStyleSheet("font-size: 16px; color: #42b72a;")
            avg_layout.addWidget(avg_info)
            avg_layout.addStretch()

            stats_layout.addWidget(avg_frame)

        self.center_layout.addWidget(stats_widget)

    def show_connections(self):
        """Mostrar conexiones entre usuarios"""
        self.clear_center_content()

        # Título
        title = QLabel("Buscar Conexiones entre Usuarios")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1c1e21;
                font-family: 'Arial';
                padding: 20px;
            }
        """)
        self.center_layout.addWidget(title)

        # Formulario para buscar conexiones
        form_widget = QWidget()
        form_widget.setStyleSheet("background-color: white; padding: 20px; border-radius: 8px;")

        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(15)

        # Campo usuario destino
        user_frame = QWidget()
        user_layout = QHBoxLayout(user_frame)

        user_label = QLabel("Usuario destino:")
        user_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        user_layout.addWidget(user_label)

        self.target_user_input = QLineEdit()
        self.target_user_input.setPlaceholderText("Ingresa el nombre de usuario")
        self.target_user_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #dddfe2;
                border-radius: 4px;
                color: #1c1e21;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #8d949e;
            }
        """)
        self.target_user_input.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        user_layout.addWidget(self.target_user_input, 1)

        form_layout.addWidget(user_frame)

        # Botón buscar conexión
        find_btn = QPushButton("Buscar Conexión")
        find_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        find_btn.setStyleSheet("""
            QPushButton {
                background-color: #1877f2;
                color: white;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border: none;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #166fe5;
            }
        """)
        find_btn.clicked.connect(self.find_connection)
        form_layout.addWidget(find_btn)

        self.center_layout.addWidget(form_widget)

        # Resultado
        self.connection_result = QLabel()
        self.connection_result.setStyleSheet("""
            QLabel {
                font-size: 16px;
                padding: 20px;
                background-color: white;
                border-radius: 8px;
                margin-top: 20px;
            }
        """)
        self.connection_result.setWordWrap(True)
        self.center_layout.addWidget(self.connection_result)
        self.center_layout.addStretch()

    def find_connection(self):
        """Buscar conexión entre usuarios"""
        target_user = self.target_user_input.text().strip()

        if not target_user:
            QMessageBox.warning(self, "Error", "Ingresa un usuario destino")
            return

        if target_user == self.username:
            QMessageBox.warning(self, "Error", "No puedes buscar conexión contigo mismo")
            return

        # Buscar conexión
        response = self.client.find_path(target_user)

        if response.get('status') == 'success':
            path = response.get('path', [])
            path_text = " → ".join(path)
            self.connection_result.setText(f"Conexión encontrada:\n\n{path_text}\n\n Distancia: {len(path)-1} saltos")
            self.connection_result.setStyleSheet("color: #42b72a; font-size: 16px; padding: 20px; background-color: white;")
        else:
            self.connection_result.setText(f"No existe conexión entre {self.username} y {target_user}")
            self.connection_result.setStyleSheet("color: #ff4444; font-size: 16px; padding: 20px; background-color: white;")

    def show_settings(self):
        """Mostrar configuración"""
        self.clear_center_content()

        # Título
        title = QLabel("Configuración")
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1c1e21;
                font-family: 'Arial';
                padding: 20px;
            }
        """)
        self.center_layout.addWidget(title)

        # Contenido de configuración
        settings_widget = QWidget()
        settings_widget.setStyleSheet("background-color: white; border-radius: 8px;")

        settings_layout = QVBoxLayout(settings_widget)
        settings_layout.setSpacing(20)
        settings_layout.setContentsMargins(30, 30, 30, 30)

        # Configuración de cuenta
        account_group = QGroupBox("Cuenta")
        account_layout = QVBoxLayout(account_group)

        # Cambiar contraseña
        change_pass_btn = QPushButton("Cambiar Contraseña")
        change_pass_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        change_pass_btn.clicked.connect(self.change_password)
        account_layout.addWidget(change_pass_btn)

        # Eliminar cuenta
        delete_account_btn = QPushButton("Eliminar Cuenta")
        delete_account_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_account_btn.setStyleSheet("background-color: #ff4444; color: white;")
        delete_account_btn.clicked.connect(self.delete_account)
        account_layout.addWidget(delete_account_btn)

        settings_layout.addWidget(account_group)

        # Configuración de privacidad
        privacy_group = QGroupBox("Privacidad")
        privacy_layout = QVBoxLayout(privacy_group)

        # Quién puede ver tu perfil
        visibility_combo = QComboBox()
        visibility_combo.addItems(["Público", "Solo amigos", "Privado"])
        privacy_layout.addWidget(QLabel("Quién puede ver tu perfil:"))
        privacy_layout.addWidget(visibility_combo)

        settings_layout.addWidget(privacy_group)

        self.center_layout.addWidget(settings_widget)
        self.center_layout.addStretch()

    def view_profile(self, username: str):
        """Ver perfil de usuario"""
        QMessageBox.information(self, "Ver Perfil", f"Ver perfil de {username}")

    def add_friend(self, username: str):
        """Agregar amigo"""
        response = self.client.add_friend(username)

        if response.get('status') == 'success':
            QMessageBox.information(self, "Éxito", f"Ahora eres amigo de {username}")
            # Actualizar vista
            self.show_friends()
        else:
            QMessageBox.critical(self, "Error",
                               response.get('message', 'No se pudo agregar amigo'))

    def remove_friend(self, username: str):
        """Eliminar amigo"""
        reply = QMessageBox.question(
            self, "Confirmar",
            f"¿Eliminar a {username} de tus amigos?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            response = self.client.remove_friend(username)

            if response.get('status') == 'success':
                QMessageBox.information(self, "Éxito", f"Has eliminado a {username} de tus amigos")
                # Actualizar vista
                self.show_friends()
            else:
                QMessageBox.critical(self, "Error",
                                   response.get('message', 'No se pudo eliminar amigo'))

    def delete_account(self):
        """Eliminar cuenta"""
        reply = QMessageBox.critical(
            self, "Confirmar",
            "¿Estás seguro de eliminar tu cuenta? Esta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Cuenta Eliminada",
                                  "Tu cuenta ha sido eliminada (simulación)")

    def logout(self):
        """Cerrar sesión"""
        reply = QMessageBox.question(
            self, "Cerrar Sesión",
            "¿Estás seguro de que quieres cerrar sesión?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.client.disconnect()
            self.close()


def main():
    """Función principal"""
    app = QApplication(sys.argv)

    # Configurar estilo de la aplicación
    app.setStyle("Fusion")

    # Crear y mostrar ventana de login
    login_window = LoginWindow()
    login_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()