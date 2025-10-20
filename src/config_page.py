import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import shutil
from .users.create_user import CreateUserWindow


class ConfigPage(ctk.CTkFrame):
    def __init__(self, master, user_management):
        super().__init__(master)
        self.user_management = user_management

        self.label = ctk.CTkLabel(self, text="Configuración Principal", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.btn_create_user = ctk.CTkButton(self, text="Crear Nuevo Usuario", command=self.open_create_user)
        self.btn_create_user.pack(pady=10)

        # Botón para cambiar logo del cliente
        self.btn_change_logo = ctk.CTkButton(self, text="Cambiar Logo del Cliente", command=self.seleccionar_logo)
        self.btn_change_logo.pack(pady=10)

    def open_create_user(self):
        def refresh_users():
            pass  # Actualiza lista usuarios aquí

        create_window = CreateUserWindow(self.master, self.user_management, refresh_callback=refresh_users)
        create_window.focus_set()

    def seleccionar_logo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccione el logo del cliente",
            filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.bmp *.gif")]
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
