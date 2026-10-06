import customtkinter as ctk

from tkinter import messagebox

from modelos.expresion_regular import (
    ExpresionRegular
)

from algoritmos.procesador_regex import (
    procesar_expresion_regular
)

from algoritmos.integracion_regex import (
    validar_cadena_con_regex,
    generar_afn_desde_regex
)

from algoritmos.simulador import (
    formatear_resultado_afn
)

from utilidades.logs_validacion import (
    registrar_validacion
)


class ExpresionesRegularesFrame(
    ctk.CTkScrollableFrame
):

    def __init__(
        self,
        master,
        ventana_principal
    ):
        super().__init__(
            master,
            corner_radius=0,
            fg_color="transparent"
        )

        self.ventana_principal = (
            ventana_principal
        )

        self.regex_actual = None

        self.datos_procesados = None

        self.afn_generado = None

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.crear_encabezado()

        self.crear_formulario()

        self.crear_resultado()

        self.crear_generacion_automata()

        self.crear_validacion_cadena()

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        titulo = ctk.CTkLabel(
            self,
            text="Expresiones regulares",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        titulo.grid(
            row=0,
            column=0,
            pady=(20, 5)
        )

        descripcion = ctk.CTkLabel(
            self,
            text=(
                "Ingrese una expresión regular "
                "para analizarla, validar cadenas "
                "y generar su autómata."
            ),
            font=ctk.CTkFont(
                size=14
            )
        )

        descripcion.grid(
            row=1,
            column=0,
            pady=(0, 5)
        )

        descripcion2 = ctk.CTkLabel(
            self,
            text=(
                "Operadores disponibles: "
                "|   *   +   ?   ( )   ε"
            ),
            font=ctk.CTkFont(
                size=13
            )
        )

        descripcion2.grid(
            row=2,
            column=0,
            pady=(0, 15)
        )

    # =========================================================
    # FORMULARIO REGEX
    # =========================================================

    def crear_formulario(self):

        self.frame_formulario = (
            ctk.CTkFrame(
                self
            )
        )

        self.frame_formulario.grid(
            row=3,
            column=0,
            padx=30,
            pady=10,
            sticky="ew"
        )

        self.frame_formulario.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            self.frame_formulario,
            text="Ingresar expresión regular",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            padx=20,
            pady=(18, 15)
        )

        # -----------------------------------------------------
        # NOMBRE
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_formulario,
            text="Nombre:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=10,
            sticky="w"
        )

        self.entry_nombre = ctk.CTkEntry(
            self.frame_formulario,
            placeholder_text=(
                "Ejemplo: Termina en 01"
            ),
            height=40
        )

        self.entry_nombre.grid(
            row=1,
            column=1,
            columnspan=2,
            padx=(10, 20),
            pady=10,
            sticky="ew"
        )

        # -----------------------------------------------------
        # REGEX
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_formulario,
            text="Regex:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=2,
            column=0,
            padx=(20, 10),
            pady=10,
            sticky="w"
        )

        self.entry_regex = ctk.CTkEntry(
            self.frame_formulario,
            placeholder_text=(
                "Ejemplo: (0|1)*01"
            ),
            height=42
        )

        self.entry_regex.grid(
            row=2,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.entry_regex.bind(
            "<Return>",
            lambda event: self.analizar()
        )

        # -----------------------------------------------------
        # ANALIZAR
        # -----------------------------------------------------

        self.btn_analizar = (
            ctk.CTkButton(
                self.frame_formulario,
                text="Analizar",
                width=130,
                height=42,
                command=self.analizar
            )
        )

        self.btn_analizar.grid(
            row=2,
            column=2,
            padx=(10, 20),
            pady=10
        )

        # -----------------------------------------------------
        # LIMPIAR
        # -----------------------------------------------------

        self.btn_limpiar = (
            ctk.CTkButton(
                self.frame_formulario,
                text="Limpiar",
                width=130,
                height=40,
                command=self.limpiar
            )
        )

        self.btn_limpiar.grid(
            row=3,
            column=2,
            padx=(10, 20),
            pady=(5, 18)
        )

        # -----------------------------------------------------
        # EJEMPLOS
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_formulario,
            text=(
                "Ejemplos:  a|b     ab     "
                "(a|b)*     (0|1)*01     a|ε"
            ),
            font=ctk.CTkFont(
                size=12
            )
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            padx=20,
            pady=(5, 18)
        )

    # =========================================================
    # RESULTADO DEL ANÁLISIS
    # =========================================================

    def crear_resultado(self):

        self.frame_resultado = (
            ctk.CTkFrame(
                self
            )
        )

        self.frame_resultado.grid(
            row=4,
            column=0,
            padx=30,
            pady=10,
            sticky="ew"
        )

        self.frame_resultado.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            self.frame_resultado,
            text="Resultado del análisis",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 8)
        )

        self.lbl_estado = ctk.CTkLabel(
            self.frame_resultado,
            text=(
                "Ingrese una expresión regular "
                "y presione Analizar."
            ),
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        self.lbl_estado.grid(
            row=1,
            column=0,
            padx=20,
            pady=8
        )

        self.txt_resultado = (
            ctk.CTkTextbox(
                self.frame_resultado,
                height=230,
                font=(
                    "Consolas",
                    14
                )
            )
        )

        self.txt_resultado.grid(
            row=2,
            column=0,
            padx=20,
            pady=(5, 20),
            sticky="ew"
        )

        self.txt_resultado.configure(
            state="disabled"
        )

    # =========================================================
    # GENERAR AUTÓMATA
    # =========================================================

    def crear_generacion_automata(self):

        self.frame_generacion = ctk.CTkFrame(
            self
        )

        self.frame_generacion.grid(
            row=5,
            column=0,
            padx=30,
            pady=10,
            sticky="ew"
        )

        self.frame_generacion.grid_columnconfigure(
            0,
            weight=1
        )

        ctk.CTkLabel(
            self.frame_generacion,
            text="Generar autómata desde la regex",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(18, 8)
        )

        ctk.CTkLabel(
            self.frame_generacion,
            text=(
                "La expresión regular será convertida "
                "a un AFN-ε mediante la construcción "
                "de Thompson."
            ),
            font=ctk.CTkFont(
                size=13
            )
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            padx=20,
            pady=(0, 12)
        )

        self.lbl_generacion = ctk.CTkLabel(
            self.frame_generacion,
            text=(
                "Primero analice una expresión regular."
            ),
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        self.lbl_generacion.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=20,
            pady=8
        )

        self.btn_generar_afn = ctk.CTkButton(
            self.frame_generacion,
            text="Generar AFN",
            width=180,
            height=42,
            command=self.generar_afn
        )

        self.btn_generar_afn.grid(
            row=3,
            column=0,
            padx=(20, 10),
            pady=(8, 20),
            sticky="e"
        )

        self.btn_ver_afn = ctk.CTkButton(
            self.frame_generacion,
            text="Ver diagrama",
            width=180,
            height=42,
            command=(
                self.ventana_principal
                .mostrar_diagrama
            ),
            state="disabled"
        )

        self.btn_ver_afn.grid(
            row=3,
            column=1,
            padx=(10, 20),
            pady=(8, 20),
            sticky="w"
        )

    # =========================================================
    # VALIDACIÓN DE CADENA
    # =========================================================

    def crear_validacion_cadena(self):

        self.frame_validacion = ctk.CTkFrame(
            self
        )

        self.frame_validacion.grid(
            row=6,
            column=0,
            padx=30,
            pady=(10, 30),
            sticky="ew"
        )

        self.frame_validacion.grid_columnconfigure(
            1,
            weight=1
        )

        ctk.CTkLabel(
            self.frame_validacion,
            text="Validar cadena con la expresión regular",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            padx=20,
            pady=(18, 10)
        )

        # -----------------------------------------------------
        # CADENA
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_validacion,
            text="Cadena:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=10
        )

        self.entry_cadena = ctk.CTkEntry(
            self.frame_validacion,
            placeholder_text=(
                "Ejemplo: 1101"
            ),
            height=42
        )

        self.entry_cadena.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.entry_cadena.bind(
            "<Return>",
            lambda event: self.validar_cadena()
        )

        # -----------------------------------------------------
        # VALIDAR
        # -----------------------------------------------------

        self.btn_validar_cadena = ctk.CTkButton(
            self.frame_validacion,
            text="Validar cadena",
            width=140,
            height=42,
            command=self.validar_cadena
        )

        self.btn_validar_cadena.grid(
            row=1,
            column=2,
            padx=10,
            pady=10
        )

        # -----------------------------------------------------
        # LIMPIAR
        # -----------------------------------------------------

        self.btn_limpiar_cadena = ctk.CTkButton(
            self.frame_validacion,
            text="Limpiar",
            width=100,
            height=42,
            command=self.limpiar_validacion
        )

        self.btn_limpiar_cadena.grid(
            row=1,
            column=3,
            padx=(0, 20),
            pady=10
        )

        ctk.CTkLabel(
            self.frame_validacion,
            text=(
                "Puede dejar la cadena vacía para "
                "evaluar ε."
            ),
            font=ctk.CTkFont(
                size=12
            )
        ).grid(
            row=2,
            column=0,
            columnspan=4,
            padx=20,
            pady=(0, 10)
        )

        self.lbl_resultado_cadena = ctk.CTkLabel(
            self.frame_validacion,
            text=(
                "Ingrese una cadena para validarla."
            ),
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        self.lbl_resultado_cadena.grid(
            row=3,
            column=0,
            columnspan=4,
            padx=20,
            pady=10
        )

        self.txt_validacion = ctk.CTkTextbox(
            self.frame_validacion,
            height=300,
            font=(
                "Consolas",
                14
            )
        )

        self.txt_validacion.grid(
            row=4,
            column=0,
            columnspan=4,
            padx=20,
            pady=(5, 20),
            sticky="ew"
        )

        self.txt_validacion.configure(
            state="disabled"
        )

    # =========================================================
    # ANALIZAR REGEX
    # =========================================================

    def analizar(self):

        try:

            expresion = (
                self.entry_regex
                .get()
                .strip()
            )

            nombre = (
                self.entry_nombre
                .get()
                .strip()
            )

            if not nombre:

                nombre = (
                    "Expresión regular"
                )

            regex = ExpresionRegular(
                nombre=nombre,
                expresion=expresion
            )

            datos = (
                procesar_expresion_regular(
                    regex.expresion
                )
            )

            self.regex_actual = regex

            self.datos_procesados = datos

            self.afn_generado = None

            alfabeto = (
                "{"
                + ", ".join(
                    sorted(
                        regex.alfabeto
                    )
                )
                + "}"
            )

            texto = (
                f"Nombre: {regex.nombre}\n\n"
                f"Expresión original:\n"
                f"{datos['original']}\n\n"
                f"Expresión normalizada:\n"
                f"{datos['normalizada']}\n\n"
                f"Alfabeto detectado:\n"
                f"{alfabeto}\n\n"
                f"Concatenación explícita:\n"
                f"{datos['explicita']}\n\n"
                f"Notación postfija:\n"
                f"{datos['postfija']}"
            )

            self.mostrar_resultado(
                texto
            )

            self.lbl_estado.configure(
                text=(
                    "EXPRESIÓN REGULAR VÁLIDA"
                )
            )

            self.lbl_generacion.configure(
                text=(
                    "Regex lista para generar "
                    "su AFN-ε."
                )
            )

            self.btn_ver_afn.configure(
                state="disabled"
            )

            self.ventana_principal.lbl_estado.configure(
                text=(
                    "Estado: Expresión regular "
                    "analizada correctamente"
                )
            )

        except ValueError as error:

            self.regex_actual = None

            self.datos_procesados = None

            self.afn_generado = None

            self.lbl_estado.configure(
                text=(
                    "EXPRESIÓN REGULAR INVÁLIDA"
                )
            )

            self.lbl_generacion.configure(
                text=(
                    "No existe una regex válida "
                    "para generar el AFN."
                )
            )

            self.btn_ver_afn.configure(
                state="disabled"
            )

            self.limpiar_resultado()

            self.limpiar_validacion()

            messagebox.showerror(
                "Expresión regular inválida",
                str(error)
            )

    # =========================================================
    # GENERAR AFN DESDE REGEX
    # =========================================================

    def generar_afn(self):

        try:

            expresion = (
                self.entry_regex
                .get()
                .strip()
            )

            if not expresion:

                raise ValueError(
                    "Debe ingresar una expresión "
                    "regular."
                )

            if self.regex_actual is None:

                raise ValueError(
                    "Primero debe analizar la "
                    "expresión regular."
                )

            if (
                self.regex_actual.expresion
                != expresion
            ):

                raise ValueError(
                    "La expresión fue modificada. "
                    "Presione Analizar nuevamente "
                    "antes de generar el AFN."
                )

            # -------------------------------------------------
            # Si existe otro autómata cargado preguntamos
            # antes de reemplazarlo.
            # -------------------------------------------------

            if (
                self.ventana_principal
                .automata_actual
                is not None
            ):

                actual = (
                    self.ventana_principal
                    .automata_actual
                    .nombre
                )

                respuesta = messagebox.askyesno(
                    "Reemplazar autómata",
                    (
                        "Ya existe un autómata "
                        "cargado:\n\n"
                        f"{actual}\n\n"
                        "El AFN generado desde la "
                        "expresión regular lo "
                        "reemplazará en la sesión "
                        "actual.\n\n"
                        "¿Desea continuar?"
                    )
                )

                if not respuesta:

                    return

            nombre = (
                self.entry_nombre
                .get()
                .strip()
            )

            if nombre:

                nombre_afn = (
                    f"AFN - {nombre}"
                )

            else:

                nombre_afn = (
                    f"AFN de regex: {expresion}"
                )

            afn = generar_afn_desde_regex(
                expresion,
                nombre=nombre_afn
            )

            self.afn_generado = afn

            # -------------------------------------------------
            # Convertimos el AFN generado en el autómata
            # actual de toda la aplicación.
            # -------------------------------------------------

            self.ventana_principal.establecer_automata(
                afn,
                "AFN"
            )

            cantidad_transiciones = sum(
                len(destinos)
                for destinos
                in afn.transiciones.values()
            )

            self.lbl_generacion.configure(
                text=(
                    f"AFN GENERADO Y CARGADO\n"
                    f"{afn.nombre}\n"
                    f"Estados: "
                    f"{len(afn.estados)} | "
                    f"Transiciones: "
                    f"{cantidad_transiciones}"
                )
            )

            self.btn_ver_afn.configure(
                state="normal"
            )

            messagebox.showinfo(
                "AFN generado",
                (
                    "La expresión regular fue "
                    "convertida correctamente "
                    "a un AFN-ε mediante Thompson.\n\n"
                    f"Nombre: {afn.nombre}\n"
                    f"Estados: "
                    f"{len(afn.estados)}\n"
                    f"Transiciones: "
                    f"{cantidad_transiciones}\n\n"
                    "El AFN ahora es el autómata "
                    "actual de la aplicación."
                )
            )

        except ValueError as error:

            messagebox.showerror(
                "No se pudo generar el AFN",
                str(error)
            )

        except Exception as error:

            messagebox.showerror(
                "Error al generar AFN",
                (
                    "Ocurrió un error al generar "
                    "el autómata.\n\n"
                    f"Detalle: {error}"
                )
            )

    # =========================================================
    # VALIDAR CADENA
    # =========================================================

    def validar_cadena(self):

        try:

            expresion = (
                self.entry_regex
                .get()
                .strip()
            )

            if not expresion:

                raise ValueError(
                    "Debe ingresar una expresión "
                    "regular antes de validar la cadena."
                )

            cadena = (
                self.entry_cadena
                .get()
            )

            regex = ExpresionRegular(
                nombre=(
                    self.entry_nombre
                    .get()
                    .strip()
                    or "Expresión regular"
                ),
                expresion=expresion
            )

            procesar_expresion_regular(
                regex.expresion
            )

            resultado = (
                validar_cadena_con_regex(
                    regex.expresion,
                    cadena
                )
            )

            registrar_validacion(
                resultado["expresion"],
                cadena,
                resultado["aceptada"]
            )

            detalle = (
                formatear_resultado_afn(
                    resultado["detalle"]
                )
            )

            texto = (
                f"Expresión regular: "
                f"{resultado['expresion']}\n"
                f"Cadena evaluada: "
                f"{cadena if cadena else 'ε'}\n\n"
                f"{detalle}"
            )

            self.mostrar_validacion(
                texto
            )

            if resultado["aceptada"]:

                self.lbl_resultado_cadena.configure(
                    text="CADENA ACEPTADA"
                )

                estado = (
                    "Cadena aceptada por la regex"
                )

            else:

                self.lbl_resultado_cadena.configure(
                    text="CADENA RECHAZADA"
                )

                estado = (
                    "Cadena rechazada por la regex"
                )

            self.ventana_principal.lbl_estado.configure(
                text=(
                    f"Estado: {estado}"
                )
            )

        except ValueError as error:

            self.lbl_resultado_cadena.configure(
                text="NO FUE POSIBLE VALIDAR"
            )

            self.limpiar_texto_validacion()

            messagebox.showerror(
                "Validación inválida",
                str(error)
            )

    # =========================================================
    # MOSTRAR ANÁLISIS
    # =========================================================

    def mostrar_resultado(
        self,
        texto
    ):

        self.txt_resultado.configure(
            state="normal"
        )

        self.txt_resultado.delete(
            "1.0",
            "end"
        )

        self.txt_resultado.insert(
            "end",
            texto
        )

        self.txt_resultado.configure(
            state="disabled"
        )

    # =========================================================
    # MOSTRAR VALIDACIÓN
    # =========================================================

    def mostrar_validacion(
        self,
        texto
    ):

        self.txt_validacion.configure(
            state="normal"
        )

        self.txt_validacion.delete(
            "1.0",
            "end"
        )

        self.txt_validacion.insert(
            "end",
            texto
        )

        self.txt_validacion.configure(
            state="disabled"
        )

    # =========================================================
    # LIMPIAR RESULTADO
    # =========================================================

    def limpiar_resultado(self):

        self.txt_resultado.configure(
            state="normal"
        )

        self.txt_resultado.delete(
            "1.0",
            "end"
        )

        self.txt_resultado.configure(
            state="disabled"
        )

    # =========================================================
    # LIMPIAR TEXTO VALIDACIÓN
    # =========================================================

    def limpiar_texto_validacion(self):

        self.txt_validacion.configure(
            state="normal"
        )

        self.txt_validacion.delete(
            "1.0",
            "end"
        )

        self.txt_validacion.configure(
            state="disabled"
        )

    # =========================================================
    # LIMPIAR VALIDACIÓN
    # =========================================================

    def limpiar_validacion(self):

        self.entry_cadena.delete(
            0,
            "end"
        )

        self.lbl_resultado_cadena.configure(
            text=(
                "Ingrese una cadena para validarla."
            )
        )

        self.limpiar_texto_validacion()

    # =========================================================
    # LIMPIAR TODO
    # =========================================================

    def limpiar(self):

        self.entry_nombre.delete(
            0,
            "end"
        )

        self.entry_regex.delete(
            0,
            "end"
        )

        self.regex_actual = None

        self.datos_procesados = None

        self.afn_generado = None

        self.lbl_estado.configure(
            text=(
                "Ingrese una expresión regular "
                "y presione Analizar."
            )
        )

        self.lbl_generacion.configure(
            text=(
                "Primero analice una "
                "expresión regular."
            )
        )

        self.btn_ver_afn.configure(
            state="disabled"
        )

        self.limpiar_resultado()

        self.limpiar_validacion()

        self.entry_regex.focus()