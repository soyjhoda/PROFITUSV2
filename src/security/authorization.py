# src/security/authorization.py

"""
----------------------------------------------------------
    Módulo de Autorización y Permisos por Rol
----------------------------------------------------------

Contiene la lógica central para validar qué permisos tiene cada rol del sistema
sin modificar ni afectar la lógica de otros módulos.
----------------------------------------------------------
"""

# Diccionario de permisos por rol
PERMISOS_POR_ROL = {
    "administrador total": {
        "crear_usuario", "editar_usuario", "eliminar_usuario",
        "crear_producto", "editar_producto", "eliminar_producto",
        "ver_inventario", "modificar_inventario",
        "configuracion_general",
        "ver_reportes"
    },
    "desarrollador": {
        "crear_usuario", "editar_usuario", "eliminar_usuario",
        "crear_producto", "editar_producto", "eliminar_producto",
        "ver_inventario", "modificar_inventario",
        "configuracion_general",
        "ver_reportes"
    },
    "gerente": {
        "crear_usuario", "editar_usuario",
        "crear_producto", "editar_producto",
        "ver_inventario", "modificar_inventario",
        "ver_reportes"
    },
    "vendedor": {
        "ver_inventario"
    }
}

def tiene_permiso(rol, accion):
    """
    ------------------------------------------------------
    Función que valida si un rol tiene permiso sobre acción
    ------------------------------------------------------

    Args:
        rol (str): Rol del usuario (administrador total, gerente, vendedor, desarrollador)
        accion (str): Acción a validar (ej: 'crear_usuario', 'modificar_inventario')

    Returns:
        bool: True si tiene permiso, False si NO lo tiene
    ------------------------------------------------------
    """
    rol = str(rol).lower() if rol else ""
    permisos_rol = PERMISOS_POR_ROL.get(rol, set())
    return accion in permisos_rol
