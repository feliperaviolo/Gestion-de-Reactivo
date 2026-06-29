import tkinter as tk
from tkinter import ttk, messagebox
import db


COLOR_FONDO = "#f6f8fb"
COLOR_AZUL = "#2563eb"
COLOR_TEXTO = "#0f172a"
COLOR_BORDE = "#e5e7eb"


def mostrar_modulo_reactivos(parent, usuario=None):
    modulo = ModuloReactivos(parent)
    modulo.pack(fill="both", expand=True)


class ModuloReactivos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
        self.labels_indicadores = {}
        self.crear_interfaz()

    def crear_interfaz(self):
        self.crear_cards()

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
            text="Inventario de Reactivos",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")

        tk.Button(
            top,
            text="+ Nuevo Reactivo",
            command=self.abrir_formulario_reactivo,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="right")

        tk.Button(
            top,
            text="Editar Reactivo",
            command=self.abrir_formulario_editar_reactivo,
            bg="#64748b",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="right", padx=(0, 10))

        self.crear_tabla(card)
        self.actualizar_indicadores()
        self.cargar_tabla()

    def crear_cards(self):
        frame = tk.Frame(self, bg=COLOR_FONDO)
        frame.pack(fill="x", pady=(0, 18))

        cards = [
            ("total", "🧪", "Reactivos totales", "#2563eb"),
            ("stock_ok", "🛒", "Stock adecuado", "#22c55e"),
            ("por_vencer", "⚠️", "Por vencer", "#f59e0b"),
            ("vencidos", "⛔", "Vencidos", "#ef4444"),
            ("bajo_stock", "📋", "Bajo stock", "#7c3aed"),
        ]

        for clave, icono, texto, color in cards:
            card = tk.Frame(
                frame,
                bg="white",
                highlightbackground=COLOR_BORDE,
                highlightthickness=1
            )
            card.pack(side="left", fill="x", expand=True, padx=6, ipady=15)

            tk.Label(
                card,
                text=icono,
                bg="white",
                fg=color,
                font=("Segoe UI", 28)
            ).pack(side="left", padx=18)

            info = tk.Frame(card, bg="white")
            info.pack(side="left")

            lbl_numero = tk.Label(
                info,
                text="0",
                bg="white",
                fg=COLOR_TEXTO,
                font=("Segoe UI", 20, "bold")
            )
            lbl_numero.pack(anchor="w")

            tk.Label(
                info,
                text=texto,
                bg="white",
                fg=COLOR_TEXTO,
                font=("Segoe UI", 10)
            ).pack(anchor="w")

            

            self.labels_indicadores[clave] = lbl_numero

    def actualizar_indicadores(self):
        datos = db.obtener_indicadores_reactivos()

        self.labels_indicadores["total"].config(text=datos["total"])
        self.labels_indicadores["stock_ok"].config(text=datos["stock_ok"])
        self.labels_indicadores["por_vencer"].config(text=datos["por_vencer"])
        self.labels_indicadores["vencidos"].config(text=datos["vencidos"])
        self.labels_indicadores["bajo_stock"].config(text=datos["bajo_stock"])

    def crear_tabla(self, parent):
        columnas = (
            "codigo",
            "nombre",
            "renpre",
            "stock",
            "unidad",
            "vencimiento",
            "estado"
        )

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="white",
            foreground=COLOR_TEXTO,
            rowheight=42,
            fieldbackground="white",
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background="#f8fafc",
            foreground=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        )

        self.tabla = ttk.Treeview(parent, columns=columnas, show="headings", height=12)
        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 10))

        encabezados = {
            "codigo": "Código interno",
            "nombre": "Nombre",
            "renpre": "RENPRE",
            "stock": "Stock actual",
            "unidad": "Unidad",
            "vencimiento": "Vencimiento",
            "estado": "Estado",
        }

        for col in columnas:
            self.tabla.heading(col, text=encabezados[col])
            self.tabla.column(col, width=130)

    def cargar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        datos = db.obtener_inventario()

        for fila in datos:
            self.tabla.insert("", "end", values=fila)

    def abrir_formulario_reactivo(self):
        ventana = tk.Toplevel(self)
        ventana.title("Nuevo Reactivo")
        ventana.geometry("540x560")
        ventana.configure(bg="white")
        ventana.resizable(False, False)

        canvas = tk.Canvas(ventana, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)

        contenido = tk.Frame(canvas, bg="white")

        contenido.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=contenido, anchor="nw", width=520)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(
            contenido,
            text="Nuevo Reactivo",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        frame = tk.Frame(contenido, bg="white")
        frame.pack(fill="both", expand=True, padx=30)

        campos = {}

        def crear_campo(label, nombre):
            tk.Label(
                frame,
                text=label,
                bg="white",
                fg=COLOR_TEXTO,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", pady=(8, 2))

            entry = tk.Entry(frame, font=("Segoe UI", 10), relief="solid", bd=1)
            entry.pack(fill="x", ipady=6)

            campos[nombre] = entry

        crear_campo("Código interno *", "codigo")
        crear_campo("Nombre *", "nombre")
        crear_campo("CAS N°", "cas")
        crear_campo("GTIN", "gtin")

        tk.Label(
            frame,
            text="RENPRE",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_renpre = ttk.Combobox(
            frame,
            values=["Sí", "No"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_renpre.pack(fill="x", ipady=6)
        combo_renpre.set("No")

        crear_campo("Riesgo", "riesgo")

        tk.Label(
            frame,
            text="Condición de almacenamiento",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_condiciones = ttk.Combobox(
            frame,
            values=[
                "Temperatura ambiente",
                "Heladera",
                "Freezer"
            ],
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_condiciones.pack(fill="x", ipady=6)
        combo_condiciones.set("Temperatura ambiente")

        tk.Label(
            frame,
            text="Unidad de medida",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_unidad = ttk.Combobox(
            frame,
            values=["ml", "litro", "gramo"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_unidad.pack(fill="x", ipady=6)
        combo_unidad.set("ml")

        crear_campo("Stock mínimo *", "stock_minimo")
        crear_campo("Días vencimiento después de apertura", "dias_vencimiento_apertura")

        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass

        ventana.bind_all("<MouseWheel>", _on_mousewheel)

        def cerrar():
            canvas.unbind_all("<MouseWheel>")
            ventana.destroy()

        def guardar():
            codigo = campos["codigo"].get().strip()
            nombre = campos["nombre"].get().strip()
            stock_minimo = campos["stock_minimo"].get().strip()
            dias_apertura = campos["dias_vencimiento_apertura"].get().strip()

            if not codigo or not nombre or not stock_minimo:
                messagebox.showwarning(
                    "Campos obligatorios",
                    "Código interno, nombre y stock mínimo son obligatorios."
                )
                return

            try:
                stock_minimo = float(stock_minimo.replace(",", "."))
            except ValueError:
                messagebox.showerror("Error", "El stock mínimo debe ser un número.")
                return

            try:
                dias_apertura = int(dias_apertura) if dias_apertura else 0
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Los días de vencimiento después de apertura deben ser un número entero."
                )
                return

            renpre = combo_renpre.get()
            unidad = combo_unidad.get()

            try:
                db.insertar_reactivo(
                    codigo,
                    nombre,
                    campos["gtin"].get().strip(),
                    campos["cas"].get().strip(),
                    renpre,
                    campos["riesgo"].get().strip(),
                    combo_condiciones.get(),
                    unidad,
                    stock_minimo,
                    dias_apertura
                )

                self.cargar_tabla()
                self.actualizar_indicadores()
                cerrar()

                messagebox.showinfo("Correcto", "Reactivo creado correctamente.")

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el reactivo.\n\n{e}")

        botones = tk.Frame(contenido, bg="white")
        botones.pack(fill="x", padx=30, pady=25)

        tk.Button(
            botones,
            text="Cancelar",
            command=cerrar,
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
            text="Guardar Reactivo",
            command=guardar,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(side="right")

    def abrir_formulario_editar_reactivo(self):
        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Sin selección",
                "Seleccioná un reactivo de la tabla para editar."
            )
            return

        valores = self.tabla.item(seleccionado[0], "values")
        codigo_actual = valores[0]

        reactivo = db.obtener_reactivo_por_codigo(codigo_actual)

        if not reactivo:
            messagebox.showerror("Error", "No se encontró el reactivo seleccionado.")
            return

        ventana = tk.Toplevel(self)
        ventana.title("Editar Reactivo")
        ventana.geometry("540x620")
        ventana.configure(bg="white")
        ventana.resizable(False, False)

        canvas = tk.Canvas(ventana, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)

        contenido = tk.Frame(canvas, bg="white")

        contenido.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=contenido, anchor="nw", width=520)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        tk.Label(
            contenido,
            text="Editar Reactivo",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(pady=20)

        frame = tk.Frame(contenido, bg="white")
        frame.pack(fill="both", expand=True, padx=30)

        campos = {}

        def crear_campo(label, nombre, valor=""):
            tk.Label(
                frame,
                text=label,
                bg="white",
                fg=COLOR_TEXTO,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w", pady=(8, 2))

            entry = tk.Entry(frame, font=("Segoe UI", 10), relief="solid", bd=1)
            entry.pack(fill="x", ipady=6)
            entry.insert(0, "" if valor is None else str(valor))

            campos[nombre] = entry

        codigo, nombre, gtin, cas, renpre, riesgo, condiciones, unidad, stock_minimo, dias_apertura, activo = reactivo

        crear_campo("Código interno", "codigo", codigo)
        campos["codigo"].config(state="disabled")

        crear_campo("Nombre *", "nombre", nombre)
        crear_campo("GTIN", "gtin", gtin)
        crear_campo("CAS N°", "cas", cas)

        tk.Label(
            frame,
            text="RENPRE",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_renpre = ttk.Combobox(
            frame,
            values=["Sí", "No"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_renpre.pack(fill="x", ipady=6)
        combo_renpre.set(renpre if renpre else "No")

        crear_campo("Riesgo", "riesgo", riesgo)

        tk.Label(
            frame,
            text="Condición de almacenamiento",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_condiciones = ttk.Combobox(
            frame,
            values=["Temperatura ambiente", "Heladera", "Freezer"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_condiciones.pack(fill="x", ipady=6)
        combo_condiciones.set(condiciones if condiciones else "Temperatura ambiente")

        tk.Label(
            frame,
            text="Unidad de medida",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_unidad = ttk.Combobox(
            frame,
            values=["ml", "litro", "gramo"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_unidad.pack(fill="x", ipady=6)
        combo_unidad.set(unidad if unidad else "ml")

        crear_campo("Stock mínimo *", "stock_minimo", stock_minimo)
        crear_campo("Días vencimiento después de apertura", "dias_apertura", dias_apertura)

        tk.Label(
            frame,
            text="Estado",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(8, 2))

        combo_activo = ttk.Combobox(
            frame,
            values=["Activo", "Inactivo"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo_activo.pack(fill="x", ipady=6)
        combo_activo.set("Activo" if activo == 1 else "Inactivo")

        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass

        ventana.bind("<MouseWheel>", _on_mousewheel)

        def cerrar():
            ventana.unbind("<MouseWheel>")
            ventana.destroy()

        def guardar_edicion():
            nombre_editado = campos["nombre"].get().strip()
            stock = campos["stock_minimo"].get().strip()
            dias = campos["dias_apertura"].get().strip()

            if not nombre_editado or not stock:
                messagebox.showwarning(
                    "Campos obligatorios",
                    "Nombre y stock mínimo son obligatorios."
                )
                return

            try:
                stock = float(stock.replace(",", "."))
            except ValueError:
                messagebox.showerror("Error", "El stock mínimo debe ser un número.")
                return

            try:
                dias = int(dias) if dias else 0
            except ValueError:
                messagebox.showerror(
                    "Error",
                    "Los días de vencimiento deben ser un número entero."
                )
                return

            activo_valor = 1 if combo_activo.get() == "Activo" else 0

            try:
                db.actualizar_reactivo(
                    codigo_actual,
                    nombre_editado,
                    campos["gtin"].get().strip(),
                    campos["cas"].get().strip(),
                    combo_renpre.get(),
                    campos["riesgo"].get().strip(),
                    combo_condiciones.get(),
                    combo_unidad.get(),
                    stock,
                    dias,
                    activo_valor
                )

                self.cargar_tabla()
                self.actualizar_indicadores()
                cerrar()

                messagebox.showinfo("Correcto", "Reactivo actualizado correctamente.")

            except Exception as e:
                messagebox.showerror(
                    "Error",
                    f"No se pudo actualizar el reactivo.\n\n{e}"
                )

        botones = tk.Frame(contenido, bg="white")
        botones.pack(fill="x", padx=30, pady=25)

        tk.Button(
            botones,
            text="Cancelar",
            command=cerrar,
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
            text="Guardar Cambios",
            command=guardar_edicion,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        ).pack(side="right")

