import customtkinter as ctk
from tkinter import messagebox, END
from PIL import Image
from customtkinter import CTkImage

from src.currency import currency_model as cm

class CurrencyManager(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Gestión de Finanzas (Tasas, Pagos, Bancos)")
        self.geometry("1380x830+60+10")
        self.configure(fg_color="#181c25")
        self.resizable(True, True)
        self.focus()
        self.grab_set()

        # Solo crear la tabla de tasas si no existe, sin sobrescribir valores
        cm.crear_tabla_tasas_si_no_existe()

        self._build_ui()
        self._llenar_datos_db()

    def _build_ui(self):
        img_title = Image.open("C:/Proyectos/ERP_LITE_PYME_V2/assets/iconos/txtfinanzas.png")
        self.imgfin_title = CTkImage(light_image=img_title, dark_image=img_title, size=(640, 90))
        label_img_title = ctk.CTkLabel(self, text="", image=self.imgfin_title, fg_color="#181c25")
        label_img_title.pack(pady=(18, 4))

        self.tabview = ctk.CTkTabview(self,
                                      fg_color="#000000",
                                      segmented_button_fg_color="#313a5e",
                                      segmented_button_selected_color="#f308d4",
                                      segmented_button_selected_hover_color="#181c25",
                                      segmented_button_unselected_color="#e90707",
                                      height=700, width=1280)
        self.tabview.pack(fill="both", expand=True, padx=6, pady=(6, 16))

        self.tab_tasas = self.tabview.add("Tasas")
        self._build_tasas_tab(self.tab_tasas)

        self.tab_metodos = self.tabview.add("Métodos de Pago")
        self._build_metodos_tab(self.tab_metodos)

        self.tab_bancos = self.tabview.add("Bancos")
        self._build_bancos_tab(self.tab_bancos)

    def _build_tasas_tab(self, frame):
        frame.configure(fg_color="#232150")
        label_bcv = ctk.CTkLabel(
            frame, text="Tasa Oficial BCV (VES/USD):",
            font=("Segoe UI", 18, "bold"), text_color="#79e066", fg_color="#232150"
        )
        label_bcv.pack(pady=(80, 8))
        self.input_bcv = ctk.CTkEntry(frame, width=300, font=("Segoe UI", 16))
        self.input_bcv.pack(pady=4)

        label_para = ctk.CTkLabel(
            frame, text="Tasa Paralela (VES/USD):",
            font=("Segoe UI", 18, "bold"), text_color="#e1d326", fg_color="#232150"
        )
        label_para.pack(pady=(34, 8))
        self.input_para = ctk.CTkEntry(frame, width=300, font=("Segoe UI", 16))
        self.input_para.pack(pady=4)

        btn_guardar = ctk.CTkButton(
            frame, text="Guardar tasas", font=("Segoe UI", 16, "bold"),
            width=260, height=46, fg_color="#2bb696", hover_color="#289b87",
            command=self.save_tasas
        )
        btn_guardar.pack(pady=(60, 18))

    def _build_metodos_tab(self, frame):
        frame.configure(fg_color="#232150")
        label_metodos = ctk.CTkLabel(
            frame, text="Métodos de pago registrados:", font=("Segoe UI", 17, "bold"),
            text_color="#9bc8ff", fg_color="#232150"
        )
        label_metodos.pack(pady=(55, 8))

        self.lista_pago = ctk.CTkTextbox(frame, width=550, height=250, fg_color="#20203a",
                                         text_color="#e6e6e6", font=("Segoe UI", 15))
        self.lista_pago.pack(pady=(4, 18))

        add_frame = ctk.CTkFrame(frame, fg_color="#232150")
        add_frame.pack(pady=(2, 2))

        self.input_pago = ctk.CTkEntry(add_frame, width=240, font=("Segoe UI", 13))
        self.input_pago.pack(side="left", padx=(0,10))

        btn_add_pago = ctk.CTkButton(
            add_frame, text="Agregar método", font=("Segoe UI", 13, "bold"),
            width=140, fg_color="#86ffb9", hover_color="#7ad4a7",
            text_color="#191937", command=self.add_pago)
        btn_add_pago.pack(side="left", padx=4)

        btn_del_pago = ctk.CTkButton(
            add_frame, text="Eliminar seleccionado", font=("Segoe UI", 13, "bold"),
            width=190, fg_color="#c05446", hover_color="#ad382f",
            command=self.del_pago)
        btn_del_pago.pack(side="left", padx=6)

        self.lista_pago.delete("1.0", END)

    def _build_bancos_tab(self, frame):
        frame.configure(fg_color="#232150")
        label_bancos = ctk.CTkLabel(
            frame, text="Bancos registrados:", font=("Segoe UI", 17, "bold"),
            text_color="#cf7bd3", fg_color="#232150"
        )
        label_bancos.pack(pady=(55, 8))

        self.lista_bancos = ctk.CTkTextbox(frame, width=550, height=250, fg_color="#20203a",
                                           text_color="#e6e6e6", font=("Segoe UI", 15))
        self.lista_bancos.pack(pady=(4, 18))

        addbanco_frame = ctk.CTkFrame(frame, fg_color="#232150")
        addbanco_frame.pack(pady=(2, 2))

        self.input_banco = ctk.CTkEntry(addbanco_frame, width=240, font=("Segoe UI", 13))
        self.input_banco.pack(side="left", padx=(0,10))

        btn_add_banco = ctk.CTkButton(
            addbanco_frame, text="Agregar banco", font=("Segoe UI", 13, "bold"),
            width=140, fg_color="#ffaff9", hover_color="#ceaedd",
            text_color="#191937", command=self.add_banco)
        btn_add_banco.pack(side="left", padx=4)

        btn_del_banco = ctk.CTkButton(
            addbanco_frame, text="Eliminar seleccionado", font=("Segoe UI", 13, "bold"),
            width=190, fg_color="#e13eda", hover_color="#ad32bb",
            command=self.del_banco)
        btn_del_banco.pack(side="left", padx=6)

        self.lista_bancos.delete("1.0", END)

    def _llenar_datos_db(self):
        # TASAS
        bcv = cm.get_tasa("BCV")
        paralela = cm.get_tasa("PARALELA")
        self.input_bcv.delete(0, END)
        self.input_bcv.insert(0, str(bcv) if bcv is not None else "")
        self.input_para.delete(0, END)
        self.input_para.insert(0, str(paralela) if paralela is not None else "")

        # MÉTODOS DE PAGO
        self.lista_pago.delete("1.0", END)
        for p in cm.get_metodos_pago():
            self.lista_pago.insert(END, p + "\n")

        # BANCOS
        self.lista_bancos.delete("1.0", END)
        for b in cm.get_bancos():
            self.lista_bancos.insert(END, b + "\n")

    def save_tasas(self):
        try:
            bcv = float(self.input_bcv.get())
            paralela = float(self.input_para.get())
            cm.save_tasas(bcv, paralela)
            messagebox.showinfo("Guardado", "¡Tasas actualizadas correctamente!")
        except Exception:
            messagebox.showwarning("Error", "Debes ingresar valores numéricos válidos.")

    def add_pago(self):
        metodo = self.input_pago.get().strip()
        if metodo:
            cm.add_metodo_pago(metodo)
            self.input_pago.delete(0, "end")
            self._llenar_datos_db()

    def del_pago(self):
        current_text = self.lista_pago.get("1.0", END).strip().split("\n")
        if not current_text or (len(current_text)==1 and current_text[0]==""):
            messagebox.showinfo("Vacío", "No hay métodos de pago para eliminar.")
            return
        idx_choice = ctk.CTkInputDialog(text="Ingresa el nombre EXACTO del método a eliminar:", title="Eliminar método de pago")
        metodo = idx_choice.get_input() if idx_choice else None
        if metodo and metodo in current_text and cm.delete_metodo_pago(metodo):
            self._llenar_datos_db()
        else:
            messagebox.showwarning("No encontrado", "El método no existe en la lista o no pudo eliminarse.")

    def add_banco(self):
        banco = self.input_banco.get().strip()
        if banco:
            cm.add_banco(banco)
            self.input_banco.delete(0, "end")
            self._llenar_datos_db()

    def del_banco(self):
        current_text = self.lista_bancos.get("1.0", END).strip().split("\n")
        if not current_text or (len(current_text)==1 and current_text[0]==""):
            messagebox.showinfo("Vacío", "No hay bancos para eliminar.")
            return
        idx_choice = ctk.CTkInputDialog(text="Ingresa el nombre EXACTO del banco a eliminar:", title="Eliminar banco")
        banco = idx_choice.get_input() if idx_choice else None
        if banco and banco in current_text and cm.delete_banco(banco):
            self._llenar_datos_db()
        else:
            messagebox.showwarning("No encontrado", "El banco no existe en la lista o no pudo eliminarse.")

if __name__ == "__main__":
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    cw = CurrencyManager(root)
    cw.mainloop()
