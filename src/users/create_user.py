import os
import shutil
import customtkinter as ctk
from tkinter import messagebox, filedialog
from ..config.settings import USER_IMAGES_DIR  # Importar ruta fija

# AGREGADO: Importa la función de roles
from src.security.authorization import tiene_permiso

class CreateUserWindow(ctk.CTkToplevel):
    def __init__(self, master, user_management, refresh_callback, user_actual_rol=None):
        super().__init__(master)
        self.user_management = user_management
        self.refresh_callback = refresh_callback
        self.user_image_path = None
        self.user_actual_rol = user_actual_rol  # AGREGADO: recibir el rol del usuario actual

        self.title("Crear Nuevo Usuario")
        self.geometry("600x520")
        self.transient(master)
        self.grab_set()
        self.resizable(False, False)

        self._create_widgets()

    def _create_widgets(self):
        ctk.CTkLabel(self, text="Crear Usuario Nuevo",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="#00FFFF").pack(pady=15)

        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=10, padx=20, fill="x")

        self.entry_username = self._add_labeled_entry("Usuario (Login):")
        self.entry_password = self._add_labeled_entry("Contraseña:", show="*")
        self.entry_name = self._add_labeled_entry("Nombre Completo:")

        ctk.CTkLabel(self.frame_form, text="Rol Asignado:").pack(anchor="w", padx=10, pady=(12, 0))
        self.combobox_role = ctk.CTkComboBox(self.frame_form,
                                             values=["Vendedor", "Gerente", "administrador total", "desarrollador"],
                                             state="readonly")
        self.combobox_role.set("Vendedor")
        self.combobox_role.pack(fill="x", padx=10, pady=(0, 15))

        ctk.CTkLabel(self.frame_form, text="Foto de Perfil (opcional):").pack(anchor="w", padx=10, pady=(12, 0))
        btn_select_image = ctk.CTkButton(self.frame_form, text="Seleccionar Imagen", command=self._select_image)
        btn_select_image.pack(padx=10, pady=(0, 10))

        btn_create = ctk.CTkButton(self, text="Crear Usuario",
                                   fg_color="#00C853", text_color="#001122",
                                   font=ctk.CTkFont(size=18, weight="bold"),
                                   command=self._create_user)
        btn_create.pack(pady=10, padx=40, fill="x")

    def _add_labeled_entry(self, label, show=None):
        ctk.CTkLabel(self.frame_form, text=label).pack(anchor="w", padx=10, pady=(6, 0))
        entry = ctk.CTkEntry(self.frame_form, font=ctk.CTkFont(size=14), show=show)
        entry.pack(fill="x", padx=10, pady=(0, 10))
        return entry

    def _select_image(self):
        path = filedialog.askopenfilename(
            title="Seleccione una imagen",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if path:
            self.user_image_path = path
            messagebox.showinfo("Imagen Seleccionada", f"{os.path.basename(path)}")

    def _create_user(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()
        nombre_completo = self.entry_name.get().strip()
        rol = self.combobox_role.get()

        # AGREGADO: Validación de PERMISO SEGÚN ROL
        if not tiene_permiso(self.user_actual_rol, "crear_usuario"):
            messagebox.showerror("Restricción de permisos", "No tienes permisos para crear usuarios.")
            return

        if not (username and password and nombre_completo and rol):
            messagebox.showwarning("Datos Faltantes", "Todos los campos son obligatorios excepto la foto.")
            return

        from hashlib import sha256
        password_hashed = sha256(password.encode("utf-8")).hexdigest()

        foto_path = None
        if self.user_image_path:
            file_dest = os.path.join(USER_IMAGES_DIR, f"{username}_{os.path.basename(self.user_image_path)}")
            try:
                shutil.copy(self.user_image_path, file_dest)
                foto_path = file_dest
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo copiar la imagen: {e}")
                return

        success = self.user_management.create_user(username, password_hashed, nombre_completo, rol, foto_path)
        if success:
            messagebox.showinfo("Usuario creado", f"Usuario {username} creado correctamente.")
            self.refresh_callback()
            self.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario. Puede que el usuario ya exista.")
