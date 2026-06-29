import tkinter as tk
from tkinter import ttk, messagebox
import db
from datetime import datetime
import win32print
from dateutil.relativedelta import relativedelta


COLOR_FONDO = "#f6f8fb"
COLOR_AZUL = "#2563eb"
COLOR_TEXTO = "#0f172a"
COLOR_BORDE = "#e5e7eb"


def mostrar_modulo_ingresos(parent, usuario=None):
    modulo = ModuloIngresos(parent, usuario)
    modulo.pack(fill="both", expand=True)


class ModuloIngresos(tk.Frame):
    def __init__(self, parent, usuario=None):
        super().__init__(parent, bg=COLOR_FONDO)
        self.usuario = usuario
        self.rol_usuario = usuario[2] if usuario else ""
        self.combo_data = []
        self.crear_interfaz()

    def crear_interfaz(self):
        card = tk.Frame(
            self,
            bg="white",
            highlightbackground=COLOR_BORDE,
            highlightthickness=1
        )
        card.pack(fill="both", expand=True)

        top = tk.Frame(card, bg="white")
        top.pack(fill="x", padx=18, pady=15)

        tk.Label(
            top,
            text="Ingresos de Reactivos",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")

        tk.Button(
            top,
            text="Imprimir Rótulo",
            command=self.imprimir_rotulo_ingreso,
            bg="#16a34a",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="right", padx=(0, 10))

        tk.Button(
            top,
            text="+ Nuevo Ingreso",
            command=self.abrir_formulario_ingreso,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

        self.crear_tabla(card)
        self.cargar_tabla()

    def crear_tabla(self, parent):
        columnas = (
            "id",
            "codigo",
            "reactivo",
            "proveedor",
            "lote",
            "cantidad",
            "unidad",
            "fecha_ingreso",
            "vencimiento",
            "estado"
        )

        self.tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=14)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 15))

        encabezados = {
            "id": "ID",
            "codigo": "Código",
            "reactivo": "Reactivo",
            "proveedor": "Proveedor",
            "lote": "Lote",
            "cantidad": "Cantidad",
            "unidad": "Unidad",
            "fecha_ingreso": "Fecha ingreso",
            "vencimiento": "Vencimiento",
            "estado": "Estado"
        }

        for col in columnas:
            self.tabla.heading(col, text=encabezados[col])
            self.tabla.column(col, width=120)

        self.tabla.column("id", width=50)

    def cargar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for fila in db.obtener_ingresos():
            self.tabla.insert("", "end", values=fila)

    def abrir_formulario_ingreso(self):

        self.combo_data = db.obtener_reactivo_proveedor_combo()
        

        if not self.combo_data:
            messagebox.showwarning(
                "Sin asociaciones",
                "Primero tenés que asociar un reactivo con un proveedor."
            )
            return

        ventana = tk.Toplevel(self)
        ventana.title("Nuevo Ingreso")
        ventana.geometry("600x620")
        ventana.configure(bg="white")
        ventana.resizable(False, False)

        tk.Label(
            ventana,
            text="Nuevo Ingreso de Reactivo",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        frame = tk.Frame(
            ventana,
            bg="white"
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30
        )

        # ==================================
        # BUSCADOR
        # ==================================

        tk.Label(
            frame,
            text="Buscar por código interno, reactivo o proveedor",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        entry_buscar = tk.Entry(
            frame,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        )
        entry_buscar.pack(fill="x", ipady=6)

        tk.Label(
            frame,
            text="Reactivo / Proveedor *",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        valores_combo = [str(item[1]) for item in self.combo_data]

        combo_reactivo_proveedor = ttk.Combobox(
            frame,
            values=valores_combo,
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_reactivo_proveedor.pack(fill="x", ipady=6)


        def filtrar_reactivos(event=None):
            texto = entry_buscar.get().strip().lower()

            filtrados = []

            for item in self.combo_data:
                texto_combo = str(item[1]).lower()

                if texto in texto_combo:
                    filtrados.append(item[1])

            combo_reactivo_proveedor["values"] = filtrados

            if filtrados:
                combo_reactivo_proveedor.set(filtrados[0])
            else:
                combo_reactivo_proveedor.set("")
            
            

        entry_buscar.bind(
            "<KeyRelease>",
            filtrar_reactivos
        )

        # ==================================
        # CAMPOS
        # ==================================

        campos = {}

        def crear_campo(label, nombre):

            tk.Label(
                frame,
                text=label,
                bg="white",
                fg=COLOR_TEXTO,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", pady=(8, 2))

            entry = tk.Entry(
                frame,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1
            )

            entry.pack(fill="x", ipady=6)

            campos[nombre] = entry

        crear_campo(
            "Número de lote *",
            "numero_lote"
        )

        crear_campo(
            "Cantidad de frascos *",
            "cantidad"
        )

        crear_campo(
            "Fecha ingreso *",
            "fecha_ingreso"
        )

        campos["fecha_ingreso"].insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        crear_campo(
            "Vencimiento sin abrir *",
            "vencimiento"
        )

        crear_campo(
            "Observaciones",
            "observaciones"
        )

        # ==================================
        # GUARDAR
        # ==================================

        def guardar():

            seleccionado = combo_reactivo_proveedor.get()
            numero_lote = campos["numero_lote"].get().strip()
            cantidad_frascos = campos["cantidad"].get().strip()
            fecha_ingreso = campos["fecha_ingreso"].get().strip()
            vencimiento = campos["vencimiento"].get().strip()
            observaciones = campos["observaciones"].get().strip()

            if (
                not seleccionado
                or not numero_lote
                or not cantidad_frascos
                or not fecha_ingreso
                or not vencimiento
            ):
                messagebox.showwarning(
                    "Campos obligatorios",
                    "Completá todos los campos obligatorios."
                )
                return

            id_reactivo_proveedor = None

            for item in self.combo_data:
                if str(item[1]).strip() == seleccionado.strip():
                    id_reactivo_proveedor = item[0]
                    break

            if id_reactivo_proveedor is None:
                messagebox.showerror(
                    "Error",
                    "No se encontró la asociación reactivo-proveedor."
                )
                return

            try:
                cantidad_frascos = float(cantidad_frascos.replace(",", "."))
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "La cantidad de frascos debe ser un número."
                )
                return

            try:
                fecha_ingreso_dt = datetime.strptime(fecha_ingreso, "%Y-%m-%d").date()
                vencimiento_dt = datetime.strptime(vencimiento, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Las fechas deben tener formato AAAA-MM-DD."
                )
                return

            hoy = datetime.now().date()

            if vencimiento_dt < hoy:
                messagebox.showerror(
                    "Lote vencido",
                    "No se puede ingresar un lote que ya está vencido."
                )
                return

            if vencimiento_dt < fecha_ingreso_dt:
                messagebox.showerror(
                    "Fecha inválida",
                    "El vencimiento no puede ser anterior a la fecha de ingreso."
                )
                return

            rol_usuario = getattr(self, "rol_usuario", "")

            if rol_usuario != "Administrador":
                fecha_minima = hoy + relativedelta(months=4)

                if vencimiento_dt < fecha_minima:
                    messagebox.showerror(
                        "Vencimiento no permitido",
                        "El vencimiento del lote debe ser como mínimo de 4 meses.\n\n"
                        "Solo un Administrador puede ingresar lotes con vencimiento menor."
                    )
                    return

            try:
                db.insertar_ingreso_lote(
                    id_reactivo_proveedor,
                    numero_lote,
                    cantidad_frascos,
                    fecha_ingreso,
                    vencimiento,
                    observaciones,
                    1
                )

                self.cargar_tabla()
                ventana.destroy()

                messagebox.showinfo(
                    "Correcto",
                    "Ingreso registrado correctamente."
                )

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo registrar el ingreso.\n\n{e}"
                )


        # ==================================
        # BOTONES
        # ==================================

        botones = tk.Frame(
            ventana,
            bg="white"
        )

        botones.pack(
            fill="x",
            padx=30,
            pady=20
        )

        tk.Button(
            botones,
            text="Cancelar",
            command=ventana.destroy,
            bg="#e5e7eb",
            fg=COLOR_TEXTO,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(side="left")

        tk.Button(
            botones,
            text="Guardar Ingreso",
            command=guardar,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(side="right")

    def generar_zpl_rotulo(self, codigo_interno, lote, vencimiento):
        return f"""
        ^XA
        ^CI28
        ^MD20
        ^PW342
        ^LL236

        ^FO123,123^GB332,226,2^FS

        ^FO130,130^A0N,18,18^FDCODIGO INTERNO^FS
        ^FO130,150^A0N,26,26^FD{codigo_interno}^FS

        ^FO130,178^BY1,2,38
        ^BCN,38,Y,N,N
        ^FD{codigo_interno}^FS

        ^FO130,233^GB315,2,2^FS

        ^FO130,240^A0N,18,18^FDLOTE^FS
        ^FO130,260^A0N,24,24^FD{lote}^FS

        ^FO130,284^BY1,2,34
        ^BCN,34,Y,N,N
        ^FD{lote}^FS

        ^FO130,331^A0N,17,17^FDVTO: {vencimiento}^FS

        ^XZ
        """


    def imprimir_zpl(self, nombre_impresora, zpl):
        hPrinter = win32print.OpenPrinter(nombre_impresora)

        try:
            hJob = win32print.StartDocPrinter(
                hPrinter,
                1,
                ("Rotulo Reactivo", None, "RAW")
            )

            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, zpl.encode("utf-8"))
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)

        finally:
            win32print.ClosePrinter(hPrinter)


    def imprimir_rotulo_ingreso(self):
        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Sin selección",
                "Seleccioná un ingreso de la tabla para imprimir el rótulo."
            )
            return

        valores = self.tabla.item(seleccionado[0], "values")

        codigo_interno = valores[1]
        lote = valores[4]
        vencimiento = valores[8]

        zpl = self.generar_zpl_rotulo(
            codigo_interno,
            lote,
            vencimiento
        )

        try:
            self.imprimir_zpl(
                "ZDesigner ZM400 300 dpi (ZPL)",
                zpl
            )

            messagebox.showinfo(
                "Correcto",
                "Rótulo enviado a imprimir."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo imprimir el rótulo.\n\n{e}"
            )

