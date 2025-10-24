import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from customtkinter import CTkImage
import os
import shutil
from .users.create_user import CreateUserWindow
from src.ui.theme import (
    BACKGROUND_COLOR, BUTTON_STYLE_DEFAULT, FONT_BOLD_LARGE, FONT_BOLD_MEDIUM,
    FONT_BOLD_SMALL, FONT_REGULAR_MEDIUM, TEXT_COLOR_SECONDARY, ICON_BTN_USUARIOS_PATH
)


class ConfigPage(ctk.CTkFrame):
    def __init__(self, master, user_management, on_close=None):
        super().__init__(master)
        self.user_management = user_management
        self.on_close = on_close

        self.configure(fg_color=BACKGROUND_COLOR)
        self.pack(fill="both", expand=True)

        # Topbar con título y botón cerrar
        self.topbar = ctk.CTkFrame(self, height=60, fg_color="#231B44")
        self.topbar.pack(side='top', fill='x')

        self.label_title = ctk.CTkLabel(
            self.topbar,
            text="Configuración de la Aplicación",
            font=FONT_BOLD_LARGE,
            text_color=TEXT_COLOR_SECONDARY,
            fg_color="#231B44"
        )
        self.label_title.pack(side='left', padx=30, pady=18)

        self.btn_close = ctk.CTkButton(
            self.topbar,
            text="✖",
            width=40,
            height=40,
            corner_radius=16,
            fg_color="#c0392b",
            hover_color="#e74c3c",
            font=FONT_BOLD_MEDIUM,
            command=self._handle_close
        )
        self.btn_close.pack(side="right", padx=18, pady=10)

        # Frame para botones pestañas (pestañas manuales)
        self.tab_buttons_frame = ctk.CTkFrame(self, fg_color="#28204d")
        self.tab_buttons_frame.pack(side="top", fill="x", padx=50, pady=(20, 10))

        # Cargar imagen CTkImage para botón "Gestión de Usuarios"
        img_pil_usuarios = Image.open(ICON_BTN_USUARIOS_PATH)
        self.icon_gestion_usuarios = CTkImage(light_image=img_pil_usuarios, dark_image=img_pil_usuarios, size=(180, 60))

        # Cargar imagen CTkImage para botón "Gestión del Negocio"
        img_pil_negocio = Image.open("assets/iconos/btngnegocio.png")
        self.icon_gestion_negocio = CTkImage(light_image=img_pil_negocio, dark_image=img_pil_negocio, size=(180, 60))

        icon_width, icon_height = 180, 60

        # Botón "Gestión de Usuarios" con imagen
        self.btn_gestion_usuarios = ctk.CTkButton(
            self.tab_buttons_frame,
            image=self.icon_gestion_usuarios,
            text="",
            width=icon_width,
            height=icon_height,
            fg_color="transparent",
            hover_color="#2503A0",
            command=self._show_tab_usuarios
        )
        self.btn_gestion_usuarios.pack(side="left", padx=20)

        # Botón "Gestión del Negocio" con imagen y texto oculto para apariencia limpia
        self.btn_gestion_negocio = ctk.CTkButton(
            self.tab_buttons_frame,
            image=self.icon_gestion_negocio,
            text="",
            width=icon_width,
            height=icon_height,
            fg_color="transparent",
            hover_color="#F30303",
            command=self._show_tab_general
        )
        self.btn_gestion_negocio.pack(side="left", padx=20)

        # Frame para contenido de la pestaña seleccionada
        self.content_frame = ctk.CTkFrame(self, fg_color="#232150")
        self.content_frame.pack(fill="both", expand=True, padx=50, pady=(10, 30))

        # Crear contenedores por pestaña
        self._create_tab_usuarios()
        self._create_tab_general()

        # Mostrar pestaña usuarios por defecto
        self._show_tab_usuarios()

    def _create_tab_usuarios(self):
        self.tab_usuarios = ctk.CTkFrame(self.content_frame, fg_color="#232150")
        self.tab_usuarios.pack(fill="both", expand=True)

        label = ctk.CTkLabel(
            self.tab_usuarios,
            text="Configuración de Usuarios",
            font=FONT_BOLD_MEDIUM,
            text_color=TEXT_COLOR_SECONDARY
        )
        label.pack(pady=(30, 16))

        # Cargar imagen CTkImage para el botón de crear usuario
        try:
            img_pil_crear = Image.open("assets/iconos/btncrearusuario.png")
            self.icon_crear_usuario = CTkImage(light_image=img_pil_crear, dark_image=img_pil_crear, size=(180, 60))
        except Exception:
            self.icon_crear_usuario = None

        self.btn_create_user = ctk.CTkButton(
            self.tab_usuarios,
            image=self.icon_crear_usuario,
            text="",
            width=180,
            height=60,
            fg_color="transparent",
            hover_color="#A70505",  # igual que fondo para no resaltar
            command=self.open_create_user
        )
        self.btn_create_user.pack(pady=8)

    def _create_tab_general(self):
        self.tab_general = ctk.CTkFrame(self.content_frame, fg_color="#232150")
        self.tab_general.pack(fill="both", expand=True)

        label = ctk.CTkLabel(
            self.tab_general,
            text="Gestión General (pendiente)",
            font=FONT_BOLD_MEDIUM,
            text_color=TEXT_COLOR_SECONDARY
        )
        label.pack(pady=30)

        # Aquí puedes agregar botones funcionales para Gestión General más adelante

    def _show_tab_usuarios(self):
        self.tab_general.pack_forget()
        self.tab_usuarios.pack(fill="both", expand=True)

    def _show_tab_general(self):
        self.tab_usuarios.pack_forget()
        self.tab_general.pack(fill="both", expand=True)

    def open_create_user(self):
        def refresh_users():
            pass

        create_window = CreateUserWindow(self.master, self.user_management, refresh_callback=refresh_users)
        create_window.focus_set()

    def _handle_close(self):
        if callable(self.on_close):
            self.on_close()
