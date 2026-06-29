import tkinter as tk
from tkinter import ttk, messagebox
import db
import webbrowser
from urllib.parse import quote

COLOR_FONDO = "#f6f8fb"
COLOR_AZUL = "#2563eb"
COLOR_TEXTO = "#0f172a"
COLOR_BORDE = "#e5e7eb"
COLOR_ROJO = "#dc2626"
COLOR_NARANJA = "#f97316"


def mostrar_modulo_alertas(parent, usuario=None):
    modulo = ModuloAlertas(parent)
    modulo.pack(fill="both", expand=True)


class ModuloAlertas(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_FONDO)
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
            text="Alertas de Reactivos",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 15, "bold")
        ).pack(side="left")

        tk.Button(
            top,
            text="Actualizar",
            command=self.cargar_alertas,
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
            text="Enviar email",
            command=self.enviar_email_alertas,
            bg="#16a34a",
            fg="white",
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=7,
            cursor="hand2"
        ).pack(side="right", padx=(0, 10))

        self.crear_tabla(card)
        self.cargar_alertas()

    def crear_tabla(self, parent):
        columnas = (
            "tipo",
            "codigo",
            "reactivo",
            "lote",
            "proveedor",
            "stock_actual",
            "stock_minimo",
            "vencimiento",
            "estado"
        )

        self.tabla = ttk.Treeview(
            parent,
            columns=columnas,
            show="headings",
            height=16
        )

        self.tabla.pack(fill="both", expand=True, padx=18, pady=(0, 15))

        encabezados = {
            "tipo": "Tipo alerta",
            "codigo": "Código",
            "reactivo": "Reactivo",
            "lote": "Lote",
            "proveedor": "Proveedor",
            "stock_actual": "Stock actual",
            "stock_minimo": "Stock mínimo",
            "vencimiento": "Vencimiento",
            "estado": "Estado"
        }

        for col in columnas:
            self.tabla.heading(col, text=encabezados[col])
            self.tabla.column(col, width=130)

        self.tabla.column("reactivo", width=220)
        self.tabla.column("proveedor", width=180)

    def cargar_alertas(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        datos = db.obtener_alertas_reactivos()

        for fila in datos:
            self.tabla.insert("", "end", values=fila)

    def enviar_email_alertas(self):

        datos = db.obtener_items_para_email_alertas()

        if not datos:
            messagebox.showinfo(
                "Sin alertas",
                "No hay reactivos por debajo del stock mínimo."
            )
            return

        proveedores = {}

        for fila in datos:

            id_proveedor = fila[0]
            proveedor = fila[1]
            email = fila[2]
            codigo_proveedor = fila[3]
            reactivo = fila[4]
            cas_numero = fila[5]
            cantidad_inicial = fila[6] or 0
            unidad = fila[7] or ""
            stock_minimo = fila[8] or 0
            stock_actual = fila[9] or 0

            faltante = stock_minimo - stock_actual

            if faltante <= 0:
                continue

            if cantidad_inicial > 0:

                cantidad_botellas = int(faltante / cantidad_inicial)

                if faltante % cantidad_inicial != 0:
                    cantidad_botellas += 1

            else:
                cantidad_botellas = 1

            if id_proveedor not in proveedores:

                proveedores[id_proveedor] = {
                    "proveedor": proveedor,
                    "email": email,
                    "items": []
                }

            proveedores[id_proveedor]["items"].append({
                "codigo_proveedor": codigo_proveedor,
                "reactivo": reactivo,
                "cas_numero": cas_numero,
                "cantidad_botellas": cantidad_botellas
            })

        if not proveedores:
            messagebox.showinfo(
                "Sin alertas",
                "No hay materiales con faltante para solicitar."
            )
            return

        try:

            for _, info in proveedores.items():

                asunto = "Solicitud de cotización / reposición de materiales"

                cuerpo = f"Estimados {info['proveedor']},\n\n"

                cuerpo += (
                    "Solicitamos cotización para la reposición "
                    "de los siguientes materiales:\n\n"
                )

                for item in info["items"]:

                    cuerpo += (
                        f"\n"
                        f"Código proveedor: {item['codigo_proveedor']}\n"
                        f"Reactivo: {item['reactivo']}\n"
                        f"CAS N°: {item['cas_numero']}\n"
                        f"Cantidad solicitada: {item['cantidad_botellas']} botella/s\n"
                        f"{'-'*50}\n"
                    )

                cuerpo += (
                    "\nPor favor enviar presupuesto indicando:\n"
                    "- Disponibilidad\n"
                    "- Precio\n"
                    "- Presentación\n"
                    "- Plazo de entrega\n\n"
                    "Saludos."
                )

                mailto = (
                    f"mailto:{info['email']}"
                    f"?subject={quote(asunto)}"
                    f"&body={quote(cuerpo)}"
                )

                webbrowser.open(mailto)

            messagebox.showinfo(
                "Correcto",
                "Se generaron los correos para Outlook."
            )

        except Exception as e:

            messagebox.showerror(
                "Error",
                f"No se pudo generar el correo.\n\n{e}"
            )

