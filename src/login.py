import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage, CTkLabel
import os
import hashlib


class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, user_management, on_login_success):
        super().__init__(parent)
        self.parent = parent
        self.user_management = user_management
        self.on_login_success = on_login_success

        self.pack(fill='both', expand=True)  # Ocupa toda ventana padre

        # Frame pequeño centrado para formulario
        self.form_frame = ctk.CTkFrame(self, width=400, height=400, corner_radius=15)
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")

        self._create_widgets()
        self._place_focus()

        # Etiqueta fija con crédito abajo centrada
        self.credit_label = ctk.CTkLabel(self.parent,
                                        text="ProfitUs: Creado por Jhoda Studios.",
                                        font=ctk.CTkFont(size=14))
        self.credit_label.place(relx=0.5, rely=0.95, anchor="center")

    def _create_widgets(self):
        logo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..", "assets", "logo-app", "logo.png"
        )

        if hasattr(self.parent, 'ctk_img'):
            self.parent.ctk_img = self.parent.ctk_img
        else:
            if os.path.exists(logo_path):
                img = Image.open(logo_path)
                self.parent.ctk_img = CTkImage(light_image=img, dark_image=img, size=(150, 150))
            else:
                self.parent.ctk_img = None

        if self.parent.ctk_img:
            self.logo_label = CTkLabel(self.form_frame, image=self.parent.ctk_img, text="")
            self.logo_label.pack(pady=20)
        else:
            self.logo_label = CTkLabel(self.form_frame, text="Bienvenido",
                                    font=ctk.CTkFont(size=28, weight="bold"), pady=20)
            self.logo_label.pack()

        self.username_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Nombre de usuario", width=320)
        self.username_entry.pack(pady=(20, 12), padx=20)

        self.password_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Contraseña", show="*", width=320)
        self.password_entry.pack(pady=12, padx=20)

        self.remember_me = ctk.CTkCheckBox(self.form_frame, text="Recordarme")
        self.remember_me.pack(pady=12)

        self.login_button = ctk.CTkButton(self.form_frame, text="Ingresar", command=self._attempt_login, width=320)
        self.login_button.pack(pady=30, padx=20)

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
            self.on_login_success(user)
        else:
            messagebox.showerror("Falló ingreso", "Usuario o contraseña incorrectos.")
            self.password_entry.delete(0, "end")
