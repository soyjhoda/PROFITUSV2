import sqlite3
import os
import shutil
from tkinter import messagebox

class DBManager:
    def __init__(self, db_path='profitus.db'):
        self.db_path = db_path
        self.connection = None
        self._connect()
        self._create_tables()

    def _connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            messagebox.showerror("DB Error", f"No se pudo conectar a la base de datos: {e}")

    def _create_tables(self):
        try:
            cursor = self.connection.cursor()

            # Tabla usuarios
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    nombre_completo TEXT NOT NULL,
                    rol TEXT NOT NULL,
                    foto_path TEXT NULL
                );
            ''')

            # Tabla proveedores (básica)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS proveedores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    telefono TEXT,
                    email TEXT,
                    direccion TEXT
                );
            ''')

            # Tabla productos como ejemplo (incluye id_proveedor como FK)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS productos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT,
                    precio REAL NOT NULL,
                    stock INTEGER NOT NULL,
                    id_proveedor INTEGER,
                    FOREIGN KEY (id_proveedor) REFERENCES proveedores(id)
                );
            ''')

            self.connection.commit()
        except sqlite3.Error as e:
            messagebox.showerror("DB Error", f"No se pudieron crear las tablas: {e}")

    def fetch_all(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=()):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()

    def execute(self, query, params=()):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("DB Error", f"Error de base de datos: {e}")
            return False

    def create_backup(self, destination_path):
        try:
            self.connection.commit()
            self.connection.close()
            if os.path.exists(self.db_path):
                shutil.copy(self.db_path, destination_path)
            else:
                return False, "Archivo de base de datos no encontrado."
            self._connect()
            return True, "Backup creado correctamente."
        except Exception as e:
            return False, str(e)

    def restore_backup(self, source_path):
        try:
            self.connection.close()
            shutil.copy(source_path, self.db_path)
            self._connect()
            return True, "Base de datos restaurada con éxito."
        except Exception as e:
            return False, str(e)
