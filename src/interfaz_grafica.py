import tkinter as tk
from tkinter import ttk, messagebox
from src.modelos.servicio import GestorServicios
from src.excepciones.errores_personalizados import ErrorSistemaFJ
from src.utils.logger import registrar_evento

class AppServiciosFJ:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Integral de Gestión - Módulo 3: Servicios")
        self.root.geometry("800x530")
        self.root.resizable(False, False)

        self.gestor = GestorServicios()
        self._construir_interfaz()
        registrar_evento("Interfaz gráfica del Módulo 3 (Servicios) iniciada.")

    def _construir_interfaz(self):
        lbl_titulo = tk.Label(
            self.root, text="MÓDULO 3: GESTIÓN DE SERVICIOS (POLIMORFISMO)", 
            font=("Arial", 13, "bold"), fg="#1f4e78", pady=10
        )
        lbl_titulo.pack()

        frame_form = tk.LabelFrame(self.root, text="Detalles del Servicio", padx=15, pady=15)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="Tipo de Servicio:").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_tipo = ttk.Combobox(frame_form, values=["Sala", "Equipo", "Asesoría"], state="readonly", width=22)
        self.combo_tipo.grid(row=0, column=1, padx=10, pady=5)
        self.combo_tipo.current(0)
        self.combo_tipo.bind("<<ComboboxSelected>>", self.actualizar_etiqueta_extra)

        tk.Label(frame_form, text="ID Servicio:").grid(row=0, column=2, sticky="w", pady=5)
        self.ent_id = tk.Entry(frame_form, width=25)
        self.ent_id.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="w", pady=5)
        self.ent_nombre = tk.Entry(frame_form, width=25)
        self.ent_nombre.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame_form, text="Costo Base ($):").grid(row=1, column=2, sticky="w", pady=5)
        self.ent_costo = tk.Entry(frame_form, width=25)
        self.ent_costo.grid(row=1, column=3, padx=10, pady=5)

        # Etiqueta dinámica según el servicio (Capacidad, Horas o Complejidad)
        self.lbl_extra = tk.Label(frame_form, text="Capacidad (Personas):")
        self.lbl_extra.grid(row=2, column=0, sticky="w", pady=5)
        self.ent_extra = tk.Entry(frame_form, width=25)
        self.ent_extra.grid(row=2, column=1, padx=10, pady=5)

        # Botones
        frame_botones = tk.Frame(self.root, pady=10)
        frame_botones.pack()

        btn_guardar = tk.Button(
            frame_botones, text="Registrar Servicio", bg="#2e7d32", fg="white",
            font=("Arial", 10, "bold"), width=20, command=self.accion_registrar
        )
        btn_guardar.grid(row=0, column=0, padx=10)

        btn_limpiar = tk.Button(
            frame_botones, text="Limpiar Campos", bg="#455a64", fg="white",
            font=("Arial", 10, "bold"), width=15, command=self.limpiar
        )
        btn_limpiar.grid(row=0, column=1, padx=10)

        # Tabla
        frame_tabla = tk.Frame(self.root, padx=20, pady=10)
        frame_tabla.pack(fill="both", expand=True)

        columnas = ("tipo", "id", "nombre", "base", "extra", "total")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=10)
        
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("base", text="Costo Base")
        self.tabla.heading("extra", text="Dato Extra")
        self.tabla.heading("total", text="Costo Total (Polimorfismo)")

        self.tabla.column("tipo", width=90, anchor="center")
        self.tabla.column("id", width=70, anchor="center")
        self.tabla.column("nombre", width=180)
        self.tabla.column("base", width=100, anchor="e")
        self.tabla.column("extra", width=110, anchor="center")
        self.tabla.column("total", width=150, anchor="e")

        self.tabla.pack(fill="both", expand=True)

    def actualizar_etiqueta_extra(self, event):
        tipo = self.combo_tipo.get()
        if tipo == "Sala":
            self.lbl_extra.config(text="Capacidad (Personas):")
        elif tipo == "Equipo":
            self.lbl_extra.config(text="Horas de Alquiler:")
        elif tipo == "Asesoría":
            self.lbl_extra.config(text="Complejidad (normal/alta):")

    def accion_registrar(self):
        try:
            tipo = self.combo_tipo.get()
            servicio = self.gestor.registrar_servicio(
                tipo,
                self.ent_id.get(),
                self.ent_nombre.get(),
                self.ent_costo.get(),
                self.ent_extra.get()
            )
            
            # Identificar el valor extra para mostrarlo en la tabla
            extra_val = getattr(servicio, 'capacidad_personas', None) or \
                        getattr(servicio, 'horas_alquiler', None) or \
                        getattr(servicio, 'nivel_complejidad', '')

            self.tabla.insert("", "end", values=(
                tipo, servicio.id_servicio, servicio.nombre,
                f"${servicio.costo_base:,.2f}", extra_val,
                f"${servicio.calcular_costo_total():,.2f}"
            ))
            messagebox.showinfo("Éxito", f"Servicio de tipo {tipo} registrado correctamente.")
            self.limpiar()
        except (ValueError, ErrorSistemaFJ) as e:
            messagebox.showwarning("Atención", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    def limpiar(self):
        self.ent_id.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_costo.delete(0, tk.END)
        self.ent_extra.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppServiciosFJ(root)
    root.mainloop()