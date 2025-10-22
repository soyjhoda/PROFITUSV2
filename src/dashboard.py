import customtkinter as ctk
from PIL import Image
import os
import datetime
from tkinter import filedialog
import shutil
from .config_page import ConfigPage

NOMBRE_NEGOCIO_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "logo-cliente", "nombre_negocio.txt")
LOGO_PROFITUS_PATH = r"C:\Proyectos\ERP_LITE_PYME_V2\assets\logo-app\logo.png"


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, user_data, logo_cliente_path="", on_logout=None):
        super().__init__(master)
        self.pack(fill='both', expand=True)

        self.user_data = user_data
        self.logo_cliente_path = logo_cliente_path
        self.theme_mode = "dark"
        self.menu_expanded = True
        self.nombre_negocio = self._cargar_nombre_negocio()
        self.configure(fg_color="#1b1440")

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
        # Al abrir configuración, pásale el callback para regresar al panel principal
        self.main_panel = ConfigPage(self, user_management=None, on_close=self._create_main_panel)
        # Ubicar main panel a la derecha de sidebar
        self.main_panel.place(x=190, y=55, relwidth=1.0, relheight=1.0, anchor='nw')
        # Ajustar tamaño sin tapar sidebar
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
        self.topbar_frame = ctk.CTkFrame(self, height=55, fg_color="#000000")
        self.topbar_frame.place(x=0, y=0, relwidth=1.0)

        bar = self.topbar_frame

        if self.logo_cliente_path and os.path.exists(self.logo_cliente_path):
            img_logo = Image.open(self.logo_cliente_path).resize((38, 38))
            self.logo_topbar = ctk.CTkImage(img_logo, size=(38, 38))
            logo_label = ctk.CTkLabel(bar, image=self.logo_topbar, text="", fg_color="#000000")
            logo_label.pack(side="left", padx=(10, 4), pady=8)
        else:
            logo_label = None

        nombre_frame = ctk.CTkFrame(bar, fg_color="#000000")
        nombre_frame.pack(side="left", padx=(0, 20), pady=2)
        self.label_nombre_negocio = ctk.CTkLabel(nombre_frame, text=self.nombre_negocio,
                                                 font=ctk.CTkFont(size=19, weight="bold"), fg_color="#000000")
        self.label_nombre_negocio.pack(side="left")
        self.label_nombre_negocio.bind("<Double-1>", self._edit_nombre_negocio)
        self.entry_nombre_negocio = ctk.CTkEntry(nombre_frame, font=ctk.CTkFont(size=16), width=180)
        self.btn_guardar_nombre = ctk.CTkButton(nombre_frame, text="Guardar", width=68,
                                                font=ctk.CTkFont(size=14), command=self._guardar_nombre_negocio)
        mode_btn = ctk.CTkButton(bar, text="🌗", width=35, height=35, fg_color="#000000", command=self._toggle_mode)
        mode_btn.pack(side="right", padx=9, pady=6)
        now = datetime.datetime.now()
        fecha_label = ctk.CTkLabel(bar, text=now.strftime("%d %b, %Y"), font=ctk.CTkFont(size=14), fg_color="#000000")
        fecha_label.pack(side="right", padx=15)
        hora_label = ctk.CTkLabel(bar, text=now.strftime("%I:%M %p"), font=ctk.CTkFont(size=14), fg_color="#000000")
        hora_label.pack(side="right")

        try:
            user_name = self.user_data["nombre_completo"]
        except (KeyError, TypeError):
            user_name = "Usuario"
        avatar_label = ctk.CTkLabel(bar, text="👤", font=ctk.CTkFont(size=19), fg_color="#000000")
        avatar_label.pack(side="right", padx=(22, 2))
        user_label = ctk.CTkLabel(bar, text=f"{user_name}", font=ctk.CTkFont(size=13), fg_color="#000000")
        user_label.pack(side="right", padx=(0, 7))

    def _toggle_mode(self):
        self.theme_mode = "light" if self.theme_mode == "dark" else "dark"
        ctk.set_appearance_mode(self.theme_mode)

    def _create_sidebar(self):
        if self.sidebar is not None:
            self.sidebar.destroy()
        self.sidebar = ctk.CTkFrame(self, fg_color="#000000", width=190)
        self.sidebar.place(x=0, y=55, relheight=1.0, anchor="nw")

        self.menu_toggle = ctk.CTkButton(self.sidebar, text="≡", width=36, height=36, fg_color="#000000",
                                         command=self._toggle_sidebar)
        self.menu_toggle.place(x=142, y=12)

        self.menu_buttons = []
        menus = [("HOME", "🏠"), ("POS", "🛒"), ("INVENTARIO", "📦"),
                 ("COMPRAS", "🧾"), ("GESTION", "📋")]

        y_start = 58
        spacing = 54

        for i, (txt, icon) in enumerate(menus):
            btn = ctk.CTkButton(self.sidebar, corner_radius=8, height=42, width=142,
                                text=f"{icon} {txt}",
                                font=ctk.CTkFont(size=16),
                                fg_color="#000000",
                                hover_color="#222222",
                                bg_color="#000000",
                                command=lambda t=txt: self._activate_menu(t))
            btn.place(x=20, y=y_start + i * spacing)
            self.menu_buttons.append(btn)

        self._activate_menu("HOME")

        account_text_y = y_start + len(menus) * spacing + 110
        ctk.CTkLabel(self.sidebar, text="ACCOUNT DETAILS", font=ctk.CTkFont(size=13, underline=True),
                     text_color="#4F5D7A", fg_color="#000000").place(x=29, y=account_text_y)

        acciones = [("Perfil", "👤"), ("Configuración", "⚙️"), ("Cambiar logo", "🖼️"), ("Cerrar Sesión", "🔒")]
        y_acc = account_text_y + 50
        self.acciones_buttons = []
        for name, icon in acciones:
            b = ctk.CTkButton(self.sidebar, corner_radius=7, height=30, width=142,
                              text=f"{icon} {name}",
                              font=ctk.CTkFont(size=14),
                              fg_color="#4113AE",
                              hover_color="#511ABE",
                              bg_color="#231B44")
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
            logo_label = ctk.CTkLabel(self.sidebar, image=self.profitus_logo, text="", fg_color="#000000")
            logo_label.place(relx=0.5, rely=1.0, anchor="s", y=-120)

    def _toggle_sidebar(self):
        new_width = 52 if self.menu_expanded else 190
        self.menu_expanded = not self.menu_expanded
        self.sidebar.configure(width=new_width)
        for btn in self.menu_buttons:
            btn.configure(width=(16 if not self.menu_expanded else 142))
            btn.configure(font=ctk.CTkFont(size=(14 if not self.menu_expanded else 16)))
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
        # Cuando selecciones otro menú, cerrar configuración si está abierta
        if self.main_panel is not None and isinstance(self.main_panel, ConfigPage):
            self.main_panel.destroy()
            self._create_main_panel()
        for btn in self.menu_buttons:
            if menu_name in btn.cget('text'):
                btn.configure(fg_color="#4113AE")
            else:
                btn.configure(fg_color="#231B44")

    def _create_main_panel(self):
        if hasattr(self, "main_panel") and self.main_panel is not None:
            self.main_panel.destroy()

        self.main_panel = ctk.CTkFrame(self, fg_color="#1b1440")
        self.main_panel.place(x=190, y=55, relwidth=1.0, relheight=1.0, anchor="nw")

        try:
            nombre = self.user_data["nombre_completo"]
        except (KeyError, TypeError):
            nombre = "Usuario"
        try:
            rol = self.user_data["rol"]
        except (KeyError, TypeError):
            rol = "Sin rol"

        welcome = ctk.CTkLabel(self.main_panel, text="Bienvenido", font=ctk.CTkFont(size=30, weight="bold"),
                                text_color="white", fg_color="#1b1440")
        welcome.pack(pady=(35, 8))
        rol_label = ctk.CTkLabel(self.main_panel, text=f"{nombre}: Rol {rol}.", font=ctk.CTkFont(size=22),
                                 text_color="#81E821", fg_color="#1b1440")
        rol_label.pack(pady=(0, 22))

        if self.logo_cliente_path and os.path.exists(self.logo_cliente_path):
            img_c = Image.open(self.logo_cliente_path)
            self.c_logo = ctk.CTkImage(img_c, size=(320, 320))
            self.logo_cliente_label = ctk.CTkLabel(self.main_panel, image=self.c_logo, text="", fg_color="#1b1440")
            self.logo_cliente_label.pack(pady=(0, 18))
            self.logo_cliente_label.bind("<Button-1>", lambda e: self.seleccionar_logo())
        else:
            self.logo_cliente_label = ctk.CTkLabel(self.main_panel, text="SIN LOGO",
                                                   font=ctk.CTkFont(size=36), fg_color="#1b1440")
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
