import customtkinter as ctk
from tkinter import messagebox
import hashlib

class ChangePasswordWindow(ctk.CTkToplevel):
    def __init__(self, master, user_management, user_id, username):
        super().__init__(master)
        self.user_management = user_management
        self.user_id = user_id
        self.username = username

        self.title(f"Cambiar Contraseña: {username}")
        self.geometry("400x300")
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        self._create_widgets()

    def _create_widgets(self):
        ctk.CTkLabel(self, text="Nueva Contraseña", font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#00FFFF").pack(pady=20)

        self.entry_new_password = ctk.CTkEntry(self, placeholder_text="Mínimo 6 caracteres", show="*",
                                               font=ctk.CTkFont(size=14))
        self.entry_new_password.pack(fill="x", padx=30, pady=(0, 15))

        self.entry_confirm_password = ctk.CTkEntry(self, placeholder_text="Confirmar contraseña", show="*",
                                                   font=ctk.CTkFont(size=14))
        self.entry_confirm_password.pack(fill="x", padx=30, pady=(0, 20))

        btn_update = ctk.CTkButton(self, text="Actualizar Contraseña", fg_color="#00C853",
                                   text_color="#001122", font=ctk.CTkFont(size=16, weight="bold"),
                                   command=self._update_password)
        btn_update.pack(padx=30, fill="x")

    def _update_password(self):
        new_password = self.entry_new_password.get()
        confirm_password = self.entry_confirm_password.get()

        if not new_password or not confirm_password:
            messagebox.showwarning("Faltan Datos", "Por favor complete ambos campos.")
            return

        if len(new_password) < 6:
            messagebox.showwarning("Contraseña Débil", "La contraseña debe tener al menos 6 caracteres.")
            return

        if new_password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return

        password_hashed = hashlib.sha256(new_password.encode("utf-8")).hexdigest()

        success = self.user_management.update_user_password(self.user_id, password_hashed)

        if success:
            messagebox.showinfo("Éxito", "Contraseña actualizada correctamente.")
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la contraseña.")
