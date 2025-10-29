# currency_model.py

import sqlite3
from datetime import datetime
import os

DB_PATH = os.path.abspath("profitus.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

# ---------- TASAS ----------
def crear_tabla_tasas_si_no_existe():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasas (
            tipo_tasa TEXT PRIMARY KEY,
            valor REAL,
            fecha_actualizacion TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_tasas(bcv, paralela):
    conn = get_connection()
    cursor = conn.cursor()
    crear_tabla_tasas_si_no_existe()
    fecha = datetime.now().isoformat(sep=' ', timespec='seconds')
    cursor.execute("""
        INSERT INTO tasas (tipo_tasa, valor, fecha_actualizacion)
        VALUES (?, ?, ?)
        ON CONFLICT(tipo_tasa) DO UPDATE SET
            valor=excluded.valor,
            fecha_actualizacion=excluded.fecha_actualizacion
    """, ("BCV", bcv, fecha))
    cursor.execute("""
        INSERT INTO tasas (tipo_tasa, valor, fecha_actualizacion)
        VALUES (?, ?, ?)
        ON CONFLICT(tipo_tasa) DO UPDATE SET
            valor=excluded.valor,
            fecha_actualizacion=excluded.fecha_actualizacion
    """, ("PARALELA", paralela, fecha))
    conn.commit()
    conn.close()

def get_tasa(tipo):
    conn = get_connection()
    cursor = conn.cursor()
    crear_tabla_tasas_si_no_existe()
    cursor.execute("SELECT valor FROM tasas WHERE tipo_tasa = ?", (tipo,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else ""

# ---------- MÉTODOS DE PAGO ----------
def add_metodo_pago(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metodos_pago (
            nombre TEXT PRIMARY KEY
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO metodos_pago (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()

def get_metodos_pago():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS metodos_pago (
            nombre TEXT PRIMARY KEY
        )
    """)
    cursor.execute("SELECT nombre FROM metodos_pago")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def delete_metodo_pago(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM metodos_pago WHERE nombre = ?", (nombre,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

# ---------- BANCOS ----------
def add_banco(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bancos (
            nombre TEXT PRIMARY KEY
        )
    """)
    cursor.execute("INSERT OR IGNORE INTO bancos (nombre) VALUES (?)", (nombre,))
    conn.commit()
    conn.close()

def get_bancos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bancos (
            nombre TEXT PRIMARY KEY
        )
    """)
    cursor.execute("SELECT nombre FROM bancos")
    rows = cursor.fetchall()
    conn.close()
    return [r[0] for r in rows]

def delete_banco(nombre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bancos WHERE nombre = ?", (nombre,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
