import customtkinter as ctk

from tkinter import (
    messagebox,
    filedialog
)

from interfaz.crear_automata import (
    CrearAutomataFrame
)

from interfaz.simular_cadena import (
    SimularCadenaFrame
)

from interfaz.ver_diagrama import (
    VerDiagramaFrame
)

from interfaz.conversion_afn_afd import (
    ConversionAFNaAFDFrame
)

from interfaz.minimizar_afd import (
    MinimizarAFDFrame
)

from utilidades.persistencia import (
    guardar_automata,
    cargar_automata
)


class VentanaPrincipal(ctk.CTk):

    def __init__(self):
        super().__init__()

        # =====================================================
        # CONFIGURACIÓN GENERAL
        # =====================================================

        self.title(
            "Simulador de Autómatas"
        )

        self.geometry(
            "1180x720"
        )

        self.minsize(
            1000,
            650
        )

        # Autómata actualmente cargado
        self.automata_actual = None

        # "AFD" o "AFN"
        self.tipo_automata_actual = None

        # =====================================================
        # GRID PRINCIPAL
        # =====================================================

        self.grid_rowconfigure(
            0,
            weight=1
        )

        self.grid_columnconfigure(
            1,
            weight=1
        )

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_menu_lateral()

        self.crear_area_principal()

        self.crear_barra_estado()

        self.actualizar_estado_botones()

        self.mostrar_inicio()

    # =========================================================
    # MENÚ LATERAL
    # =========================================================

    def crear_menu_lateral(self):

        self.frame_menu = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.frame_menu.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.frame_menu.grid_propagate(
            False
        )

        # -----------------------------------------------------
        # LOGO / TÍTULO
        # -----------------------------------------------------

        self.lbl_titulo = ctk.CTkLabel(
            self.frame_menu,
            text="AUTÓMATAS",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        self.lbl_titulo.pack(
            pady=(35, 5)
        )

        self.lbl_subtitulo = ctk.CTkLabel(
            self.frame_menu,
            text="Simulador",
            font=ctk.CTkFont(
                size=14
            )
        )

        self.lbl_subtitulo.pack(
            pady=(0, 25)
        )

        # -----------------------------------------------------
        # INICIO
        # -----------------------------------------------------

        self.btn_inicio = ctk.CTkButton(
            self.frame_menu,
            text="Inicio",
            height=42,
            command=self.mostrar_inicio
        )

        self.btn_inicio.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        # -----------------------------------------------------
        # NUEVO AUTÓMATA
        # -----------------------------------------------------

        self.btn_nuevo = ctk.CTkButton(
            self.frame_menu,
            text="Nuevo autómata",
            height=42,
            command=self.mostrar_crear_automata
        )

        self.btn_nuevo.pack(
            padx=20,
            pady=5,
            fill="x"
        )



        # -----------------------------------------------------
        # ABRIR AUTÓMATA
        # -----------------------------------------------------

        self.btn_abrir = ctk.CTkButton(
            self.frame_menu,
            text="Abrir autómata",
            height=42,
            command=self.abrir_automata
        )

        self.btn_abrir.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        # -----------------------------------------------------
        # GUARDAR AUTÓMATA
        # -----------------------------------------------------

        self.btn_guardar = ctk.CTkButton(
            self.frame_menu,
            text="Guardar autómata",
            height=42,
            command=self.guardar_automata_actual
        )

        self.btn_guardar.pack(
            padx=20,
            pady=5,
            fill="x"
        )




        # -----------------------------------------------------
        # SIMULAR
        # -----------------------------------------------------

        self.btn_simular = ctk.CTkButton(
            self.frame_menu,
            text="Simular cadena",
            height=42,
            command=self.mostrar_simular_cadena
        )

        self.btn_simular.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        # -----------------------------------------------------
        # CONVERTIR
        # -----------------------------------------------------

        self.btn_convertir = ctk.CTkButton(
            self.frame_menu,
            text="AFN → AFD",
            height=42,
            command=self.mostrar_conversion
        )

        self.btn_convertir.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        # -----------------------------------------------------
        # MINIMIZAR
        # -----------------------------------------------------

        self.btn_minimizar = ctk.CTkButton(
            self.frame_menu,
            text="Minimizar AFD",
            height=42,
            command=self.mostrar_minimizacion
        )

        self.btn_minimizar.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        # -----------------------------------------------------
        # DIAGRAMA
        # -----------------------------------------------------

        self.btn_diagrama = ctk.CTkButton(
            self.frame_menu,
            text="Ver diagrama",
            height=42,
            command=self.mostrar_diagrama
        )

        self.btn_diagrama.pack(
            padx=20,
            pady=5,
            fill="x"
        )

        # -----------------------------------------------------
        # REINICIAR AUTÓMATA
        # -----------------------------------------------------

        self.btn_reiniciar = ctk.CTkButton(
            self.frame_menu,
            text="Reiniciar autómata",
            height=42,
            command=self.reiniciar_automata,
            fg_color="#A93226",
            hover_color="#922B21"
        )

        self.btn_reiniciar.pack(
            padx=20,
            pady=(18, 5),
            fill="x"
        )

        # -----------------------------------------------------
        # APARIENCIA
        # -----------------------------------------------------

        self.lbl_apariencia = ctk.CTkLabel(
            self.frame_menu,
            text="Apariencia"
        )

        self.lbl_apariencia.pack(
            side="bottom",
            pady=(5, 5)
        )

        self.selector_apariencia = ctk.CTkOptionMenu(
            self.frame_menu,
            values=[
                "Sistema",
                "Claro",
                "Oscuro"
            ],
            command=self.cambiar_apariencia
        )

        self.selector_apariencia.set(
            "Sistema"
        )

        self.selector_apariencia.pack(
            side="bottom",
            padx=20,
            pady=(0, 20),
            fill="x"
        )

    # =========================================================
    # ÁREA PRINCIPAL
    # =========================================================

    def crear_area_principal(self):

        self.frame_contenido = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        self.frame_contenido.grid(
            row=0,
            column=1,
            padx=20,
            pady=(20, 60),
            sticky="nsew"
        )

        self.frame_contenido.grid_rowconfigure(
            0,
            weight=1
        )

        self.frame_contenido.grid_columnconfigure(
            0,
            weight=1
        )

    # =========================================================
    # BARRA DE ESTADO
    # =========================================================

    def crear_barra_estado(self):

        self.lbl_estado = ctk.CTkLabel(
            self,
            text=(
                "Estado: No hay un autómata cargado."
            ),
            anchor="w"
        )

        self.lbl_estado.grid(
            row=0,
            column=1,
            padx=25,
            pady=(0, 18),
            sticky="sew"
        )

    # =========================================================
    # LIMPIAR CONTENIDO
    # =========================================================

    def limpiar_contenido(self):

        for widget in (
            self.frame_contenido.winfo_children()
        ):
            widget.destroy()

    # =========================================================
    # INICIO
    # =========================================================

    def mostrar_inicio(self):

        self.limpiar_contenido()

        contenido = ctk.CTkScrollableFrame(
            self.frame_contenido,
            fg_color="transparent",
            corner_radius=0
        )

        contenido.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        contenido.grid_columnconfigure(
            0,
            weight=1
        )

        # -----------------------------------------------------
        # ENCABEZADO
        # -----------------------------------------------------

        titulo = ctk.CTkLabel(
            contenido,
            text="SIMULADOR DE AUTÓMATAS",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )

        titulo.grid(
            row=0,
            column=0,
            pady=(35, 8)
        )

        descripcion = ctk.CTkLabel(
            contenido,
            text=(
                "Construye, simula, convierte y "
                "minimiza autómatas finitos."
            ),
            font=ctk.CTkFont(
                size=17
            )
        )

        descripcion.grid(
            row=1,
            column=0,
            pady=5
        )

        descripcion2 = ctk.CTkLabel(
            contenido,
            text=(
                "Compatible con AFD, AFN y "
                "transiciones ε."
            ),
            font=ctk.CTkFont(
                size=15
            )
        )

        descripcion2.grid(
            row=2,
            column=0,
            pady=(0, 25)
        )

        # =====================================================
        # SIN AUTÓMATA
        # =====================================================

        if self.automata_actual is None:

            frame_sin_automata = ctk.CTkFrame(
                contenido
            )

            frame_sin_automata.grid(
                row=3,
                column=0,
                padx=50,
                pady=20,
                sticky="ew"
            )

            ctk.CTkLabel(
                frame_sin_automata,
                text="No hay un autómata cargado",
                font=ctk.CTkFont(
                    size=20,
                    weight="bold"
                )
            ).pack(
                pady=(25, 8)
            )

            ctk.CTkLabel(
                frame_sin_automata,
                text=(
                    "Cree un AFD o AFN para comenzar."
                ),
                font=ctk.CTkFont(
                    size=14
                )
            ).pack(
                pady=5
            )

            ctk.CTkButton(
                frame_sin_automata,
                text="Crear nuevo autómata",
                width=220,
                height=44,
                command=self.mostrar_crear_automata
            ).pack(
                pady=(15, 25)
            )

            return

        # =====================================================
        # AUTÓMATA CARGADO
        # =====================================================

        frame_actual = ctk.CTkFrame(
            contenido
        )

        frame_actual.grid(
            row=3,
            column=0,
            padx=50,
            pady=15,
            sticky="ew"
        )

        frame_actual.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            frame_actual,
            text="Autómata actual",
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(20, 15)
        )

        # -----------------------------------------------------
        # TIPO
        # -----------------------------------------------------

        ctk.CTkLabel(
            frame_actual,
            text="Tipo:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            padx=25,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            frame_actual,
            text=self.tipo_automata_actual
        ).grid(
            row=1,
            column=1,
            padx=25,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # NOMBRE
        # -----------------------------------------------------

        ctk.CTkLabel(
            frame_actual,
            text="Nombre:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=2,
            column=0,
            padx=25,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            frame_actual,
            text=self.automata_actual.nombre,
            wraplength=650,
            justify="left"
        ).grid(
            row=2,
            column=1,
            padx=25,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # ESTADOS
        # -----------------------------------------------------

        ctk.CTkLabel(
            frame_actual,
            text="Estados:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=3,
            column=0,
            padx=25,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            frame_actual,
            text=str(
                len(
                    self.automata_actual.estados
                )
            )
        ).grid(
            row=3,
            column=1,
            padx=25,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # TRANSICIONES
        # -----------------------------------------------------

        cantidad_transiciones = sum(
            len(destinos)
            for destinos
            in self.automata_actual.transiciones.values()
        )

        ctk.CTkLabel(
            frame_actual,
            text="Transiciones:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=4,
            column=0,
            padx=25,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            frame_actual,
            text=str(
                cantidad_transiciones
            )
        ).grid(
            row=4,
            column=1,
            padx=25,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # ESTADO INICIAL
        # -----------------------------------------------------

        ctk.CTkLabel(
            frame_actual,
            text="Estado inicial:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=5,
            column=0,
            padx=25,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            frame_actual,
            text=self.automata_actual.estado_inicial
        ).grid(
            row=5,
            column=1,
            padx=25,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # ESTADOS FINALES
        # -----------------------------------------------------

        finales = (
            "{"
            + ", ".join(
                sorted(
                    self.automata_actual.estados_finales
                )
            )
            + "}"
        )

        ctk.CTkLabel(
            frame_actual,
            text="Estados finales:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=6,
            column=0,
            padx=25,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            frame_actual,
            text=finales,
            wraplength=650,
            justify="left"
        ).grid(
            row=6,
            column=1,
            padx=25,
            pady=7,
            sticky="w"
        )

        # =====================================================
        # ACCESOS RÁPIDOS
        # =====================================================

        frame_acciones = ctk.CTkFrame(
            contenido
        )

        frame_acciones.grid(
            row=4,
            column=0,
            padx=50,
            pady=(10, 30),
            sticky="ew"
        )

        ctk.CTkLabel(
            frame_acciones,
            text="Acciones rápidas",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).pack(
            pady=(18, 12)
        )

        frame_botones = ctk.CTkFrame(
            frame_acciones,
            fg_color="transparent"
        )

        frame_botones.pack(
            pady=(0, 20)
        )

        ctk.CTkButton(
            frame_botones,
            text="Simular cadena",
            width=160,
            height=42,
            command=self.mostrar_simular_cadena
        ).grid(
            row=0,
            column=0,
            padx=8,
            pady=5
        )

        ctk.CTkButton(
            frame_botones,
            text="Ver diagrama",
            width=160,
            height=42,
            command=self.mostrar_diagrama
        ).grid(
            row=0,
            column=1,
            padx=8,
            pady=5
        )

        if self.tipo_automata_actual == "AFN":

            ctk.CTkButton(
                frame_botones,
                text="Convertir a AFD",
                width=160,
                height=42,
                command=self.mostrar_conversion
            ).grid(
                row=0,
                column=2,
                padx=8,
                pady=5
            )

        elif self.tipo_automata_actual == "AFD":

            ctk.CTkButton(
                frame_botones,
                text="Minimizar",
                width=160,
                height=42,
                command=self.mostrar_minimizacion
            ).grid(
                row=0,
                column=2,
                padx=8,
                pady=5
            )

    # =========================================================
    # CREAR AUTÓMATA
    # =========================================================

    def mostrar_crear_automata(self):

        # Si ya existe un autómata, advertimos
        if self.automata_actual is not None:

            respuesta = messagebox.askyesno(
                "Crear nuevo autómata",
                (
                    "Ya existe un autómata cargado:\n\n"
                    f"{self.automata_actual.nombre}\n\n"
                    "Si crea otro autómata, el actual "
                    "será reemplazado cuando guarde "
                    "el nuevo.\n\n"
                    "¿Desea continuar?"
                )
            )

            if not respuesta:
                return

        self.limpiar_contenido()

        formulario = CrearAutomataFrame(
            self.frame_contenido,
            self
        )

        formulario.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    # =========================================================
    # SIMULAR CADENA
    # =========================================================

    def mostrar_simular_cadena(self):

        self.limpiar_contenido()

        simulador = SimularCadenaFrame(
            self.frame_contenido,
            self
        )

        simulador.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    # =========================================================
    # CONVERSIÓN AFN -> AFD
    # =========================================================

    def mostrar_conversion(self):

        self.limpiar_contenido()

        conversion = ConversionAFNaAFDFrame(
            self.frame_contenido,
            self
        )

        conversion.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    # =========================================================
    # MINIMIZACIÓN
    # =========================================================

    def mostrar_minimizacion(self):

        self.limpiar_contenido()

        minimizacion = MinimizarAFDFrame(
            self.frame_contenido,
            self
        )

        minimizacion.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    # =========================================================
    # VER DIAGRAMA
    # =========================================================

    def mostrar_diagrama(self):

        self.limpiar_contenido()

        diagrama = VerDiagramaFrame(
            self.frame_contenido,
            self
        )

        diagrama.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

    # =========================================================
    # ESTABLECER AUTÓMATA ACTUAL
    # =========================================================

    def establecer_automata(
        self,
        automata,
        tipo
    ):

        self.automata_actual = automata

        self.tipo_automata_actual = tipo

        cantidad = sum(
            len(destinos)
            for destinos
            in automata.transiciones.values()
        )

        self.lbl_estado.configure(
            text=(
                f"Estado: {tipo} cargado - "
                f"{automata.nombre} | "
                f"{cantidad} transiciones"
            )
        )

        self.actualizar_estado_botones()

    # =========================================================
    # REINICIAR AUTÓMATA
    # =========================================================

    def reiniciar_automata(self):

        if self.automata_actual is None:
            return

        respuesta = messagebox.askyesno(
            "Reiniciar autómata",
            (
                "¿Está seguro de que desea eliminar "
                "el autómata actualmente cargado?\n\n"
                f"{self.tipo_automata_actual}: "
                f"{self.automata_actual.nombre}\n\n"
                "Esta acción eliminará el autómata "
                "de la sesión actual."
            )
        )

        if not respuesta:
            return

        self.automata_actual = None

        self.tipo_automata_actual = None

        self.lbl_estado.configure(
            text=(
                "Estado: No hay un autómata cargado."
            )
        )

        self.actualizar_estado_botones()

        self.mostrar_inicio()

        messagebox.showinfo(
            "Autómata reiniciado",
            (
                "El autómata fue eliminado "
                "de la sesión actual."
            )
        )

    # =========================================================
    # ACTIVAR / DESACTIVAR BOTONES
    # =========================================================

    def actualizar_estado_botones(self):

        if self.automata_actual is None:

            self.btn_guardar.configure(
                state="disabled"
            )

            self.btn_simular.configure(
                state="disabled"
            )

            self.btn_convertir.configure(
                state="disabled"
            )

            self.btn_minimizar.configure(
                state="disabled"
            )

            self.btn_diagrama.configure(
                state="disabled"
            )

            self.btn_reiniciar.configure(
                state="disabled"
            )

            return

        # -----------------------------------------------------
        # HAY AUTÓMATA
        # -----------------------------------------------------


        self.btn_simular.configure(
            state="normal"
        )

        self.btn_guardar.configure(
            state="normal"
        )

        self.btn_diagrama.configure(
            state="normal"
        )

        self.btn_reiniciar.configure(
            state="normal"
        )

        # -----------------------------------------------------
        # AFN
        # -----------------------------------------------------

        if self.tipo_automata_actual == "AFN":

            self.btn_convertir.configure(
                state="normal"
            )

            self.btn_minimizar.configure(
                state="disabled"
            )

        # -----------------------------------------------------
        # AFD
        # -----------------------------------------------------

        elif self.tipo_automata_actual == "AFD":

            self.btn_convertir.configure(
                state="disabled"
            )

            self.btn_minimizar.configure(
                state="normal"
            )

    # =========================================================
    # APARIENCIA
    # =========================================================

    def cambiar_apariencia(
        self,
        opcion
    ):

        if opcion == "Claro":

            ctk.set_appearance_mode(
                "light"
            )

        elif opcion == "Oscuro":

            ctk.set_appearance_mode(
                "dark"
            )

        else:

            ctk.set_appearance_mode(
                "system"
            )




    # =========================================================
    # GUARDAR AUTÓMATA
    # =========================================================

    def guardar_automata_actual(self):

        if self.automata_actual is None:

            messagebox.showwarning(
                "Sin autómata",
                (
                    "No existe ningún autómata "
                    "para guardar."
                )
            )

            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar autómata",
            defaultextension=".json",
            filetypes=[
                (
                    "Autómata JSON",
                    "*.json"
                ),
                (
                    "Todos los archivos",
                    "*.*"
                )
            ],
            initialfile=(
                self.automata_actual.nombre
                + ".json"
            )
        )

        # El usuario presionó Cancelar
        if not ruta:
            return

        try:

            ruta_final = guardar_automata(
                self.automata_actual,
                self.tipo_automata_actual,
                ruta
            )

            self.lbl_estado.configure(
                text=(
                    f"Estado: "
                    f"{self.tipo_automata_actual} - "
                    f"{self.automata_actual.nombre} | "
                    f"Guardado correctamente"
                )
            )

            messagebox.showinfo(
                "Autómata guardado",
                (
                    "El autómata fue guardado "
                    "correctamente.\n\n"
                    f"{ruta_final}"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error al guardar",
                (
                    "No fue posible guardar "
                    "el autómata.\n\n"
                    f"Detalle: {error}"
                )
            )



    # =========================================================
    # ABRIR AUTÓMATA
    # =========================================================

    def abrir_automata(self):

        # -----------------------------------------------------
        # AVISO SI YA EXISTE UNO
        # -----------------------------------------------------

        if self.automata_actual is not None:

            respuesta = messagebox.askyesno(
                "Abrir autómata",
                (
                    "Ya existe un autómata cargado:\n\n"
                    f"{self.automata_actual.nombre}\n\n"
                    "Si abre otro archivo, el autómata "
                    "actual será reemplazado.\n\n"
                    "¿Desea continuar?"
                )
            )

            if not respuesta:
                return

        # -----------------------------------------------------
        # SELECCIONAR ARCHIVO
        # -----------------------------------------------------

        ruta = filedialog.askopenfilename(
            title="Abrir autómata",
            filetypes=[
                (
                    "Autómata JSON",
                    "*.json"
                ),
                (
                    "Todos los archivos",
                    "*.*"
                )
            ]
        )

        if not ruta:
            return

        try:

            automata, tipo = cargar_automata(
                ruta
            )

            self.establecer_automata(
                automata,
                tipo
            )

            self.mostrar_inicio()

            messagebox.showinfo(
                "Autómata cargado",
                (
                    f"El {tipo} fue cargado "
                    "correctamente.\n\n"
                    f"Nombre: {automata.nombre}"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error al abrir",
                (
                    "No fue posible abrir "
                    "el autómata.\n\n"
                    f"Detalle: {error}"
                )
            )

