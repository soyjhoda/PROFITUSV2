import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from PIL import Image
from customtkinter import CTkImage
import os
import shutil
import tkinter.font as tkFont
from .users.create_user import CreateUserWindow
from .users.edit_user import EditUserWindow
from src.ui.theme import (
    BACKGROUND_COLOR, BUTTON_STYLE_DEFAULT, FONT_BOLD_LARGE, FONT_BOLD_MEDIUM,
    FONT_BOLD_SMALL, FONT_REGULAR_MEDIUM, TEXT_COLOR_SECONDARY, ICON_BTN_USUARIOS_PATH,
    TREE_FONT, TREE_FONT_HEADER, TREE_BG_COLOR, TREE_HEADER_BG_COLOR, TREE_HEADER_FG_COLOR, TREE_FG_COLOR, TREE_ROW_HEIGHT, TREE_SELECTED_COLOR
)



class ConfigPage(ctk.CTkFrame):
    def __init__(self, master, user_management, on_close=None):
        super().__init__(master)

        if user_management is None:
            messagebox.showerror("Error", "user_management no puede ser None. Pasa la instancia correcta.")
            raise ValueError("user_management es None")

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
        self.btn_close.pack(side="left", padx=18, pady=10)

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
            hover_color="#A70505",
            command=self.open_create_user
        )
        self.btn_create_user.pack(pady=8)

        # Tabla usuarios con ancho limitado

        self.user_table_frame = ctk.CTkFrame(self.tab_usuarios, fg_color="#232150", width=630)
        self.user_table_frame.pack(fill="y", expand=False, padx=20, pady=10)
        self.user_table_frame.pack_propagate(False)

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background=TREE_BG_COLOR,
            foreground=TREE_FG_COLOR,
            fieldbackground=TREE_BG_COLOR,
            rowheight=TREE_ROW_HEIGHT,
            font=TREE_FONT
        )
        style.configure(
            "Treeview.Heading",
            background=TREE_HEADER_BG_COLOR,
            foreground=TREE_HEADER_FG_COLOR,
            font=TREE_FONT_HEADER
        )
        style.map("Treeview", background=[("selected", TREE_SELECTED_COLOR)])

        self.user_tree = ttk.Treeview(
            self.user_table_frame,
            columns=("Usuario", "Nombre", "Rol"),
            height=9,
            show="headings"
        )
        self.user_tree.heading("Usuario", text="Usuario")
        self.user_tree.column("Usuario", anchor="center", width=180, stretch=False)
        self.user_tree.heading("Nombre", text="Nombre Completo")
        self.user_tree.column("Nombre", anchor="center", width=250, stretch=False)
        self.user_tree.heading("Rol", text="Rol")
        self.user_tree.column("Rol", anchor="center", width=200, stretch=False)
        self.user_tree.pack(side="left", fill="y", expand=False)

        scrollbar_y = ctk.CTkScrollbar(self.user_table_frame, orientation="vertical", command=self.user_tree.yview)
        scrollbar_y.pack(side="right", fill="y")
        self.user_tree.configure(yscrollcommand=scrollbar_y.set)

        scrollbar_x = ctk.CTkScrollbar(self.user_table_frame, orientation="horizontal", command=self.user_tree.xview)
        scrollbar_x.pack(side="bottom", fill="x")
        self.user_tree.configure(xscrollcommand=scrollbar_x.set)

        # Agregamos los botones de acción debajo de la tabla
        self.buttons_frame = ctk.CTkFrame(self.tab_usuarios, fg_color="#232150")
        self.buttons_frame.pack(pady=(5, 20))

        self.btn_edit_user = ctk.CTkButton(
            self.buttons_frame,
            text="Editar Usuario",
            width=140,
            command=self.edit_selected_user,
            hover_color="#3D8AFF"
        )
        self.btn_edit_user.pack(side="left", padx=12)

        self.btn_delete_user = ctk.CTkButton(
            self.buttons_frame,
            text="Eliminar Usuario",
            width=140,
            command=self.delete_selected_user,
            fg_color="#D74343",
            hover_color="#FF0000"
        )
        self.btn_delete_user.pack(side="left", padx=12)

        self.btn_view_info = ctk.CTkButton(
            self.buttons_frame,
            text="Ver Información",
            width=140,
            command=self.view_selected_user_info,
            fg_color="#4CAF50",
            hover_color="#66BB6A"
        )
        self.btn_view_info.pack(side="left", padx=12)

        self._load_user_data()

    def edit_selected_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Seleccione un Usuario", "Por favor seleccione un usuario para editar.")
            return
        user_id = self._get_user_id_from_selection(selected[0])
        EditUserWindow(self, self.user_management, user_id, self._load_user_data).focus_set()

    def delete_selected_user(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Seleccione un Usuario", "Por favor seleccione un usuario para eliminar.")
            return
        confirm = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de eliminar este usuario?")
        if confirm:
            user_id = self._get_user_id_from_selection(selected[0])
            success = self.user_management.delete_user(user_id)
            if success:
                messagebox.showinfo("Usuario Eliminado", "El usuario fue eliminado exitosamente.")
                self._load_user_data()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")

    def view_selected_user_info(self):
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("Seleccione un Usuario", "Por favor seleccione un usuario para ver información.")
            return
        user_id = self._get_user_id_from_selection(selected[0])
        user_data = self.user_management.db.fetch_one("SELECT * FROM usuarios WHERE id=?", (user_id,))
        if user_data:
            info_window = ctk.CTkToplevel(self)
            info_window.title(f"Información de {user_data['username']}")
            info_window.geometry("300x300")
            # Mostrar foto si existe
            if user_data['foto_path'] and os.path.exists(user_data['foto_path']):
                image = Image.open(user_data['foto_path'])
                image = image.resize((100, 100))
                photo = CTkImage(image, size=(100, 100))
                label_image = ctk.CTkLabel(info_window, image=photo)
                label_image.image = photo
                label_image.pack(pady=10)
            # Mostrar texto con info
            info_text = f"Usuario: {user_data['username']}\nNombre Completo: {user_data['nombre_completo']}\nRol: {user_data['rol']}"
            label_info = ctk.CTkLabel(info_window, text=info_text)
            label_info.pack(pady=10)
        else:
            messagebox.showerror("Error", "No se pudo obtener la información del usuario.")

    def _get_user_id_from_selection(self, tree_item_id):
        # Esto asume que el id real del usuario se guarda en el 'iid' del item, o que puedes obtenerlo del user_tree
        # Si en tu insert usas como iid el id real del usuario, devuelve ese valor
        return int(tree_item_id)

    def _load_user_data(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        usuarios = self.user_management.get_all_users()

        for usuario in usuarios:
            # Insertar usando como iid el id real para poder recuperar luego
            self.user_tree.insert(
                "",
                "end",
                iid=str(usuario["id"]),
                values=(usuario["username"], usuario["nombre_completo"], usuario["rol"])
            )

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

    def _show_tab_usuarios(self):
        self.tab_general.pack_forget()
        self.tab_usuarios.pack(fill="both", expand=True)

    def _show_tab_general(self):
        self.tab_usuarios.pack_forget()
        self.tab_general.pack(fill="both", expand=True)

    def open_create_user(self):
        def refresh_users():
            self._load_user_data()

        create_window = CreateUserWindow(self.master, self.user_management, refresh_callback=refresh_users)
        create_window.focus_set()

    def _handle_close(self):
        if callable(self.on_close):
            self.on_close()
