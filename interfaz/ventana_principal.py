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

from interfaz.expresiones_regulares import (
    ExpresionesRegularesFrame
)

from interfaz.validacion_logs import (
    ValidacionLogsFrame
)

from utilidades.persistencia import (
    guardar_automata,
    cargar_automata
)

from utilidades.registro_logs import (
    registrar_info,
    registrar_warning,
    registrar_error
)

from utilidades.tema import (
    FONDO_APP,
    FONDO_PANEL,
    TEXTO_TITULO,
    TEXTO_NORMAL,
    TEXTO_SUAVE,
    TEXTO_DESHABILITADO,
    BOTON_PRINCIPAL,
    BOTON_PRINCIPAL_HOVER,
    TEXTO_BOTON,
    BOTON_PELIGRO,
    BOTON_PELIGRO_HOVER,
    COLOR_BORDE,
    COLOR_EXITO,
    COLOR_ADVERTENCIA,
    COLOR_ERROR
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

        self.configure(
            fg_color=FONDO_APP
        )

        self.automata_actual = None

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
    # BOTÓN PRINCIPAL DEL MENÚ
    # =========================================================

    def crear_boton_menu(
        self,
        texto,
        comando
    ):

        boton = ctk.CTkButton(
            self.frame_botones_menu,
            text=texto,
            height=36,
            command=comando,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
           text_color_disabled=TEXTO_DESHABILITADO,
            corner_radius=8,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        boton.pack(
            padx=8,
            pady=3,
            fill="x"
        )

        return boton

        # =========================================================
    # MENÚ LATERAL
    # =========================================================

    def crear_menu_lateral(self):

        self.frame_menu = ctk.CTkFrame(
            self,
            width=225,
            corner_radius=0,
            fg_color=FONDO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
        )

        self.frame_menu.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.frame_menu.grid_propagate(
            False
        )

        self.frame_menu.grid_columnconfigure(
            0,
            weight=1
        )

        self.frame_menu.grid_rowconfigure(
            1,
            weight=1
        )

        # =====================================================
        # ENCABEZADO
        # =====================================================

        frame_encabezado = ctk.CTkFrame(
            self.frame_menu,
            fg_color="transparent"
        )

        frame_encabezado.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(12, 5)
        )

        self.lbl_titulo = ctk.CTkLabel(
            frame_encabezado,
            text="AUTÓMATAS",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        self.lbl_titulo.pack(
            pady=(3, 1)
        )

        self.lbl_subtitulo = ctk.CTkLabel(
            frame_encabezado,
            text="Simulador",
            text_color=TEXTO_SUAVE,
            font=ctk.CTkFont(
                size=14
            )
        )

        self.lbl_subtitulo.pack(
            pady=(0, 5)
        )

        # =====================================================
        # BOTONES DEL MENÚ
        # =====================================================

        self.frame_botones_menu = ctk.CTkFrame(
            self.frame_menu,
            fg_color="transparent",
            corner_radius=0
        )

        self.frame_botones_menu.grid(
            row=1,
            column=0,
            sticky="new",
            padx=10,
            pady=(3, 5)
        )

        self.btn_inicio = (
            self.crear_boton_menu(
                "Inicio",
                self.mostrar_inicio
            )
        )

        self.btn_nuevo = (
            self.crear_boton_menu(
                "Nuevo autómata",
                self.mostrar_crear_automata
            )
        )

        self.btn_regex = (
            self.crear_boton_menu(
                "Expresiones regulares",
                self.mostrar_regex
            )
        )

        self.btn_abrir = (
            self.crear_boton_menu(
                "Abrir autómata",
                self.abrir_automata
            )
        )

        self.btn_guardar = (
            self.crear_boton_menu(
                "Guardar autómata",
                self.guardar_automata_actual
            )
        )

        self.btn_simular = (
            self.crear_boton_menu(
                "Simular cadena",
                self.mostrar_simular_cadena
            )
        )

        self.btn_convertir = (
            self.crear_boton_menu(
                "AFN → AFD",
                self.mostrar_conversion
            )
        )

        self.btn_minimizar = (
            self.crear_boton_menu(
                "Minimizar AFD",
                self.mostrar_minimizacion
            )
        )

        self.btn_diagrama = (
            self.crear_boton_menu(
                "Ver diagrama",
                self.mostrar_diagrama
            )
        )

        # =====================================================
        # REINICIAR AUTÓMATA
        # =====================================================

        self.btn_reiniciar = ctk.CTkButton(
            self.frame_botones_menu,
            text="Reiniciar autómata",
            height=36,
            command=self.reiniciar_automata,
            fg_color=BOTON_PELIGRO,
            hover_color=BOTON_PELIGRO_HOVER,
            text_color=TEXTO_BOTON,
            text_color_disabled=(
                "#969696",
                "#A8A8A8"
            ),
            corner_radius=8,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.btn_reiniciar.pack(
            padx=8,
            pady=(9, 3),
            fill="x"
        )

        # =====================================================
        # APARIENCIA FIJA ABAJO
        # =====================================================

        self.frame_apariencia = ctk.CTkFrame(
            self.frame_menu,
            fg_color="transparent"
        )

        self.frame_apariencia.grid(
            row=2,
            column=0,
            padx=20,
            pady=(5, 12),
            sticky="sew"
        )

        self.lbl_apariencia = ctk.CTkLabel(
            self.frame_apariencia,
            text="Apariencia",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        self.lbl_apariencia.pack(
            pady=(0, 5)
        )

        self.selector_apariencia = (
            ctk.CTkOptionMenu(
                self.frame_apariencia,
                values=[
                    "Sistema",
                    "Claro",
                    "Oscuro"
                ],
                command=self.cambiar_apariencia,
                fg_color=BOTON_PRINCIPAL,
                button_color=BOTON_PRINCIPAL,
                button_hover_color=(
                    BOTON_PRINCIPAL_HOVER
                ),
                text_color=TEXTO_BOTON,
                height=34
            )
        )

        self.selector_apariencia.set(
            "Sistema"
        )

        self.selector_apariencia.pack(
            fill="x"
        )

        # =====================================================
        # ENCABEZADO
        # =====================================================

        frame_encabezado = ctk.CTkFrame(
            self.frame_menu,
            fg_color="transparent"
        )

        frame_encabezado.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(20, 8)
        )

        self.lbl_titulo = ctk.CTkLabel(
            frame_encabezado,
            text="AUTÓMATAS",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=25,
                weight="bold"
            )
        )

        self.lbl_titulo.pack(
            pady=(5, 2)
        )

        self.lbl_subtitulo = ctk.CTkLabel(
            frame_encabezado,
            text="Simulador",
            text_color=TEXTO_SUAVE,
            font=ctk.CTkFont(
                size=14
            )
        )

        self.lbl_subtitulo.pack(
            pady=(0, 8)
        )

        # =====================================================
        # ÁREA DE BOTONES
        # =====================================================

        self.frame_botones_menu = ctk.CTkFrame(
        self.frame_menu,
        fg_color="transparent",
        corner_radius=0
        )

        self.frame_botones_menu.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(10, 3),
            pady=5
        )

        self.btn_inicio = (
            self.crear_boton_menu(
                "Inicio",
                self.mostrar_inicio
            )
        )

        self.btn_nuevo = (
            self.crear_boton_menu(
                "Nuevo autómata",
                self.mostrar_crear_automata
            )
        )

        self.btn_regex = (
            self.crear_boton_menu(
                "Expresiones regulares",
                self.mostrar_regex
            )
        )

        self.btn_logs = (
            self.crear_boton_menu(
                "Validación de logs",
                self.mostrar_validacion_logs
            )
        )

        self.btn_abrir = (
            self.crear_boton_menu(
                "Abrir autómata",
                self.abrir_automata
            )
        )

        self.btn_guardar = (
            self.crear_boton_menu(
                "Guardar autómata",
                self.guardar_automata_actual
            )
        )

        self.btn_simular = (
            self.crear_boton_menu(
                "Simular cadena",
                self.mostrar_simular_cadena
            )
        )

        self.btn_convertir = (
            self.crear_boton_menu(
                "AFN → AFD",
                self.mostrar_conversion
            )
        )

        self.btn_minimizar = (
            self.crear_boton_menu(
                "Minimizar AFD",
                self.mostrar_minimizacion
            )
        )

        self.btn_diagrama = (
            self.crear_boton_menu(
                "Ver diagrama",
                self.mostrar_diagrama
            )
        )

        # =====================================================
        # REINICIAR
        # =====================================================

        self.btn_reiniciar = ctk.CTkButton(
            self.frame_botones_menu,
            text="Reiniciar autómata",
            height=40,
            command=self.reiniciar_automata,
            fg_color=BOTON_PELIGRO,
            hover_color=BOTON_PELIGRO_HOVER,
            text_color=TEXTO_BOTON,
            corner_radius=8,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.btn_reiniciar.pack(
            padx=8,
            pady=(12, 4),
            fill="x"
        )

        # =====================================================
        # APARIENCIA
        # =====================================================

        self.frame_apariencia = ctk.CTkFrame(
            self.frame_menu,
            fg_color="transparent"
        )

        self.frame_apariencia.grid(
            row=2,
            column=0,
            padx=20,
            pady=(5, 15),
            sticky="ew"
        )

        self.lbl_apariencia = ctk.CTkLabel(
            self.frame_apariencia,
            text="Apariencia",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            )
        )

        self.lbl_apariencia.pack(
            pady=(0, 6)
        )

        self.selector_apariencia = (
            ctk.CTkOptionMenu(
                self.frame_apariencia,
                values=[
                    "Sistema",
                    "Claro",
                    "Oscuro"
                ],
                command=self.cambiar_apariencia,
                fg_color=BOTON_PRINCIPAL,
                button_color=BOTON_PRINCIPAL,
                button_hover_color=(
                    BOTON_PRINCIPAL_HOVER
                ),
                text_color=TEXTO_BOTON
            )
        )

        self.selector_apariencia.set(
            "Sistema"
        )

        self.selector_apariencia.pack(
            fill="x"
        )

    # =========================================================
    # ÁREA PRINCIPAL
    # =========================================================

    def crear_area_principal(self):

        self.frame_contenido = ctk.CTkFrame(
            self,
            corner_radius=12,
            fg_color=FONDO_PANEL,
            border_width=1,
            border_color=COLOR_BORDE
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
            anchor="w",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=13
            )
        )

        self.lbl_estado.grid(
            row=0,
            column=1,
            padx=25,
            pady=(0, 18),
            sticky="sew"
        )

    # =========================================================
    # ACTUALIZAR BARRA DE ESTADO
    # =========================================================

    def actualizar_barra_estado(
        self,
        texto,
        tipo="normal"
    ):

        colores = {
            "normal": TEXTO_NORMAL,
            "exito": COLOR_EXITO,
            "advertencia": COLOR_ADVERTENCIA,
            "error": COLOR_ERROR
        }

        color = colores.get(
            tipo,
            TEXTO_NORMAL
        )

        self.lbl_estado.configure(
            text=texto,
            text_color=color
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

        # =====================================================
        # ENCABEZADO
        # =====================================================

        titulo = ctk.CTkLabel(
            contenido,
            text="SIMULADOR DE AUTÓMATAS",
            text_color=TEXTO_TITULO,
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
            text_color=TEXTO_NORMAL,
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
                "Compatible con AFD, AFN, "
                "expresiones regulares y "
                "transiciones ε."
            ),
            text_color=TEXTO_SUAVE,
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
                contenido,
                fg_color=FONDO_APP,
                border_width=1,
                border_color=COLOR_BORDE,
                corner_radius=12
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
                text_color=TEXTO_TITULO,
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
                text_color=TEXTO_NORMAL,
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
                command=self.mostrar_crear_automata,
                fg_color=BOTON_PRINCIPAL,
                hover_color=BOTON_PRINCIPAL_HOVER,
                text_color=TEXTO_BOTON
            ).pack(
                pady=(15, 25)
            )

            return

        # =====================================================
        # AUTÓMATA CARGADO
        # =====================================================

        frame_actual = ctk.CTkFrame(
            contenido,
            fg_color=FONDO_APP,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
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
            text_color=TEXTO_TITULO,
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
            text_color=TEXTO_NORMAL,
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
            text=self.tipo_automata_actual,
            text_color=TEXTO_NORMAL
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
            text_color=TEXTO_NORMAL,
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
            text_color=TEXTO_NORMAL,
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
            text_color=TEXTO_NORMAL,
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
            ),
            text_color=TEXTO_NORMAL
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
            in self.automata_actual
            .transiciones.values()
        )

        ctk.CTkLabel(
            frame_actual,
            text="Transiciones:",
            text_color=TEXTO_NORMAL,
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
            ),
            text_color=TEXTO_NORMAL
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
            text_color=TEXTO_NORMAL,
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
            text=self.automata_actual.estado_inicial,
            text_color=TEXTO_NORMAL
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
                    self.automata_actual
                    .estados_finales
                )
            )
            + "}"
        )

        ctk.CTkLabel(
            frame_actual,
            text="Estados finales:",
            text_color=TEXTO_NORMAL,
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
            text_color=TEXTO_NORMAL,
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
        # ACCIONES RÁPIDAS
        # =====================================================

        frame_acciones = ctk.CTkFrame(
            contenido,
            fg_color=FONDO_APP,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
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
            text_color=TEXTO_TITULO,
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
            command=self.mostrar_simular_cadena,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
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
            command=self.mostrar_diagrama,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON
        ).grid(
            row=0,
            column=1,
            padx=8,
            pady=5
        )

        if (
            self.tipo_automata_actual
            == "AFN"
        ):

            ctk.CTkButton(
                frame_botones,
                text="Convertir a AFD",
                width=160,
                height=42,
                command=self.mostrar_conversion,
                fg_color=BOTON_PRINCIPAL,
                hover_color=BOTON_PRINCIPAL_HOVER,
                text_color=TEXTO_BOTON
            ).grid(
                row=0,
                column=2,
                padx=8,
                pady=5
            )

        elif (
            self.tipo_automata_actual
            == "AFD"
        ):

            ctk.CTkButton(
                frame_botones,
                text="Minimizar",
                width=160,
                height=42,
                command=self.mostrar_minimizacion,
                fg_color=BOTON_PRINCIPAL,
                hover_color=BOTON_PRINCIPAL_HOVER,
                text_color=TEXTO_BOTON
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
    # EXPRESIONES REGULARES
    # =========================================================

    def mostrar_regex(self):

        self.limpiar_contenido()

        regex = ExpresionesRegularesFrame(
            self.frame_contenido,
            self
        )

        regex.grid(
            row=0,
            column=0,
            sticky="nsew"
        )



    # =========================================================
    # VALIDACIÓN DE LOGS
    # =========================================================

    def mostrar_validacion_logs(self):

        self.limpiar_contenido()

        validacion = ValidacionLogsFrame(
            self.frame_contenido,
            self
        )

        validacion.grid(
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
    # CONVERSIÓN
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
    # ESTABLECER AUTÓMATA
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

        self.actualizar_barra_estado(
      (
        f"Estado: {tipo} cargado - "
        f"{automata.nombre} | "
        f"{cantidad} transiciones"
     ),
         "exito"
        )

        self.actualizar_estado_botones()

    # =========================================================
    # REINICIAR
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

        self.actualizar_barra_estado(
        "Estado: No hay un autómata cargado.",
         "normal"
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

        if (
            self.tipo_automata_actual
            == "AFN"
        ):

            self.btn_convertir.configure(
                state="normal"
            )

            self.btn_minimizar.configure(
                state="disabled"
            )

        elif (
            self.tipo_automata_actual
            == "AFD"
        ):

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

            registrar_warning(
                "ARCHIVO",
                (
                    "Se intentó guardar sin "
                    "un autómata cargado"
                )
            )

            self.actualizar_barra_estado(
         (
           f"Estado: "
           f"{self.tipo_automata_actual} - "
           f"{self.automata_actual.nombre} | "
           "Guardado correctamente"
        ),
        "exito"
    )

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

        if not ruta:

            return

        try:

            ruta_final = guardar_automata(
                self.automata_actual,
                self.tipo_automata_actual,
                ruta
            )

            registrar_info(
                "ARCHIVO",
                (
                    "Autómata guardado "
                    "correctamente: "
                    f"{ruta_final}"
                )
            )

            self.lbl_estado.configure(
                text=(
                    f"Estado: "
                    f"{self.tipo_automata_actual} - "
                    f"{self.automata_actual.nombre} | "
                    "Guardado correctamente"
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

            registrar_error(
                "ARCHIVO",
                (
                    "No fue posible guardar "
                    f"el autómata: {error}"
                )
            )

            self.actualizar_barra_estado(
            "Estado: Error al guardar el autómata.",
            "error"
        )

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

            registrar_info(
                "ARCHIVO",
                (
                    f"Autómata {tipo} cargado "
                    f"correctamente desde: {ruta}"
                )
            )

            self.establecer_automata(
                automata,
                tipo
            )

            self.mostrar_inicio()

            self.actualizar_barra_estado(
            "Estado: Error al abrir el autómata.",
            "error"
        )

            messagebox.showinfo(
                "Autómata cargado",
                (
                    f"El {tipo} fue cargado "
                    "correctamente.\n\n"
                    f"Nombre: {automata.nombre}"
                )
            )

        except Exception as error:

            registrar_error(
                "ARCHIVO",
                (
                    "No fue posible abrir "
                    f"el autómata: {error}"
                )
            )

            messagebox.showerror(
                "Error al abrir",
                (
                    "No fue posible abrir "
                    "el autómata.\n\n"
                    f"Detalle: {error}"
                )
            )