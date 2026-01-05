import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QLineEdit, QTextEdit, QLabel, QMessageBox, 
                             QStackedWidget, QFileDialog, QListWidget, QAbstractItemView)
from PyQt5.QtCore import Qt

class AssistenteGit(QWidget):
    def __init__(self):
        super().__init__()
        self.diretorio_projeto = ""
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Assistente GIT')
        self.setFixedSize(550, 700)
        
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #FFFFFF; font-family: 'Segoe UI', sans-serif; }
            QPushButton { 
                background-color: #6200EE; border-radius: 8px; padding: 12px; 
                font-size: 14px; font-weight: bold; margin: 5px; 
            }
            QPushButton:hover { background-color: #3700B3; }
            QLineEdit, QTextEdit, QListWidget { 
                background-color: #1E1E1E; border: 1px solid #333; 
                border-radius: 5px; padding: 8px; color: white; 
            }
            QListWidget::item:selected { background-color: #03DAC6; color: black; }
            QLabel { font-size: 16px; margin-bottom: 5px; }
            #labelPasta { color: #03DAC6; font-weight: bold; font-size: 13px; }
        """)

        self.main_layout = QVBoxLayout()
        self.stack = QStackedWidget()

        # Telas
        self.stack.addWidget(self.create_menu())
        self.stack.addWidget(self.create_tela_criar())
        self.stack.addWidget(self.create_tela_atualizar())
        self.stack.addWidget(self.create_tela_readme())
        self.stack.addWidget(self.create_tela_gitignore()) # Nova tela (Index 4)

        self.main_layout.addWidget(self.stack)
        self.setLayout(self.main_layout)

    def selecionar_pasta(self):
        pasta = QFileDialog.getExistingDirectory(self, "Selecione o local do seu projeto")
        if pasta:
            self.diretorio_projeto = pasta
            self.label_pasta_selecionada.setText(f"Projeto: {pasta}")
            return True
        return False

    def ir_para_tela(self, index):
        if not self.diretorio_projeto:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione a pasta do projeto primeiro!")
            return
        
        if index == 4: # Se for a tela do gitignore, atualiza a lista de arquivos
            self.atualizar_lista_arquivos()
            
        self.stack.setCurrentIndex(index)

    # --- TELAS ---
    
    def create_menu(self):
        widget = QWidget()
        layout = QVBoxLayout()
        titulo = QLabel("Assistente GIT")
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #6200EE;")
        titulo.setAlignment(Qt.AlignCenter)

        self.label_pasta_selecionada = QLabel("Nenhuma pasta selecionada")
        self.label_pasta_selecionada.setObjectName("labelPasta")
        self.label_pasta_selecionada.setAlignment(Qt.AlignCenter)
        
        btn_pasta = QPushButton("📁 Selecionar Pasta do Projeto")
        btn_pasta.setStyleSheet("background-color: #03DAC6; color: black;")
        btn_pasta.clicked.connect(self.selecionar_pasta)

        btn_criar = QPushButton("Criar Novo GIT")
        btn_atualizar = QPushButton("Atualizar GIT")
        btn_readme = QPushButton("Criar README.md")
        btn_ignore = QPushButton("Criar .gitignore")

        btn_criar.clicked.connect(lambda: self.ir_para_tela(1))
        btn_atualizar.clicked.connect(lambda: self.ir_para_tela(2))
        btn_readme.clicked.connect(lambda: self.ir_para_tela(3))
        btn_ignore.clicked.connect(lambda: self.ir_para_tela(4))

        layout.addStretch()
        layout.addWidget(titulo)
        layout.addWidget(self.label_pasta_selecionada)
        layout.addWidget(btn_pasta)
        layout.addSpacing(20)
        layout.addWidget(btn_criar)
        layout.addWidget(btn_atualizar)
        layout.addWidget(btn_readme)
        layout.addWidget(btn_ignore)
        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_tela_gitignore(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Selecione os arquivos/pastas para ignorar:"))
        layout.addWidget(QLabel("(Segure CTRL para selecionar múltiplos)"))
        
        self.lista_arquivos = QListWidget()
        self.lista_arquivos.setSelectionMode(QAbstractItemView.MultiSelection)
        
        btn_gerar = QPushButton("Gerar arquivo .gitignore")
        btn_gerar.clicked.connect(self.salvar_gitignore)
        
        layout.addWidget(self.lista_arquivos)
        layout.addWidget(btn_gerar)
        layout.addWidget(self.btn_voltar())
        widget.setLayout(layout)
        return widget

    # Outras telas permanecem iguais (Criar, Atualizar, Readme)...
    def create_tela_criar(self):
        widget = QWidget(); layout = QVBoxLayout()
        self.url_git = QLineEdit(placeholderText="URL do Repositório Git"); self.msg_commit = QLineEdit(placeholderText="Mensagem do Primeiro Commit")
        btn = QPushButton("Inicializar e Enviar"); btn.clicked.connect(self.exec_criar_git)
        layout.addWidget(QLabel("Configurar Novo Repositório")); layout.addWidget(self.url_git); layout.addWidget(self.msg_commit); layout.addWidget(btn); layout.addWidget(self.btn_voltar()); widget.setLayout(layout); return widget

    def create_tela_atualizar(self):
        widget = QWidget(); layout = QVBoxLayout()
        self.msg_update = QLineEdit(placeholderText="Mensagem do Commit")
        btn = QPushButton("Enviar Atualizações"); btn.clicked.connect(self.exec_atualizar_git)
        layout.addWidget(QLabel("Atualizar Repositório")); layout.addWidget(self.msg_update); layout.addWidget(btn); layout.addWidget(self.btn_voltar()); widget.setLayout(layout); return widget

    def create_tela_readme(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.url_readme = QLineEdit(placeholderText="URL do Repositório Git (para o push)")
        
        # Modelo de texto pré-definido
        modelo_readme = (
            "# 🚀 Multi Conversor Pro\n\n"
            "Software de alta performance para conversão em massa de arquivos multimídia.\n\n"
            "### 🛠 Recursos\n"
            "* **Imagens:** Conversão entre JPG, PNG, BMP e ICO.\n"
            "* **Áudio:** Conversão de alta fidelidade entre MP3, WAV, FLAC e OGG.\n"
            "* **Vídeo:** Conversão de formatos MP4, AVI, MOV e MKV.\n\n"
            "### ⚙️ Requisitos (FFmpeg)\n"
            "1. Baixe o FFmpeg em ffmpeg.org\n"
            "2. Adicione a pasta /bin às Variáveis de Ambiente (Path) do Windows.\n\n"
            "### 💻 Tecnologias\n"
            "- Interface: PyQt5\n"
            "- Estilização: QSS\n"
            "- Motores: Pydub, FFmpeg e Pillow"
        )

        self.conteudo_readme = QTextEdit()
        self.conteudo_readme.setPlainText(modelo_readme) # Insere o modelo automaticamente
        
        btn_executar = QPushButton("Gerar e Enviar README")
        btn_executar.clicked.connect(self.exec_readme)
        
        layout.addWidget(QLabel("Editor de README.md"))
        layout.addWidget(self.url_readme)
        layout.addWidget(self.conteudo_readme)
        layout.addWidget(btn_executar)
        layout.addWidget(self.btn_voltar())
        widget.setLayout(layout)
        return widget

    def btn_voltar(self):
        btn = QPushButton("Voltar ao Menu"); btn.setStyleSheet("background-color: #333;"); btn.clicked.connect(lambda: self.stack.setCurrentIndex(0)); return btn

    # --- LÓGICA ESPECÍFICA DO GITIGNORE ---

    def atualizar_lista_arquivos(self):
        self.lista_arquivos.clear()
        try:
            # Lista todos os arquivos e pastas no diretório selecionado
            itens = os.listdir(self.diretorio_projeto)
            for item in itens:
                if item != ".git": # Não precisamos ignorar a pasta do próprio git
                    self.lista_arquivos.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível listar arquivos: {e}")

    def salvar_gitignore(self):
        selecionados = [item.text() for item in self.lista_arquivos.selectedItems()]
        if not selecionados:
            QMessageBox.warning(self, "Aviso", "Nenhum arquivo selecionado!")
            return

        try:
            caminho_ignore = os.path.join(self.diretorio_projeto, ".gitignore")
            with open(caminho_ignore, "w", encoding="utf-8") as f:
                f.write("\n".join(selecionados))
            
            QMessageBox.information(self, "Sucesso", ".gitignore criado com sucesso na pasta do projeto!")
            self.stack.setCurrentIndex(0)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao salvar .gitignore: {e}")

    # --- LÓGICA DO GIT ---

    def run_git_commands(self, commands):
        try:
            os.chdir(self.diretorio_projeto)
            for cmd in commands:
                subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            QMessageBox.information(self, "Sucesso", "Operação Git realizada!")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Erro no Git", e.stderr if e.stderr else str(e))

    def exec_criar_git(self):
        url, msg = self.url_git.text(), self.msg_commit.text()
        if url and msg:
            self.run_git_commands(["git init", "git add .", f'git commit -m "{msg}"', "git branch -M main", f"git remote add origin {url}", "git push -u origin main"])

    def exec_atualizar_git(self):
        msg = self.msg_update.text()
        if msg:
            self.run_git_commands(["git add .", f'git commit -m "{msg}"', "git push"])

    def exec_readme(self):
        url, content = self.url_readme.text(), self.conteudo_readme.toPlainText()
        if url and content:
            os.chdir(self.diretorio_projeto)
            with open("README.md", "w", encoding="utf-8") as f: f.write(content)
            self.run_git_commands(["git add README.md", 'git commit -m "docs: update README.md"', f"git remote set-url origin {url}", "git push origin main"])

if __name__ == '__main__':
    app = QApplication(sys.argv); ex = AssistenteGit(); ex.show(); sys.exit(app.exec_())