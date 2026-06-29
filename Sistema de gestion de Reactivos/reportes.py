import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from datetime import datetime
import db


COLOR_FONDO = "#f6f8fb"
COLOR_AZUL = "#2563eb"
COLOR_TEXTO = "#0f172a"
COLOR_BORDE = "#e5e7eb"


def mostrar_modulo_reportes(parent, usuario=None):
    modulo = ModuloReportes(parent)
    modulo.pack(fill="both", expand=True)


class ModuloReportes(tk.Frame):
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
        card.pack(fill="both", expand=True, padx=0, pady=0)

        tk.Label(
            card,
            text="Reportes",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=25, pady=(25, 10))

        tk.Label(
            card,
            text="Descarga de movimientos de stock",
            bg="white",
            fg=COLOR_TEXTO,
            font=("Segoe UI", 11)
        ).pack(anchor="w", padx=25, pady=(0, 20))

        tk.Button(
            card,
            text="Descargar todos los movimientos",
            command=self.descargar_todos_movimientos,
            bg=COLOR_AZUL,
            fg="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(anchor="w", padx=25, pady=8)

        tk.Button(
            card,
            text="Descargar movimientos RENPRE = Sí",
            command=self.descargar_movimientos_renpre,
            bg="#16a34a",
            fg="white",
            relief="flat",
            font=("Segoe UI", 11, "bold"),
            padx=18,
            pady=10,
            cursor="hand2"
        ).pack(anchor="w", padx=25, pady=8)

    def exportar_csv(self, datos, nombre_sugerido):
        if not datos:
            messagebox.showinfo(
                "Sin datos",
                "No hay información para exportar."
            )
            return

        columnas = [
            "ID Movimiento",
            "Fecha movimiento",
            "Tipo movimiento",
            "Código interno",
            "GTIN",
            "Reactivo",
            "CAS N°",
            "RENPRE",
            "Proveedor",
            "Lote",
            "Cantidad",
            "Unidad",
            "Vencimiento sin abrir",
            "Fecha apertura",
            "Vencimiento por apertura",
            "Usuario",
            "Observaciones"
        ]

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{nombre_sugerido}_{fecha}.csv"

        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=nombre_archivo,
            filetypes=[("CSV", "*.csv")]
        )

        if not ruta:
            return

        try:
            with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
                writer = csv.writer(archivo, delimiter=";")
                writer.writerow(columnas)

                for fila in datos:
                    writer.writerow(fila)

            messagebox.showinfo(
                "Correcto",
                f"Reporte descargado correctamente:\n\n{ruta}"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo generar el reporte.\n\n{e}"
            )

    def descargar_todos_movimientos(self):
        datos = db.obtener_reporte_movimientos_stock()
        self.exportar_csv(datos, "Reporte_Movimientos_Stock")

    def descargar_movimientos_renpre(self):
        datos = db.obtener_reporte_movimientos_renpre()
        self.exportar_csv(datos, "Reporte_Movimientos_RENPRE")