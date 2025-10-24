"""
Archivo base para definir estilos, colores, fuentes y recursos visuales
de toda la aplicación para mantener coherencia y facilitar mantenimiento.
"""

import os

# Colores
BACKGROUND_COLOR = "#1b1440"
SIDEBAR_COLOR = "#000000"
SIDEBAR_BUTTON_DEFAULT = "#231B44"
SIDEBAR_BUTTON_HOVER = "#4113AE"
SIDEBAR_BUTTON_ACTIVE = "#81E821"
TOPBAR_COLOR = "#000000"
TEXT_COLOR_PRIMARY = "#FFFFFF"
TEXT_COLOR_SECONDARY = "#81E821"
BUTTON_FG_COLOR = "#4113AE"
BUTTON_HOVER_COLOR = "#511ABE"

# Colores para botones pestañas personalizados
TAB_BUTTON_BG_COLOR = BUTTON_FG_COLOR
TAB_BUTTON_HOVER_COLOR = BUTTON_HOVER_COLOR
TAB_BUTTON_TEXT_COLOR = TEXT_COLOR_PRIMARY

# Fuentes y tamaños
FONT_FAMILY = "Segoe UI"
FONT_BOLD_LARGE = (FONT_FAMILY, 26, "bold")
FONT_BOLD_MEDIUM = (FONT_FAMILY, 22, "bold")
FONT_BOLD_SMALL = (FONT_FAMILY, 16, "bold")
FONT_REGULAR_LARGE = (FONT_FAMILY, 18)
FONT_REGULAR_MEDIUM = (FONT_FAMILY, 14)
FONT_REGULAR_SMALL = (FONT_FAMILY, 12)

# Estilos de tabla para usar en Treeview
TREE_FONT = ("Segoe UI", 13)
TREE_FONT_HEADER = ("Segoe UI Semibold", 14, "bold")
TREE_BG_COLOR = "#232150"
TREE_HEADER_BG_COLOR = "#231B44"
TREE_HEADER_FG_COLOR = "#84ff00"
TREE_FG_COLOR = "#00ffcc"
TREE_ROW_HEIGHT = 34
TREE_SELECTED_COLOR = "#36408B"

# Estilos para widgets
BUTTON_STYLE_DEFAULT = {
    "corner_radius": 8,
    "fg_color": BUTTON_FG_COLOR,
    "hover_color": BUTTON_HOVER_COLOR,
    "text_color": TEXT_COLOR_PRIMARY,
}

TAB_BUTTON_STYLE = {
    "corner_radius": 12,
    "width": 180,
    "height": 60,
    "fg_color": TAB_BUTTON_BG_COLOR,
    "hover_color": TAB_BUTTON_HOVER_COLOR,
    "text_color": TAB_BUTTON_TEXT_COLOR,
    "font": FONT_BOLD_MEDIUM,
}

LABEL_STYLE_HEADER = {
    "font": FONT_BOLD_LARGE,
    "text_color": TEXT_COLOR_PRIMARY,
}

LABEL_STYLE_SUBHEADER = {
    "font": FONT_BOLD_MEDIUM,
    "text_color": TEXT_COLOR_SECONDARY,
}

LABEL_STYLE_NORMAL = {
    "font": FONT_REGULAR_MEDIUM,
    "text_color": TEXT_COLOR_PRIMARY,
}

# Rutas
BASE_ASSETS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'assets')
LOGO_PROFITUS_PATH = os.path.join(BASE_ASSETS_PATH, 'logo-app', 'logo.png')
LOGO_CLIENTE_PATH = os.path.join(BASE_ASSETS_PATH, 'logo-cliente', 'logo.png')

# Ruta para la imagen del botón gestión de usuarios
ICON_BTN_USUARIOS_PATH = os.path.join(BASE_ASSETS_PATH, 'iconos', 'btnusuarios.png')

# Formatos de fecha y hora
DATE_FORMAT = "%d %b, %Y"
TIME_FORMAT = "%I:%M %p"
