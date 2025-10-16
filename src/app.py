import customtkinter as ctk
from .database.db_manager import DBManager
from .users.user_management import UserManagement
from . import config_page
from .login import LoginWindow


class ERPApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db_manager = DBManager()
        self.user_management = UserManagement(self.db_manager)

        # Ocultar ventana principal inicialmente
        self.withdraw()

        def open_main(user):
            # Mostrar ventana principal y cargar configuración
            self.deiconify()
            self.main_page = config_page.ConfigPage(self, self.user_management)
            self.main_page.pack(fill="both", expand=True)

        # Abrir ventana login hija CTkToplevel para evitar error de imagen
        self.login_window = LoginWindow(self, self.user_management, on_login_success=open_main)
        self.login_window.focus()
        self.login_window.grab_set()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ERPApp()
    app.mainloop()
