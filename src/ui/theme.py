# theme.py

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

# Fuentes y tamaños
FONT_FAMILY = "Segoe UI"
FONT_BOLD_LARGE = (FONT_FAMILY, 26, "bold")
FONT_BOLD_MEDIUM = (FONT_FAMILY, 22, "bold")
FONT_BOLD_SMALL = (FONT_FAMILY, 16, "bold")
FONT_REGULAR_LARGE = (FONT_FAMILY, 18)
FONT_REGULAR_MEDIUM = (FONT_FAMILY, 14)
FONT_REGULAR_SMALL = (FONT_FAMILY, 12)

# Estilos para widgets
BUTTON_STYLE_DEFAULT = {
    "corner_radius": 8,
    "fg_color": BUTTON_FG_COLOR,
    "hover_color": BUTTON_HOVER_COLOR,
    "text_color": TEXT_COLOR_PRIMARY,
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

# Formatos de fecha y hora
DATE_FORMAT = "%d %b, %Y"
TIME_FORMAT = "%I:%M %p"
