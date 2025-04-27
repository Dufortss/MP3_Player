import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QPixmap, QPainter, QMouseEvent, QPalette, QColor
from PyQt6.QtCore import Qt, QPoint
import re


class YouTubePlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reprodutor YouTube Personalizado")
        
        # 🔹 Definir tamanho da janela (fixo ou ajustável)
        self.resize(410, 217)  # Permite redimensionamento (troque por setFixedSize() se quiser fixo)

        # 🔥 Tornar a janela transparente e sem moldura
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")

        # 🔹 Carregar imagem de fundo (utilizando a função resource_path)
        image_path = self.resource_path("Novo_projeto_9_ED045BD.png")
        self.background = QPixmap(image_path)

        # 🔹 Player de vídeo
        self.video_player = QWebEngineView(self)
        self.video_player.setGeometry(42, 28, 188, 160)  
        
        # 🔹 Campo para inserir URL
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Cole a URL do YouTube aqui...")
        self.url_input.setGeometry(210, 180, 120, 30)
        
        # Mudando a cor do placeholder com QPalette
        palette = self.url_input.palette()
        palette.setColor(QPalette.ColorRole.Text, QColor("black"))  # Cor do texto
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#4d0000"))  # Cor do placeholder
        self.url_input.setPalette(palette)

        # 🔹 Botão para carregar vídeo
        self.play_button = QPushButton("", self)
        self.play_button.setGeometry(240, 85, 45, 45)
        self.play_button.clicked.connect(self.load_video)
        
        # 🔹 Botão para próximo vídeo
        self.next_button = QPushButton("", self)
        self.next_button.setGeometry(290, 30, 45, 45)
        self.next_button.clicked.connect(self.next_video)

        # 🔹 Variável para armazenar URLs e índice atual
        self.urls = []  # Lista de URLs
        self.current_index = 0  # Índice do vídeo atual
        
        # 🔹 Variável para armazenar posição inicial do mouse
        self.drag_pos = QPoint()

    def resource_path(self, relative_path):
        """ Retorna o caminho absoluto para o recurso (imagem) """
        try:
            # Para o modo de produção (executável)
            if hasattr(sys, '_MEIPASS'):
                return os.path.join(sys._MEIPASS, relative_path)
            # Para o modo de desenvolvimento
            return os.path.join(os.path.abspath("."), relative_path)
        except Exception as e:
            return relative_path

    def paintEvent(self, event):
        """ Desenha a imagem de fundo cobrindo a janela. """
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background)

    def load_video(self):
        """ Carrega um vídeo do YouTube no iframe. """
        url = self.url_input.text().strip()
        video_id = self.extract_video_id(url)

        if video_id:
            embed_url = f"https://www.youtube.com/embed/{video_id}"
            iframe_html = f"""
            <html>
                <body style="margin:0px;padding:0px;overflow:hidden">
                    <iframe width="100%" height="100%" src="{embed_url}" frameborder="0" allowfullscreen></iframe>
                </body>
            </html>
            """
            # Adiciona a URL à lista de vídeos
            self.urls.append(embed_url)
            self.url_input.clear()  # Limpa o campo de texto
            self.play_video()  # Reproduz o primeiro vídeo
        else:
            self.url_input.setText("URL inválida!")

    def play_video(self):
        """ Reproduz o vídeo atual da lista de URLs. """
        if self.urls:
            self.video_player.setHtml(f"""
            <html>
                <body style="margin:0px;padding:0px;overflow:hidden">
                    <iframe width="100%" height="100%" src="{self.urls[self.current_index]}" frameborder="0" allowfullscreen></iframe>
                </body>
            </html>
            """)
        else:
            self.url_input.setText("Adicione uma URL!")

    def next_video(self):
        """ Vai para o próximo vídeo na lista. """
        if self.urls:
            self.current_index = (self.current_index + 1) % len(self.urls)  # Vai para o próximo, reinicia quando chegar ao final
            self.play_video()

    def extract_video_id(self, url):
        """ Extrai o ID do vídeo do link do YouTube. """
        patterns = [
            r"youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)",  
            r"youtu\.be\/([a-zA-Z0-9_-]+)",  
            r"youtube\.com\/embed\/([a-zA-Z0-9_-]+)"  
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    # ✅ Permitir mover a janela com o mouse
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()  # Usando toPoint()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)  # Usando toPoint()
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = YouTubePlayer()
    player.show()
    sys.exit(app.exec())
