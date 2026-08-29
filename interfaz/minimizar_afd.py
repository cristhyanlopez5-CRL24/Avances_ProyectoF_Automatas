import customtkinter as ctk

from tkinter import messagebox

from algoritmos.minimizacion import (
    minimizar_afd,
    obtener_estados_alcanzables,
    formatear_minimizacion
)


class MinimizarAFDFrame(ctk.CTkScrollableFrame):

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

        self.automata = (
            ventana_principal.automata_actual
        )

        self.tipo = (
            ventana_principal.tipo_automata_actual
        )

        # Aquí guardaremos el resultado
        self.afd_minimo = None

        # =====================================================
        # CONFIGURACIÓN
        # =====================================================

        self.grid_columnconfigure(
            0,
            weight=1
        )

        # =====================================================
        # INTERFAZ
        # =====================================================

        self.crear_encabezado()

        self.crear_informacion_afd()

        self.crear_controles()

        self.crear_resultado()

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        lbl_titulo = ctk.CTkLabel(
            self,
            text="Minimización de AFD",
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
                "Reduce el AFD eliminando estados "
                "inalcanzables y agrupando estados equivalentes."
            ),
            font=ctk.CTkFont(
                size=14
            ),
            wraplength=850,
            justify="center"
        )

        lbl_descripcion.grid(
            row=1,
            column=0,
            padx=30,
            pady=(0, 15)
        )

    # =========================================================
    # INFORMACIÓN DEL AFD
    # =========================================================

    def crear_informacion_afd(self):

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
        # NO HAY AUTÓMATA
        # -----------------------------------------------------

        if self.automata is None:

            ctk.CTkLabel(
                self.frame_info,
                text=(
                    "No hay ningún autómata cargado.\n"
                    "Primero debe crear o convertir un AFD."
                ),
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).grid(
                row=0,
                column=0,
                columnspan=2,
                padx=20,
                pady=25
            )

            return

        # -----------------------------------------------------
        # NO ES AFD
        # -----------------------------------------------------

        if self.tipo != "AFD":

            ctk.CTkLabel(
                self.frame_info,
                text=(
                    f"El autómata actual es de tipo {self.tipo}.\n"
                    "La minimización solamente puede "
                    "realizarse sobre un AFD.\n\n"
                    "Puede utilizar primero la opción AFN → AFD."
                ),
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            ).grid(
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
            text="AFD"
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
            text=self.automata.nombre,
            wraplength=700,
            justify="left"
        ).grid(
            row=1,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # ESTADOS
        # -----------------------------------------------------

        estados = (
            "{"
            + ", ".join(
                sorted(
                    self.automata.estados
                )
            )
            + "}"
        )

        ctk.CTkLabel(
            self.frame_info,
            text="Estados:",
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
            text=estados,
            wraplength=700,
            justify="left"
        ).grid(
            row=2,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # CANTIDAD DE ESTADOS
        # -----------------------------------------------------

        ctk.CTkLabel(
            self.frame_info,
            text="Cantidad de estados:",
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
            text=str(
                len(
                    self.automata.estados
                )
            )
        ).grid(
            row=3,
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
            row=4,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=self.automata.estado_inicial
        ).grid(
            row=4,
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
            row=5,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=finales
        ).grid(
            row=5,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

        # -----------------------------------------------------
        # ALCANZABLES
        # -----------------------------------------------------

        alcanzables = obtener_estados_alcanzables(
            self.automata
        )

        ctk.CTkLabel(
            self.frame_info,
            text="Estados alcanzables:",
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=6,
            column=0,
            padx=20,
            pady=7,
            sticky="w"
        )

        ctk.CTkLabel(
            self.frame_info,
            text=str(
                len(alcanzables)
            )
        ).grid(
            row=6,
            column=1,
            padx=20,
            pady=7,
            sticky="w"
        )

    # =========================================================
    # CONTROLES
    # =========================================================

    def crear_controles(self):

        self.frame_controles = ctk.CTkFrame(
            self
        )

        self.frame_controles.grid(
            row=3,
            column=0,
            padx=30,
            pady=10,
            sticky="ew"
        )

        self.frame_controles.grid_columnconfigure(
            0,
            weight=1
        )

        self.lbl_estado_minimizacion = ctk.CTkLabel(
            self.frame_controles,
            text=(
                "Presione Minimizar para analizar "
                "los estados del AFD."
            ),
            font=ctk.CTkFont(
                size=14
            )
        )

        self.lbl_estado_minimizacion.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(15, 10)
        )

        # -----------------------------------------------------
        # MINIMIZAR
        # -----------------------------------------------------

        self.btn_minimizar = ctk.CTkButton(
            self.frame_controles,
            text="Minimizar AFD",
            width=200,
            height=42,
            command=self.minimizar
        )

        self.btn_minimizar.grid(
            row=1,
            column=0,
            padx=10,
            pady=(5, 20)
        )

        # -----------------------------------------------------
        # USAR AFD MÍNIMO
        # -----------------------------------------------------

        self.btn_usar_minimo = ctk.CTkButton(
            self.frame_controles,
            text="Usar AFD mínimo",
            width=200,
            height=42,
            command=self.usar_afd_minimo,
            state="disabled"
        )

        self.btn_usar_minimo.grid(
            row=1,
            column=1,
            padx=10,
            pady=(5, 20)
        )

        # -----------------------------------------------------
        # DESHABILITAR
        # -----------------------------------------------------

        if (
            self.automata is None
            or self.tipo != "AFD"
        ):

            self.btn_minimizar.configure(
                state="disabled"
            )

            self.lbl_estado_minimizacion.configure(
                text=(
                    "Debe cargar un AFD para "
                    "utilizar esta función."
                )
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

        ctk.CTkLabel(
            self.frame_resultado,
            text="Resultado de la minimización",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 5)
        )

        # -----------------------------------------------------
        # RESUMEN
        # -----------------------------------------------------

        self.lbl_resumen = ctk.CTkLabel(
            self.frame_resultado,
            text=(
                "Todavía no se ha realizado "
                "ninguna minimización."
            ),
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        self.lbl_resumen.grid(
            row=1,
            column=0,
            padx=20,
            pady=10
        )

        # -----------------------------------------------------
        # TEXTO
        # -----------------------------------------------------

        self.txt_resultado = ctk.CTkTextbox(
            self.frame_resultado,
            height=400,
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
    # MINIMIZAR
    # =========================================================

    def minimizar(self):

        if self.automata is None:

            messagebox.showwarning(
                "Sin autómata",
                (
                    "Primero debe crear "
                    "o convertir un AFD."
                )
            )

            return

        if self.tipo != "AFD":

            messagebox.showwarning(
                "Tipo incorrecto",
                (
                    "La minimización solamente "
                    "puede realizarse sobre un AFD."
                )
            )

            return

        try:

            # =================================================
            # MINIMIZAR
            # =================================================

            self.afd_minimo = minimizar_afd(
                self.automata
            )

            # =================================================
            # INFORMACIÓN GENERAL
            # =================================================

            cantidad_original = len(
                self.automata.estados
            )

            cantidad_minima = len(
                self.afd_minimo.estados
            )

            eliminados = (
                cantidad_original
                - cantidad_minima
            )

            # =================================================
            # FORMATEAR RESULTADO
            # =================================================

            texto = formatear_minimizacion(
                self.afd_minimo
            )

            # Agregamos una comparación
            texto_completo = (
                "=" * 60
                + "\n"
                + "COMPARACIÓN\n"
                + "=" * 60
                + "\n\n"
                + f"Estados del AFD original: {cantidad_original}\n"
                + f"Estados del AFD mínimo:   {cantidad_minima}\n"
                + f"Reducción total:          {eliminados}\n\n"
                + texto
            )

            # =================================================
            # MOSTRAR
            # =================================================

            self.txt_resultado.configure(
                state="normal"
            )

            self.txt_resultado.delete(
                "1.0",
                "end"
            )

            self.txt_resultado.insert(
                "end",
                texto_completo
            )

            self.txt_resultado.configure(
                state="disabled"
            )

            # =================================================
            # RESUMEN
            # =================================================

            if cantidad_minima < cantidad_original:

                self.lbl_resumen.configure(
                    text=(
                        f"Minimización completada: "
                        f"{cantidad_original} estados → "
                        f"{cantidad_minima} estados"
                    )
                )

            else:

                self.lbl_resumen.configure(
                    text=(
                        "El AFD ya era mínimo: "
                        f"{cantidad_minima} estados."
                    )
                )

            self.lbl_estado_minimizacion.configure(
                text=(
                    "AFD mínimo generado correctamente."
                )
            )

            self.btn_usar_minimo.configure(
                state="normal"
            )

            self.ventana_principal.lbl_estado.configure(
                text=(
                    f"Estado: AFD - "
                    f"{self.automata.nombre} | "
                    f"Minimización completada"
                )
            )

        except Exception as error:

            messagebox.showerror(
                "Error de minimización",
                (
                    "No fue posible minimizar "
                    "el AFD.\n\n"
                    f"Detalle: {error}"
                )
            )

    # =========================================================
    # USAR AFD MÍNIMO
    # =========================================================

    def usar_afd_minimo(self):

        if self.afd_minimo is None:

            messagebox.showwarning(
                "Sin minimización",
                (
                    "Primero debe minimizar "
                    "el AFD."
                )
            )

            return

        respuesta = messagebox.askyesno(
            "Usar AFD mínimo",
            (
                "¿Desea utilizar el AFD mínimo "
                "como autómata actual?\n\n"
                "Después podrá simular cadenas "
                "y visualizar su diagrama."
            )
        )

        if not respuesta:
            return

        self.ventana_principal.establecer_automata(
            self.afd_minimo,
            "AFD"
        )

        self.automata = self.afd_minimo

        self.lbl_estado_minimizacion.configure(
            text=(
                "El AFD mínimo fue cargado "
                "como autómata actual."
            )
        )

        self.btn_usar_minimo.configure(
            state="disabled"
        )

        messagebox.showinfo(
            "AFD mínimo cargado",
            (
                "El AFD mínimo ahora es "
                "el autómata actual."
            )
        )