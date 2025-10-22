import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import shutil
from .users.create_user import CreateUserWindow

class ConfigPage(ctk.CTkFrame):
    def __init__(self, master, user_management, on_close=None):
        super().__init__(master)
        self.user_management = user_management
        self.on_close = on_close

        self.configure(fg_color="#1b1440")
        self.pack(fill="both", expand=True)

        # -- Topbar para titulo y boton cerrar --
        self.topbar = ctk.CTkFrame(self, height=60, fg_color="#231B44")
        self.topbar.pack(side='top', fill='x')

        self.label_title = ctk.CTkLabel(
            self.topbar,
            text="Configuración de la Aplicación",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#81E821",
            fg_color="#231B44"
        )
        self.label_title.pack(side='left', padx=30, pady=18)

        self.btn_close = ctk.CTkButton(
            self.topbar,
            text="✖",
            width=36,
            height=38,
            corner_radius=16,
            fg_color="#c0392b",
            hover_color="#e74c3c",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self._handle_close
        )
        self.btn_close.pack(side="right", padx=18, pady=13)

        # -- Cuerpo principal con pestañas --
        self.main_frame = ctk.CTkFrame(self, fg_color="#28204d")
        self.main_frame.pack(fill='both', expand=True, padx=42, pady=(18, 30))

        # Tabview moderno de secciones
        self.tabview = ctk.CTkTabview(
            self.main_frame,
            width=880, height=540,
            segmented_button_fg_color="#4113AE",
            segmented_button_selected_color="#81E821",
            segmented_button_selected_hover_color="#6CCC09",
            segmented_button_unselected_color="#28204d"
        )
        self.tabview.pack(expand=True, fill='both', padx=42, pady=32)
        self.tabview.add("Usuarios")
        self.tabview.add("Logo")
        # Ejemplo para futuras secciones:
        self.tabview.add("General")
        self.tabview.add("Permisos")

        # --- Usuarios tab ---
        self._build_users_tab()

        # --- Logo tab ---
        self._build_logo_tab()

        # --- (Opcional) General y Permisos tab ---
        self._build_general_tab()
        self._build_permisos_tab()

    def _build_users_tab(self):
        frame = self.tabview.tab("Usuarios")
        frame.grid_columnconfigure(0, weight=1)
        frame.configure(fg_color="#232150")

        label = ctk.CTkLabel(
            frame,
            text="Configuración de Usuarios",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#81E821"
        )
        label.pack(pady=(30, 16))

        self.btn_create_user = ctk.CTkButton(
            frame,
            text="Crear Nuevo Usuario",
            font=ctk.CTkFont(size=18),
            fg_color="#4113AE",
            hover_color="#511ABE",
            command=self.open_create_user
        )
        self.btn_create_user.pack(pady=8)

    def _build_logo_tab(self):
        frame = self.tabview.tab("Logo")
        frame.configure(fg_color="#232150")

        label = ctk.CTkLabel(
            frame,
            text="Cambiar Logo del Cliente",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color="#81E821"
        )
        label.pack(pady=(36, 18))

        self.btn_change_logo = ctk.CTkButton(
            frame,
            text="Seleccionar Archivo de Logo",
            font=ctk.CTkFont(size=17),
            fg_color="#4113AE",
            hover_color="#511ABE",
            command=self.seleccionar_logo
        )
        self.btn_change_logo.pack(pady=10)

    def _build_general_tab(self):
        frame = self.tabview.tab("General")
        frame.configure(fg_color="#232150")
        label = ctk.CTkLabel(
            frame,
            text="Configuraciones Generales (Ejemplo)",
            font=ctk.CTkFont(size=20),
            text_color="#81E821"
        )
        label.pack(pady=(44, 8))

    def _build_permisos_tab(self):
        frame = self.tabview.tab("Permisos")
        frame.configure(fg_color="#232150")
        label = ctk.CTkLabel(
            frame,
            text="Gestión de Permisos (Ejemplo)",
            font=ctk.CTkFont(size=20),
            text_color="#81E821"
        )
        label.pack(pady=(44, 8))

    def open_create_user(self):
        def refresh_users():
            pass  # Actualizar lista de usuarios

        create_window = CreateUserWindow(self.master, self.user_management, refresh_callback=refresh_users)
        create_window.focus_set()

    def seleccionar_logo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccione el logo del cliente",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if ruta:
            destino_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "logo-cliente")
            if not os.path.exists(destino_dir):
                os.makedirs(destino_dir)
            destino = os.path.join(destino_dir, "logo.png")
            try:
                shutil.copyfile(ruta, destino)
                messagebox.showinfo("Logo cambiado", "El logo del cliente se cambió correctamente. Por favor reinicie el dashboard para ver los cambios.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cambiar el logo: {e}")

    def _handle_close(self):
        if callable(self.on_close):
            self.on_close()
