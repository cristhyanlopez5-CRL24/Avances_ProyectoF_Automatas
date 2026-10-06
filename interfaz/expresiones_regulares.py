import customtkinter as ctk

from tkinter import messagebox

from modelos.expresion_regular import (
    ExpresionRegular
)

from algoritmos.procesador_regex import (
    procesar_expresion_regular
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

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.crear_encabezado()

        self.crear_formulario()

        self.crear_resultado()

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
                "para analizar su estructura."
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
    # FORMULARIO
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

        # -----------------------------------------------------
        # TÍTULO
        # -----------------------------------------------------

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
        # EXPRESIÓN
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
    # RESULTADO
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
            pady=(10, 30),
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
                height=260,
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
    # ANALIZAR
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

            self.ventana_principal.lbl_estado.configure(
                text=(
                    "Estado: Expresión regular "
                    "analizada correctamente"
                )
            )

        except ValueError as error:

            self.regex_actual = None

            self.datos_procesados = None

            self.lbl_estado.configure(
                text=(
                    "EXPRESIÓN REGULAR INVÁLIDA"
                )
            )

            self.limpiar_resultado()

            messagebox.showerror(
                "Expresión regular inválida",
                str(error)
            )

    # =========================================================
    # MOSTRAR RESULTADO
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

        self.lbl_estado.configure(
            text=(
                "Ingrese una expresión regular "
                "y presione Analizar."
            )
        )

        self.limpiar_resultado()

        self.entry_regex.focus()