import customtkinter as ctk
from .database.db_manager import DBManager
from .users.user_management import UserManagement
from .login import LoginFrame
from .dashboard import Dashboard
import os


class ERPApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Establecer tamaño de ventana a pantalla completa y maximizar
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        self.geometry(f"{width}x{height}+0+0")
        self.state('zoomed')

        # Crear la instancia real de DBManager y UserManagement
        self.db_manager = DBManager()
        self.user_management = UserManagement(self.db_manager)

        self.login_frame = LoginFrame(self, self.user_management, on_login_success=self.show_dashboard)
        self.login_frame.pack(fill='both', expand=True)

        self.dashboard_frame = None

    def show_dashboard(self, user):
        self.login_frame.pack_forget()

        if self.dashboard_frame is None:
            ruta_logo_cliente = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..", "assets", "logo-cliente", "logo.png"
            )
            # Pasar la instancia real de user_management aquí
            self.dashboard_frame = Dashboard(
                self,
                user_data=user,
                user_management=self.user_management,
                logo_cliente_path=ruta_logo_cliente,
                on_logout=self.handle_logout  # Pasar callback para logout
            )

        self.dashboard_frame.pack(fill='both', expand=True)

    def handle_logout(self):
        if self.dashboard_frame:
            self.dashboard_frame.pack_forget()
            self.dashboard_frame.destroy()
            self.dashboard_frame = None

        self.login_frame.pack(fill='both', expand=True)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    app = ERPApp()
    app.mainloop()
