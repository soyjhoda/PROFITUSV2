import customtkinter as ctk
from PIL import Image
import os
import datetime
from tkinter import filedialog
import shutil
from .config_page import ConfigPage
from src.ui.theme import (
    BACKGROUND_COLOR, FONT_BOLD_MEDIUM, SIDEBAR_COLOR, SIDEBAR_BUTTON_DEFAULT, SIDEBAR_BUTTON_HOVER,
    TOPBAR_COLOR, TEXT_COLOR_PRIMARY, TEXT_COLOR_SECONDARY,
    BUTTON_STYLE_DEFAULT, LABEL_STYLE_HEADER, LABEL_STYLE_SUBHEADER,
    FONT_BOLD_SMALL, FONT_REGULAR_MEDIUM, FONT_REGULAR_SMALL,
    LOGO_PROFITUS_PATH,
    DATE_FORMAT, TIME_FORMAT
)


NOMBRE_NEGOCIO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "logo-cliente", "nombre_negocio.txt")


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, user_data, user_management=None, logo_cliente_path="", on_logout=None):
        super().__init__(master)
        self.pack(fill='both', expand=True)

        self.user_data = user_data
        self.user_management = user_management  # Guardar la instancia real aquí
        self.logo_cliente_path = logo_cliente_path
        self.theme_mode = "dark"
        self.menu_expanded = True
        self.nombre_negocio = self._cargar_nombre_negocio()
        self.configure(fg_color=BACKGROUND_COLOR)

        self.topbar_frame = None
        self.sidebar = None
        self.main_panel = None

        self.on_logout = on_logout  # Callback para cerrar sesión

        self._create_topbar()
        self._create_sidebar()
        self._create_main_panel()

    def cerrar_sesion(self):
        if self.on_logout:
            self.on_logout()
        self.destroy()

    def mostrar_configuracion(self):
        if self.main_panel is not None:
            self.main_panel.destroy()
        # PASAMOS la instancia real de user_management aquí
        self.main_panel = ConfigPage(self, user_management=self.user_management, on_close=self._create_main_panel)
        self.main_panel.place(x=190, y=55, relwidth=1.0, relheight=1.0, anchor='nw')
        self.main_panel.place_configure(relwidth=1.0, relheight=1.0)

    def _cargar_nombre_negocio(self):
        if os.path.exists(NOMBRE_NEGOCIO_PATH):
            with open(NOMBRE_NEGOCIO_PATH, "r", encoding="utf-8") as f:
                return f.read().strip() or "Mi Negocio"
        return "Mi Negocio"

    def _guardar_nombre_negocio(self):
        with open(NOMBRE_NEGOCIO_PATH, "w", encoding="utf-8") as f:
            f.write(self.entry_nombre_negocio.get().strip())
        self.nombre_negocio = self.entry_nombre_negocio.get().strip() or "Mi Negocio"
        self.label_nombre_negocio.configure(text=self.nombre_negocio)
        self.entry_nombre_negocio.pack_forget()
        self.btn_guardar_nombre.pack_forget()
        self.label_nombre_negocio.pack(side="left", padx=(0, 10))

    def _edit_nombre_negocio(self, event):
        self.label_nombre_negocio.pack_forget()
        self.entry_nombre_negocio.delete(0, "end")
        self.entry_nombre_negocio.insert(0, self.nombre_negocio)
        self.entry_nombre_negocio.pack(side="left", padx=(0, 10))
        self.btn_guardar_nombre.pack(side="left")

    def _create_topbar(self):
        if self.topbar_frame is not None:
            self.topbar_frame.destroy()
        self.topbar_frame = ctk.CTkFrame(self, height=55, fg_color=TOPBAR_COLOR)
        self.topbar_frame.place(x=0, y=0, relwidth=1.0)

        bar = self.topbar_frame

        if self.logo_cliente_path and os.path.exists(self.logo_cliente_path):
            img_logo = Image.open(self.logo_cliente_path).resize((38, 38))
            self.logo_topbar = ctk.CTkImage(img_logo, size=(38, 38))
            logo_label = ctk.CTkLabel(bar, image=self.logo_topbar, text="", fg_color=TOPBAR_COLOR)
            logo_label.pack(side="left", padx=(10, 4), pady=8)
        else:
            logo_label = None

        nombre_frame = ctk.CTkFrame(bar, fg_color=TOPBAR_COLOR)
        nombre_frame.pack(side="left", padx=(0, 20), pady=2)

        self.label_nombre_negocio = ctk.CTkLabel(
            nombre_frame,
            text=self.nombre_negocio,
            **LABEL_STYLE_HEADER,
            fg_color=TOPBAR_COLOR
        )
        self.label_nombre_negocio.pack(side="left")
        self.label_nombre_negocio.bind("<Double-1>", self._edit_nombre_negocio)

        self.entry_nombre_negocio = ctk.CTkEntry(
            nombre_frame,
            font=FONT_REGULAR_MEDIUM,
            width=180
        )
        self.btn_guardar_nombre = ctk.CTkButton(
            nombre_frame,
            text="Guardar",
            width=68,
            command=self._guardar_nombre_negocio,
            **BUTTON_STYLE_DEFAULT
        )
        mode_btn = ctk.CTkButton(
            bar,
            text="🌗",
            width=35,
            height=35,
            fg_color=TOPBAR_COLOR,
            command=self._toggle_mode
        )
        mode_btn.pack(side="right", padx=9, pady=6)

        now = datetime.datetime.now()
        fecha_label = ctk.CTkLabel(
            bar,
            text=now.strftime(DATE_FORMAT),
            font=FONT_REGULAR_MEDIUM,
            fg_color=TOPBAR_COLOR
        )
        fecha_label.pack(side="right", padx=15)

        hora_label = ctk.CTkLabel(
            bar,
            text=now.strftime(TIME_FORMAT),
            font=FONT_REGULAR_MEDIUM,
            fg_color=TOPBAR_COLOR
        )
        hora_label.pack(side="right")

        try:
            user_name = self.user_data["nombre_completo"]
        except (KeyError, TypeError):
            user_name = "Usuario"
        avatar_label = ctk.CTkLabel(
            bar,
            text="👤",
            font=FONT_BOLD_SMALL,
            fg_color=TOPBAR_COLOR
        )
        avatar_label.pack(side="right", padx=(22, 2))
        user_label = ctk.CTkLabel(
            bar,
            text=f"{user_name}",
            font=FONT_REGULAR_MEDIUM,
            fg_color=TOPBAR_COLOR
        )
        user_label.pack(side="right", padx=(0, 7))

    def _toggle_mode(self):
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        ctk.set_appearance_mode(self.theme_mode)

    def _create_sidebar(self):
        if self.sidebar is not None:
            self.sidebar.destroy()
        self.sidebar = ctk.CTkFrame(self, fg_color=SIDEBAR_COLOR, width=190)
        self.sidebar.place(x=0, y=55, relheight=1.0, anchor="nw")

        self.menu_toggle = ctk.CTkButton(
            self.sidebar,
            text="≡",
            width=36,
            height=36,
            fg_color=SIDEBAR_COLOR,
            command=self._toggle_sidebar
        )
        self.menu_toggle.place(x=142, y=12)

        self.menu_buttons = []
        menus = [("HOME", "🏠"), ("POS", "🛒"), ("INVENTARIO", "📦"),
                 ("COMPRAS", "🧾"), ("GESTION", "📋")]

        y_start = 58
        spacing = 54

        for i, (txt, icon) in enumerate(menus):
            btn = ctk.CTkButton(
                self.sidebar,
                corner_radius=8,
                height=42,
                width=142,
                text=f"{icon} {txt}",
                font=FONT_REGULAR_MEDIUM,
                fg_color=SIDEBAR_BUTTON_DEFAULT,
                hover_color=SIDEBAR_BUTTON_HOVER,
                bg_color=SIDEBAR_COLOR,
                command=lambda t=txt: self._activate_menu(t)
            )
            btn.place(x=20, y=y_start + i * spacing)
            self.menu_buttons.append(btn)

        self._activate_menu("HOME")

        account_text_y = y_start + len(menus) * spacing + 110
        ctk.CTkLabel(
            self.sidebar,
            text="ACCOUNT DETAILS",
            font=FONT_REGULAR_SMALL,
            fg_color=SIDEBAR_COLOR,
            text_color="#4F5D7A",
            underline=True
        ).place(x=29, y=account_text_y)

        acciones = [("Perfil", "👤"), ("Configuración", "⚙️"), ("Cambiar logo", "🖼️"), ("Cerrar Sesión", "🔒")]
        y_acc = account_text_y + 50
        self.acciones_buttons = []
        for name, icon in acciones:
            b = ctk.CTkButton(
                self.sidebar,
                corner_radius=7,
                height=30,
                width=142,
                text=f"{icon} {name}",
                font=FONT_REGULAR_MEDIUM,
                fg_color=BUTTON_STYLE_DEFAULT["fg_color"],
                hover_color=BUTTON_STYLE_DEFAULT["hover_color"],
                bg_color=SIDEBAR_BUTTON_DEFAULT,
            )
            if name == "Cerrar Sesión":
                b.configure(command=self.cerrar_sesion)
            if name == "Cambiar logo":
                b.configure(command=self.seleccionar_logo)
            if name == "Configuración":
                b.configure(command=self.mostrar_configuracion)
            b.place(x=20, y=y_acc)
            y_acc += 39
            self.acciones_buttons.append(b)

        if os.path.exists(LOGO_PROFITUS_PATH):
            profitus_img = Image.open(LOGO_PROFITUS_PATH).resize((150, 150))
            self.profitus_logo = ctk.CTkImage(profitus_img, size=(150, 150))
            logo_label = ctk.CTkLabel(self.sidebar, image=self.profitus_logo, text="", fg_color=SIDEBAR_COLOR)
            logo_label.place(relx=0.5, rely=1.0, anchor="s", y=-120)

    def _toggle_sidebar(self):
        new_width = 52 if self.menu_expanded else 190
        self.menu_expanded = not self.menu_expanded
        self.sidebar.configure(width=new_width)
        for btn in self.menu_buttons:
            btn.configure(width=(16 if not self.menu_expanded else 142))
            btn.configure(font=FONT_REGULAR_MEDIUM if self.menu_expanded else FONT_REGULAR_SMALL)
            if not self.menu_expanded:
                btn.configure(text=btn.cget('text').split(' ')[0])
            else:
                parts = btn.cget('text').split(' ')
                if len(parts) < 2:
                    continue
                else:
                    icon, txt = parts[0], parts[1]
                btn.configure(text=f"{icon} {txt}")
        self.menu_toggle.place(x=(5 if not self.menu_expanded else 142), y=12)

    def _activate_menu(self, menu_name):
        if self.main_panel is not None and isinstance(self.main_panel, ConfigPage):
            self.main_panel.destroy()
            self._create_main_panel()
        for btn in self.menu_buttons:
            if menu_name in btn.cget('text'):
                btn.configure(fg_color=SIDEBAR_BUTTON_HOVER)
            else:
                btn.configure(fg_color=SIDEBAR_BUTTON_DEFAULT)

    def _create_main_panel(self):
        if hasattr(self, "main_panel") and self.main_panel is not None:
            self.main_panel.destroy()

        self.main_panel = ctk.CTkFrame(self, fg_color=BACKGROUND_COLOR)
        self.main_panel.place(x=190, y=55, relwidth=1.0, relheight=1.0, anchor="nw")

        try:
            nombre = self.user_data["nombre_completo"]
        except (KeyError, TypeError):
            nombre = "Usuario"
        try:
            rol = self.user_data["rol"]
        except (KeyError, TypeError):
            rol = "Sin rol"

        welcome = ctk.CTkLabel(
            self.main_panel,
            text="Bienvenido",
            **LABEL_STYLE_HEADER,
            fg_color=BACKGROUND_COLOR
        )
        welcome.pack(pady=(35, 8))
        rol_label = ctk.CTkLabel(
            self.main_panel,
            text=f"{nombre}: Rol {rol}.",
            **LABEL_STYLE_SUBHEADER,
            fg_color=BACKGROUND_COLOR
        )
        rol_label.pack(pady=(0, 22))

        if self.logo_cliente_path and os.path.exists(self.logo_cliente_path):
            img_c = Image.open(self.logo_cliente_path)
            self.c_logo = ctk.CTkImage(img_c, size=(320, 320))
            self.logo_cliente_label = ctk.CTkLabel(self.main_panel, image=self.c_logo, text="", fg_color=BACKGROUND_COLOR)
            self.logo_cliente_label.pack(pady=(0, 18))
            self.logo_cliente_label.bind("<Button-1>", lambda e: self.seleccionar_logo())
        else:
            self.logo_cliente_label = ctk.CTkLabel(
                self.main_panel,
                text="SIN LOGO",
                font=FONT_BOLD_MEDIUM,
                fg_color=BACKGROUND_COLOR
            )
            self.logo_cliente_label.pack(pady=40)
            self.logo_cliente_label.bind("<Button-1>", lambda e: self.seleccionar_logo())

    def seleccionar_logo(self):
        ruta = filedialog.askopenfilename(
            title="Seleccione el logo",
            filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if ruta:
            destino_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "logo-cliente")
            if not os.path.exists(destino_dir):
                os.makedirs(destino_dir)
            destino = os.path.join(destino_dir, "logo.png")
            shutil.copyfile(ruta, destino)
            self.logo_cliente_path = destino
            self._create_topbar()
            self._create_main_panel()
