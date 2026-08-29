import customtkinter as ctk

from tkinter import messagebox

from algoritmos.simulador import (
    simular_afd_detallado,
    formatear_resultado_afd,
    simular_afn_detallado,
    formatear_resultado_afn
)

from utilidades.validaciones import (
    validar_cadena
)


class SimularCadenaFrame(ctk.CTkScrollableFrame):

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

        self.ventana_principal = ventana_principal

        self.automata = (
            ventana_principal.automata_actual
        )

        self.tipo = (
            ventana_principal.tipo_automata_actual
        )

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # =====================================================
        # CREAR INTERFAZ
        # =====================================================

        self.crear_encabezado()

        self.crear_informacion_automata()

        self.crear_formulario()

        self.crear_resultado()

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        lbl_titulo = ctk.CTkLabel(
            self,
            text="Simular cadena",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        lbl_titulo.grid(
            row=0,
            column=0,
            pady=(20, 5)
        )

        lbl_descripcion = ctk.CTkLabel(
            self,
            text=(
                "Ingrese una cadena para comprobar si "
                "el autómata la acepta o la rechaza."
            ),
            font=ctk.CTkFont(
                size=14
            )
        )

        lbl_descripcion.grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

    # =========================================================
    # INFORMACIÓN DEL AUTÓMATA
    # =========================================================

    def crear_informacion_automata(self):

        self.frame_info = ctk.CTkFrame(
            self
        )

        self.frame_info.grid(
            row=2,
            column=0,
            padx=30,
            pady=10,
            sticky="ew"
        )

        self.frame_info.grid_columnconfigure(
            1,
            weight=1
        )

        # -----------------------------------------------------
        # SIN AUTÓMATA
        # -----------------------------------------------------

        if self.automata is None:

            lbl_sin_automata = ctk.CTkLabel(
                self.frame_info,
                text=(
                    "No hay ningún autómata cargado.\n"
                    "Primero debe crear un AFD o AFN."
                ),
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            )

            lbl_sin_automata.grid(
                row=0,
                column=0,
                columnspan=2,
                padx=20,
                pady=25
            )

            return

        # -----------------------------------------------------
        # TIPO
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_info,
            text="Tipo:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=self.tipo
        ).grid(
            row=0,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # NOMBRE
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_info,
            text="Autómata:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=1,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=self.automata.nombre
        ).grid(
            row=1,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # ALFABETO
        # -----------------------------------------------------

        alfabeto = (
            "{"
            + ", ".join(
                sorted(
                    self.automata.alfabeto
                )
            )
            + "}"
        )

        ctk.CTkLabel(
            self.frame_info,
            text="Alfabeto:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=2,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=alfabeto
        ).grid(
            row=2,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # ESTADO INICIAL
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_info,
            text="Estado inicial:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=3,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=self.automata.estado_inicial
        ).grid(
            row=3,
            column=1,
            padx=20,
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
                    self.automata.estados_finales
                )
            )
            + "}"
        )

        ctk.CTkLabel(
            self.frame_info,
            text="Estados finales:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=4,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=finales
        ).grid(
            row=4,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

    # =========================================================
    # FORMULARIO DE CADENA
    # =========================================================

    def crear_formulario(self):

        self.frame_simulacion = ctk.CTkFrame(
            self
        )

        self.frame_simulacion.grid(
            row=3,
            column=0,
            padx=30,
            pady=15,
            sticky="ew"
        )

        self.frame_simulacion.grid_columnconfigure(
            1,
            weight=1
        )

        # -----------------------------------------------------
        # TÍTULO
        # -----------------------------------------------------

        lbl_titulo = ctk.CTkLabel(
            self.frame_simulacion,
            text="Cadena a evaluar",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        lbl_titulo.grid(
            row=0,
            column=0,
            columnspan=4,
            padx=20,
            pady=(15, 5)
        )

        # -----------------------------------------------------
        # CAMPO CADENA
        # -----------------------------------------------------

        lbl_cadena = ctk.CTkLabel(
            self.frame_simulacion,
            text="Cadena:",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        lbl_cadena.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=20
        )

        self.entry_cadena = ctk.CTkEntry(
            self.frame_simulacion,
            placeholder_text="Ejemplo: 00101",
            height=42
        )

        self.entry_cadena.grid(
            row=1,
            column=1,
            padx=10,
            pady=20,
            sticky="ew"
        )

        # Permitir usar Enter para simular
        self.entry_cadena.bind(
            "<Return>",
            lambda event: self.simular()
        )

        # -----------------------------------------------------
        # BOTÓN SIMULAR
        # -----------------------------------------------------

        self.btn_simular = ctk.CTkButton(
            self.frame_simulacion,
            text="Simular",
            height=42,
            width=130,
            command=self.simular
        )

        self.btn_simular.grid(
            row=1,
            column=2,
            padx=10,
            pady=20
        )

        # -----------------------------------------------------
        # BOTÓN LIMPIAR
        # -----------------------------------------------------

        self.btn_limpiar = ctk.CTkButton(
            self.frame_simulacion,
            text="Limpiar",
            height=42,
            width=100,
            command=self.limpiar
        )

        self.btn_limpiar.grid(
            row=1,
            column=3,
            padx=(0, 20),
            pady=20
        )

        # -----------------------------------------------------
        # NOTA SOBRE CADENA VACÍA
        # -----------------------------------------------------

        lbl_nota = ctk.CTkLabel(
            self.frame_simulacion,
            text=(
                "Puede dejar el campo vacío para evaluar "
                "la cadena ε."
            ),
            font=ctk.CTkFont(
                size=12
            )
        )

        lbl_nota.grid(
            row=2,
            column=0,
            columnspan=4,
            padx=20,
            pady=(0, 15)
        )

        # -----------------------------------------------------
        # DESHABILITAR SI NO HAY AUTÓMATA
        # -----------------------------------------------------

        if self.automata is None:

            self.entry_cadena.configure(
                state="disabled"
            )

            self.btn_simular.configure(
                state="disabled"
            )

    # =========================================================
    # RESULTADO
    # =========================================================

    def crear_resultado(self):

        self.frame_resultado = ctk.CTkFrame(
            self
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

        # -----------------------------------------------------
        # TÍTULO
        # -----------------------------------------------------

        lbl_titulo = ctk.CTkLabel(
            self.frame_resultado,
            text="Resultado de la simulación",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            )
        )

        lbl_titulo.grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 5)
        )

        # -----------------------------------------------------
        # ACEPTADA / RECHAZADA
        # -----------------------------------------------------

        self.lbl_estado_resultado = (
            ctk.CTkLabel(
                self.frame_resultado,
                text=(
                    "Ingrese una cadena y "
                    "presione Simular."
                ),
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            )
        )

        self.lbl_estado_resultado.grid(
            row=1,
            column=0,
            padx=20,
            pady=10
        )

        # -----------------------------------------------------
        # RECORRIDO
        # -----------------------------------------------------

        self.txt_resultado = ctk.CTkTextbox(
            self.frame_resultado,
            height=280,
            font=(
                "Consolas",
                14
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
    # SIMULAR
    # =========================================================

    def simular(self):

        if self.automata is None:

            messagebox.showwarning(
                "Sin autómata",
                (
                    "Primero debe crear "
                    "un autómata."
                )
            )

            return

        try:

            cadena = validar_cadena(
                self.entry_cadena.get(),
                self.automata.alfabeto
            )

            # =================================================
            # AFD
            # =================================================

            if self.tipo == "AFD":

                resultado = simular_afd_detallado(
                    self.automata,
                    cadena
                )

                texto = formatear_resultado_afd(
                    resultado
                )

            # =================================================
            # AFN
            # =================================================

            elif self.tipo == "AFN":

                resultado = simular_afn_detallado(
                    self.automata,
                    cadena
                )

                texto = formatear_resultado_afn(
                    resultado
                )

            else:

                raise ValueError(
                    "Tipo de autómata desconocido."
                )

            # =================================================
            # MOSTRAR RESULTADO
            # =================================================

            self.mostrar_resultado(
                texto,
                resultado["aceptada"]
            )

            if resultado["aceptada"]:

                estado_texto = (
                    "Cadena aceptada"
                )

            else:

                estado_texto = (
                    "Cadena rechazada"
                )

            self.ventana_principal.lbl_estado.configure(
                text=(
                    f"Estado: {self.tipo} - "
                    f"{self.automata.nombre} | "
                    f"{estado_texto}"
                )
            )

        except ValueError as error:

            messagebox.showerror(
                "Cadena inválida",
                str(error)
            )

    # =========================================================
    # MOSTRAR RESULTADO
    # =========================================================

    def mostrar_resultado(
        self,
        texto,
        aceptada
    ):

        if aceptada:

            self.lbl_estado_resultado.configure(
                text="CADENA ACEPTADA ✓"
            )

        else:

            self.lbl_estado_resultado.configure(
                text="CADENA RECHAZADA ✗"
            )

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
    # LIMPIAR
    # =========================================================

    def limpiar(self):

        if self.automata is not None:

            self.entry_cadena.configure(
                state="normal"
            )

            self.entry_cadena.delete(
                0,
                "end"
            )

        self.lbl_estado_resultado.configure(
            text=(
                "Ingrese una cadena y "
                "presione Simular."
            )
        )

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