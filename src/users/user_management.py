from src.security.authorization import tiene_permiso  # ← [Mejora de seguridad de roles]

class UserManagement:
    def __init__(self, db):
        self.db = db

    def get_all_users(self):
        query = "SELECT * FROM usuarios"
        return self.db.fetch_all(query)

    def fetch_one(self, query, params=()):
        return self.db.fetch_one(query, params)

    def create_user(self, username, password_hashed, nombre_completo, rol, foto_path=None, creador_rol=None):
        # [Mejora de seguridad] Validar permiso de crear usuario según el rol del usuario que ejecuta la acción
        # Esta mejora exige pasar el rol del usuario actual como 'creador_rol' (adaptar llamada desde interfaz)
        if creador_rol is not None and not tiene_permiso(creador_rol, "crear_usuario"):
            # Si no tiene permiso, no se crea el usuario
            return False

        try:
            self.db.execute(
                "INSERT INTO usuarios (username, password, nombre_completo, rol, foto_path) VALUES (?, ?, ?, ?, ?)",
                (username, password_hashed, nombre_completo, rol, foto_path)
            )
            return True
        except Exception:
            return False

    def update_user_details(self, user_id, username, nombre_completo, rol, foto_path):
        try:
            self.db.execute(
                "UPDATE usuarios SET nombre_completo = ?, rol = ?, foto_path = ? WHERE id=? AND username=?",
                (nombre_completo, rol, foto_path, user_id, username)
            )
            return True
        except Exception:
            return False

    def update_user_password(self, user_id, new_password_hashed):
        try:
            self.db.execute(
                "UPDATE usuarios SET password = ? WHERE id = ?", (new_password_hashed, user_id)
            )
            return True
        except Exception:
            return False

    def update_user_role(self, user_id, new_role):
        try:
            self.db.execute(
                "UPDATE usuarios SET rol = ? WHERE id = ?", (new_role, user_id)
            )
            return True
        except Exception:
            return False

    def delete_user(self, user_id):
        """Elimina el usuario especificado por su id."""
        try:
            self.db.execute(
                "DELETE FROM usuarios WHERE id = ?", (user_id,)
            )
            return True
        except Exception:
            return False

    def get_user_by_username(self, username):
        query = "SELECT * FROM usuarios WHERE username = ?"
        return self.db.fetch_one(query, (username,))
