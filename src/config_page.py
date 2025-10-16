import customtkinter as ctk
from .users.create_user import CreateUserWindow

class ConfigPage(ctk.CTkFrame):
    def __init__(self, master, user_management):
        super().__init__(master)
        self.user_management = user_management

        self.label = ctk.CTkLabel(self, text="Configuración Principal", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=20)

        self.btn_create_user = ctk.CTkButton(self, text="Crear Nuevo Usuario", command=self.open_create_user)
        self.btn_create_user.pack(pady=10)

    def open_create_user(self):
        def refresh_users():
            pass  # Actualiza lista usuarios aquí

        create_window = CreateUserWindow(self.master, self.user_management, refresh_callback=refresh_users)
        create_window.focus_set()
