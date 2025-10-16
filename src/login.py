import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage, CTkLabel
import os
import hashlib

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, parent, user_management, on_login_success):
        super().__init__(parent)
        self.parent = parent
        self.user_management = user_management
        self.on_login_success = on_login_success

        self.title("Ingreso al Sistema")
        self.geometry("600x600")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self._create_widgets()
        self._place_focus()

    def _create_widgets(self):
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "logo-app", "logo.png")

        # Guarda logo en atributo del padre para evitar garbage collection
        if hasattr(self.parent, 'ctk_img'):
            self.parent.ctk_img = self.parent.ctk_img
        else:
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                self.parent.ctk_img = CTkImage(light_image=img, dark_image=img, size=(150, 150))
            else:
                self.parent.ctk_img = None

        if self.parent.ctk_img:
            self.logo_label = CTkLabel(self, image=self.parent.ctk_img, text="")
            self.logo_label.pack(pady=20)
        else:
            self.logo_label = CTkLabel(self, text="Bienvenido", font=ctk.CTkFont(size=28, weight="bold"), pady=20)
            self.logo_label.pack()

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(padx=40, pady=20, fill="both", expand=True)

        self.username_entry = ctk.CTkEntry(self.frame, placeholder_text="Nombre de usuario")
        self.username_entry.pack(pady=(40, 12), padx=20, fill="x")

        self.password_entry = ctk.CTkEntry(self.frame, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=12, padx=20, fill="x")

        self.remember_me = ctk.CTkCheckBox(self.frame, text="Recordarme")
        self.remember_me.pack(pady=12)

        self.login_button = ctk.CTkButton(self.frame, text="Ingresar", command=self._attempt_login)
        self.login_button.pack(pady=30, padx=20, fill="x")

    def _place_focus(self):
        self.username_entry.focus_set()

    def _attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("Error", "Por favor ingresa usuario y contraseña.")
            return

        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        user = self.user_management.get_user_by_username(username)

        if user and user["password"] == password_hash:
            messagebox.showinfo("Éxito", f"Bienvenido, {user['nombre_completo']}!")
            self.destroy()
            self.on_login_success(user)
        else:
            messagebox.showerror("Falló ingreso", "Usuario o contraseña incorrectos.")
            self.password_entry.delete(0, "end")
