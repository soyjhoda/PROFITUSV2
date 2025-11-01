import os
import shutil
import customtkinter as ctk
from tkinter import messagebox, filedialog
from ..config.settings import USER_IMAGES_DIR # Importar ruta fija


class EditUserWindow(ctk.CTkToplevel):
    def __init__(self, master, user_management, user_id, refresh_callback, rol_usuario_logueado=None):
        super().__init__(master)
        self.user_management = user_management
        self.user_id = user_id
        self.refresh_callback = refresh_callback
        self.user_image_path = None
        self.rol_usuario_logueado = rol_usuario_logueado

        roles_permitidos = ["administrador total", "gerente", "desarrollador"]
        if self.rol_usuario_logueado not in roles_permitidos:
            messagebox.showerror("Permiso Denegado", "No tienes permisos para editar usuarios.")
            self.destroy()
            return

        self.title("Editar Usuario")
        self.geometry("600x520")
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        self.user_data = self.user_management.db.fetch_one("SELECT * FROM usuarios WHERE id=?", (self.user_id,))
        if not self.user_data:
            messagebox.showerror("Error", f"No se encontró el usuario con ID {user_id}")
            self.destroy()
            return

        self._create_widgets()


    def _create_widgets(self):
        ctk.CTkLabel(self, text="Editar Usuario",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#00FFFF").pack(pady=15)

        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=10, padx=20, fill="x")

        self.entry_name = self._add_labeled_entry("Nombre Completo:", self.user_data["nombre_completo"])

        ctk.CTkLabel(self.frame_form, text=f"Usuario (Login): {self.user_data['username']}").pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(self.frame_form, text="Rol Asignado:").pack(anchor="w", padx=10, pady=(12, 0))
        self.combobox_role = ctk.CTkComboBox(self.frame_form,
                                             values=["Vendedor", "Gerente", "administrador total", "desarrollador"],
                                             state="readonly")
        self.combobox_role.set(self.user_data["rol"])
        self.combobox_role.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(self.frame_form, text="Actualizar Foto de Perfil (opcional):").pack(anchor="w", padx=10, pady=(12, 0))
        btn_select_image = ctk.CTkButton(self.frame_form, text="Seleccionar Nueva Imagen", command=self._select_image)
        btn_select_image.pack(padx=10, pady=(0, 10))

        btn_save = ctk.CTkButton(self, text="Guardar Cambios", fg_color="#00C853", font=ctk.CTkFont(size=18, weight="bold"),
                                 command=self._save_changes)
        btn_save.pack(pady=10, padx=40, fill="x")

        btn_change_password = ctk.CTkButton(self, text="Cambiar Contraseña", fg_color="#0097A7", font=ctk.CTkFont(size=16),
                                            command=self._open_change_password)
        btn_change_password.pack(pady=(0, 20), padx=40, fill="x")


    def _add_labeled_entry(self, label, default_text=""):
        ctk.CTkLabel(self.frame_form, text=label).pack(anchor="w", padx=10, pady=(6, 0))
        entry = ctk.CTkEntry(self.frame_form, font=ctk.CTkFont(size=14))
        entry.pack(fill="x", padx=10, pady=(0, 10))
        entry.insert(0, default_text)
        return entry


    def _select_image(self):
        path = filedialog.askopenfilename(title="Seleccione una imagen",
                                          filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if path:
            self.user_image_path = path
            messagebox.showinfo("Imagen Seleccionada", os.path.basename(path))


    def _save_changes(self):
        new_name = self.entry_name.get().strip()
        new_role = self.combobox_role.get()

        if not new_name or not new_role:
            messagebox.showwarning("Faltan Datos", "Nombre y rol son obligatorios.")
            return

        profile_image_path = self.user_data["foto_path"]
        if self.user_image_path:
            filename = f"{self.user_data['username']}_{os.path.basename(self.user_image_path)}"
            dest_path = os.path.join(USER_IMAGES_DIR, filename)
            try:
                shutil.copy(self.user_image_path, dest_path)
                profile_image_path = dest_path
            except Exception as e:
                messagebox.showerror("Error guardando imagen", str(e))
                return

        success = self.user_management.update_user_details(
            self.user_id, self.user_data["username"], new_name, new_role, profile_image_path)

        if success:
            messagebox.showinfo("Usuario Actualizado", f"Datos de {new_name} guardados exitosamente.")
            self.refresh_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "Error guardando los datos del usuario.")


    def _open_change_password(self):
        from .change_password import ChangePasswordWindow
        ChangePasswordWindow(self.master, self.user_management, self.user_id, self.user_data["username"])
