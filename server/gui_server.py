# Interfaz gráfica del servidor con PyQt6

############################# IMPORTS #############################
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import networkx as nx
############################# IMPORTS #############################

############################# Clases #############################
from serverTCP import SocialtecServer
from graph_manager import SocialGraph

################# WIDGET PARA MOSTRAR EL GRAFO EN MATPLOTLIB #################
class GraphCanvas(FigureCanvasQTAgg):
    def __init__(self, graph_manager, parent=None, width=10, height=8, dpi= 100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.graph_manager = graph_manager
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.draw_graph()

    def draw_graph(self):
        """Dibuja el grafo - VERSIÓN CORREGIDA"""
        try:
            self.fig.clear()
            ax = self.fig.add_subplot(111)
            ax.clear()
            
            # Obtener el grafo
            G = self.graph_manager.graph
            
            if G.number_of_nodes() == 0:
                ax.text(0.5, 0.5, 'No hay usuarios en la red\n\nAgrega usuarios desde el cliente',
                         ha='center', va='center', fontsize=12, wrap=True)
                ax.set_title("Red Social - Vacía")
                ax.axis('off')
            else:
                try:
                    # Usar un layout más estable para pocos nodos
                    if G.number_of_nodes() < 10:
                        pos = nx.circular_layout(G)
                    else:
                        pos = nx.spring_layout(G, seed=42, k=1, iterations=50)
                    
                    # Dibujar el grafo
                    nx.draw_networkx_nodes(
                        G, pos,
                        node_color='#3498db',
                        node_size=700,
                        alpha=0.8,
                        ax=ax
                    )
                    
                    nx.draw_networkx_edges(
                        G, pos,
                        edge_color='gray',
                        width=1.5,
                        alpha=0.6,
                        ax=ax
                    )
                    
                    # Etiquetas más pequeñas
                    nx.draw_networkx_labels(
                        G, pos,
                        font_size=8,
                        font_weight='bold',
                        ax=ax
                    )
                    
                    ax.set_title(f"Red Social SocialTEC\n{len(G.nodes())} usuarios, {len(G.edges())} conexiones", 
                                fontsize=10)
                    ax.axis('off')
                    
                    # Ajustar márgenes
                    self.fig.tight_layout()
                    
                except Exception as e:
                    print(f"Error dibujando grafo: {e}")
                    ax.text(0.5, 0.5, f'Error dibujando grafo:\n{str(e)}',
                            ha='center', va='center', fontsize=10)
                    ax.axis('off')
            
            self.draw()
            
        except Exception as e:
            print(f"Error en draw_graph: {e}")
            # Crear una figura de error
            self.fig.clear()
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, f'Error:\n{str(e)[:50]}...',
                    ha='center', va='center', fontsize=10)
            ax.axis('off')
            self.draw()


########### VENTANA PRINCIPAL DEL SERVIDOR ##########
class ServerWindow(QMainWindow):
    def __init__(self, server_instance):
        super().__init__()
        self.server = server_instance
        self.setWindowTitle("SocialTEC - Servidor")
        self.setGeometry(100, 100, 1200, 800)

        # Variables para estadísticas y busqueda
        self.stats_result = ""
        self.path_result = ""

        self.init_ui()

        # Timer para actualizar el grafo periódicamente
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(5000)

    def init_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout(central_widget)

        # Panel izquierdo (controles)
        control_panel = QFrame()
        control_panel.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        control_panel.setMaximumWidth(300)
        control_layout = QVBoxLayout(control_panel)

            # Título
        title_label = QLabel("Controles del servidor")
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(title_label)

        control_layout.addSpacing(20)

            # Sección: Información del servidor
        info_group = QGroupBox("Información del Servidor")
        info_layout = QVBoxLayout()

        self.status_label = QLabel("Servidor activo")
        self.status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        info_layout.addWidget(self.status_label)

        self.users_label = QLabel("Usuarios registrados: 0")
        info_layout.addWidget(self.users_label)

        info_group.setLayout(info_layout)
        control_layout.addWidget(info_group)

        control_layout.addSpacing(20)

            # Sección: Estadísticas
        stats_group = QGroupBox("Estadísticas de la Red")
        stats_layout = QVBoxLayout()

        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMaximumHeight(150)
        self.stats_text.setPlaceholderText("Presiona 'Calcular' para ver estadísticas")
        stats_layout.addWidget(self.stats_text)

        stats_btn = QPushButton("Calcular Estadísticas")
        stats_btn.clicked.connect(self.calculate_stats)
        stats_layout.addWidget(stats_btn)

        stats_group.setLayout(stats_layout)
        control_layout.addWidget(stats_group)

        control_layout.addSpacing(20)

            # Sección Búsqueda de ruta
        path_group = QGroupBox("Buscar Ruta entre Usuarios")
        path_layout = QVBoxLayout()

            # Entradas
        user1_layout = QHBoxLayout()
        user1_layout.addWidget(QLabel("Usuario 1:"))
        self.user1_input = QLineEdit()
        user1_layout.addWidget(self.user1_input)
        
        user2_layout = QHBoxLayout()
        user2_layout.addWidget(QLabel("Usuario 2:"))
        self.user2_input = QLineEdit()
        user2_layout.addWidget(self.user2_input)
        
        path_layout.addLayout(user1_layout)
        path_layout.addLayout(user2_layout)
        
        self.path_result_text = QTextEdit()
        self.path_result_text.setReadOnly(True)
        self.path_result_text.setMaximumHeight(100)
        self.path_result_text.setPlaceholderText("Resultado de la búsqueda aparecerá aquí")
        path_layout.addWidget(self.path_result_text)

        find_path_btn = QPushButton("Buscar Ruta")
        find_path_btn.clicked.connect(self.find_path)
        path_layout.addWidget(find_path_btn)

        path_group.setLayout(path_layout)
        control_layout.addWidget(path_group)

        control_layout.addSpacing(20)

            # Botones de control
        control_buttons = QVBoxLayout()

        refresh_btn = QPushButton("Actualizar grafo")
        refresh_btn.clicked.connect(self.update_graph)
        control_buttons.addWidget(refresh_btn)

        export_btn = QPushButton("Exportar datos")
        export_btn.clicked.connect(self.export_data)
        control_buttons.addWidget(export_btn)

        control_layout.addLayout(control_buttons)
        control_layout.addStretch()

            # Panel derecho (grafo)
        graph_panel = QFrame()
        graph_layout = QVBoxLayout(graph_panel)

        graph_title = QLabel("Visualización de SocialTEC")
        graph_title.setStyleSheet("font-weight: bold; font-size: 18px; color: #2c3e50;")
        graph_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        graph_layout.addWidget(graph_title)

            # Canvas del grafo
        self.graph_canvas = GraphCanvas(self.server.graph, self)
        graph_layout.addWidget(self.graph_canvas)

            # Barra de estado
        status_bar = QStatusBar()
        status_bar.setStyleSheet("background-color: #ecf0f1;")
        self.setStatusBar(status_bar)

        self.status_label_bar = QLabel("Servidor iniciado correctamente")
        status_bar.addWidget(self.status_label_bar)

            # Agregar paneles al layout principal
        main_layout.addWidget(control_panel)
        main_layout.addWidget(graph_panel, 1)

    def update_graph(self):
        """Actualiza la visualización del grafo y la información"""
        try:
            # Actualizar conteos
            num_users = len(self.server.db.data["users"])
            self.users_label.setText(f"Usuarios registrados: {num_users}")

            # Actualizar el grafo
            self.graph_canvas.draw_graph()

            # Mostrar actualización en barra de estado
            self.status_label_bar.setText(f"Grafo actualizado - {num_users} usuarios")

        except Exception as e:
            print(f"Error actualizando grafo: {e}")

    
    def calculate_stats(self):
        """Calcula y muestra las estadísticas de la red"""
        try:
            stats = self.server.graph.get_statistics()

            if stats['max'][0] is None or stats['min'][0] is None:
                stats_text = "Estadísticas de la red \n\n"
                stats_text += "No hay usuarios en la red\n\n"
                stats_text += "Total de usuarios: 0\n"
                stats_text += "Total de conexiones: 0"

            else:

                stats_text = "Estadísticas de la red \n\n"

                stats_text += f"Usuarios con más amigos: {stats['max'][0]} "
                stats_text += f"({stats['max'][1]} amigos)\n\n"
                stats_text += f"Usuario con menos amigos: {stats['min'][0]} "
                stats_text += f"Promedio de amigos por usuario: {stats['avg']:.2f}\n\n"
                stats_text += f"Total de usuarios: {self.server.graph.graph.number_of_nodes()}\n"
                stats_text += f"Total de conexiones: {self.server.graph.graph.number_of_edges()}"

                self.stats_text.setText(stats_text)
                self.status_label_bar.setText("Estadísticas calculadas")

        except Exception as e:
            self.stats_text.setText(f"Error calculando estadísticas: {e}")
    
    def find_path(self):
        """Busca un camino entre dos usuarios"""
        user1 = self.user1_input.text().strip()
        user2 = self.user2_input.text().strip()
        
        if not user1 or not user2:
            self.path_result_text.setText("Por favor ingresa ambos usuarios")
            return
        
        if user1 == user2:
            self.path_result_text.setText("Los usuarios deben ser diferentes")
            return
        
        try:
            # Crear solicitud como lo haría un cliente
            request = {
                "action": "find_path",
                "start": user1,
                "end": user2
            }
            
            # Usar el método del servidor directamente
            response = self.server._handle_find_path(request)
            
            if response["status"] == "success":
                path = response["path"]
                path_text = f"CAMINO ENCONTRADO:\n\n"
                path_text += " → ".join(path)
                path_text += f"\n\nLongitud: {len(path)-1} saltos"
            else:
                path_text = f"NO EXISTE CAMINO\n\nNo hay conexión entre '{user1}' y '{user2}'"
            
            self.path_result_text.setText(path_text)
            self.status_label_bar.setText(f"Búsqueda completada: {user1} -> {user2}")
            
        except Exception as e:
            self.path_result_text.setText(f"Error en la búsqueda: {e}")
    
    def export_data(self):
        """Exporta los datos del grafo a un archivo"""
        options = QFileDialog.Option(0)
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Exportar Datos", "socialtec_data.json", 
            "JSON Files (*.json);;All Files (*)", options=options
        )
        
        if file_name:
            try:
                # Exportar datos del grafo
                import json
                data = {
                    "usuarios": list(self.server.graph.graph.nodes()),
                    "conexiones": list(self.server.graph.graph.edges()),
                    "estadisticas": self.server.graph.get_statistics()
                }
                
                with open(file_name, 'w') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                self.status_label_bar.setText(f"Datos exportados a {file_name}")
                QMessageBox.information(self, "Éxito", "Datos exportados correctamente")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo exportar: {e}")
    
    def closeEvent(self, event):
        """Maneja el cierre de la ventana"""
        reply = QMessageBox.question(
            self, 'Confirmar Salida',
            '¿Estás seguro de que quieres cerrar el servidor?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Detener timer
            self.timer.stop()
            event.accept()
        else:
            event.ignore()