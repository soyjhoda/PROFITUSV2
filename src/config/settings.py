import os

# Definir ruta absoluta fija dentro del proyecto para imágenes de usuario
USER_IMAGES_DIR = r"C:\Proyectos\ERP_LITE_PYME_V2\assets\imagen-usuarios"

# Crear carpeta si no existe para evitar errores
if not os.path.exists(USER_IMAGES_DIR):
    os.makedirs(USER_IMAGES_DIR)
