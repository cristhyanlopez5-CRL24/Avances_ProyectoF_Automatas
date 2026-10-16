import customtkinter as ctk

from tkinter import messagebox

from modelos.afd import AFD
from modelos.afn import AFN

from utilidades.validaciones import (
    validar_datos_automata,
    validar_estados,
    validar_transicion
)

from utilidades.tema import (
    FONDO_APP,
    FONDO_ENTRADA,
    TEXTO_TITULO,
    TEXTO_NORMAL,
    TEXTO_SUAVE,
    BOTON_PRINCIPAL,
    BOTON_PRINCIPAL_HOVER,
    TEXTO_BOTON,
    COLOR_BORDE,
    TEXTO_DESHABILITADO,
    COLOR_EXITO
)


class CrearAutomataFrame(
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

        self.automata = None

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.crear_encabezado()

        self.crear_formulario()

        self.crear_seccion_transiciones()

    # =========================================================
    # ENCABEZADO
    # =========================================================

    def crear_encabezado(self):

        lbl_titulo = ctk.CTkLabel(
            self,
            text="CREAR AUTÓMATA",
            text_color=TEXTO_TITULO,
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
                "Defina la estructura básica "
                "de un AFD o AFN."
            ),
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=14
            )
        )

        lbl_descripcion.grid(
            row=1,
            column=0,
            pady=(0, 20)
        )

    # =========================================================
    # FORMULARIO PRINCIPAL
    # =========================================================

    def crear_formulario(self):

        self.frame_datos = ctk.CTkFrame(
            self,
            fg_color=FONDO_APP,
            border_width=1,
            border_color=COLOR_BORDE,
            corner_radius=12
        )

        self.frame_datos.grid(
            row=2,
            column=0,
            padx=30,
            pady=10,
            sticky="ew"
        )

        self.frame_datos.grid_columnconfigure(
            1,
            weight=1
        )

        # =====================================================
        # TÍTULO
        # =====================================================

        ctk.CTkLabel(
            self.frame_datos,
            text="Datos del autómata",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=(20, 12)
        )

        # =====================================================
        # NOMBRE
        # =====================================================

        lbl_nombre = ctk.CTkLabel(
            self.frame_datos,
            text="Nombre:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        )

        lbl_nombre.grid(
            row=1,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )

        self.entry_nombre = ctk.CTkEntry(
            self.frame_datos,
            placeholder_text=(
                "Ejemplo: Cadenas que terminan en 01"
            ),
            height=40,
            fg_color=FONDO_ENTRADA,
            text_color=TEXTO_NORMAL,
            border_color=COLOR_BORDE
        )

        self.entry_nombre.grid(
            row=1,
            column=1,
            padx=20,
            pady=10,
            sticky="ew"
        )

        # =====================================================
        # TIPO
        # =====================================================

        lbl_tipo = ctk.CTkLabel(
            self.frame_datos,
            text="Tipo:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        )

        lbl_tipo.grid(
            row=2,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )

        self.selector_tipo = (
    ctk.CTkSegmentedButton(
        self.frame_datos,
        values=[
            "AFD",
            "AFN"
        ],
        height=38,
        fg_color=FONDO_ENTRADA,

        selected_color=BOTON_PRINCIPAL,
        selected_hover_color=(
            BOTON_PRINCIPAL_HOVER
        ),

        unselected_color=(
            "#7A8194",
            "#31577D"
        ),

        unselected_hover_color=(
            "#646B7D",
            "#274866"
        ),

        text_color=(
            "#FFFFFF",
            "#FFFFFF"
        ),

        font=ctk.CTkFont(
            size=14,
            weight="bold"
        )
    )
)

        self.selector_tipo.set(
            "AFD"
        )

        self.selector_tipo.grid(
            row=2,
            column=1,
            padx=20,
            pady=10,
            sticky="w"
        )

        # =====================================================
        # ESTADOS
        # =====================================================

        lbl_estados = ctk.CTkLabel(
            self.frame_datos,
            text="Estados:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        )

        lbl_estados.grid(
            row=3,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )

        frame_estados = ctk.CTkFrame(
            self.frame_datos,
            fg_color="transparent"
        )

        frame_estados.grid(
            row=3,
            column=1,
            padx=20,
            pady=10,
            sticky="ew"
        )

        frame_estados.grid_columnconfigure(
            0,
            weight=1
        )

        self.entry_estados = ctk.CTkEntry(
            frame_estados,
            placeholder_text="q0,q1,q2",
            height=40,
            fg_color=FONDO_ENTRADA,
            text_color=TEXTO_NORMAL,
            border_color=COLOR_BORDE
        )

        self.entry_estados.grid(
            row=0,
            column=0,
            padx=(0, 10),
            sticky="ew"
        )

        self.btn_actualizar_estados = (
            ctk.CTkButton(
                frame_estados,
                text="Cargar estados",
                width=140,
                height=40,
                command=self.actualizar_lista_estados,
                fg_color=BOTON_PRINCIPAL,
                hover_color=BOTON_PRINCIPAL_HOVER,
                text_color=TEXTO_BOTON
            )
        )

        self.btn_actualizar_estados.grid(
            row=0,
            column=1
        )

        # =====================================================
        # ALFABETO
        # =====================================================

        lbl_alfabeto = ctk.CTkLabel(
            self.frame_datos,
            text="Alfabeto:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        )

        lbl_alfabeto.grid(
            row=4,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )

        self.entry_alfabeto = ctk.CTkEntry(
            self.frame_datos,
            placeholder_text="0,1",
            height=40,
            fg_color=FONDO_ENTRADA,
            text_color=TEXTO_NORMAL,
            border_color=COLOR_BORDE
        )

        self.entry_alfabeto.grid(
            row=4,
            column=1,
            padx=20,
            pady=10,
            sticky="ew"
        )

        # =====================================================
        # ESTADO INICIAL
        # =====================================================

        lbl_inicial = ctk.CTkLabel(
            self.frame_datos,
            text="Estado inicial:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        )

        lbl_inicial.grid(
            row=5,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )

        self.selector_inicial = (
            ctk.CTkOptionMenu(
                self.frame_datos,
                values=[
                    "Primero cargue los estados"
                ],
                height=40,
                fg_color=BOTON_PRINCIPAL,
                button_color=BOTON_PRINCIPAL,
                button_hover_color=(
                    BOTON_PRINCIPAL_HOVER
                ),
                text_color=TEXTO_BOTON
            )
        )

        self.selector_inicial.set(
            "Primero cargue los estados"
        )

        self.selector_inicial.grid(
            row=5,
            column=1,
            padx=20,
            pady=10,
            sticky="ew"
        )

        # =====================================================
        # ESTADOS FINALES
        # =====================================================

        lbl_finales = ctk.CTkLabel(
            self.frame_datos,
            text="Estados finales:",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        )

        lbl_finales.grid(
            row=6,
            column=0,
            padx=20,
            pady=10,
            sticky="w"
        )

        self.entry_finales = ctk.CTkEntry(
            self.frame_datos,
            placeholder_text=(
                "q2 o q2,q3"
            ),
            height=40,
            fg_color=FONDO_ENTRADA,
            text_color=TEXTO_NORMAL,
            border_color=COLOR_BORDE
        )

        self.entry_finales.grid(
            row=6,
            column=1,
            padx=20,
            pady=10,
            sticky="ew"
        )

        # =====================================================
        # AYUDA
        # =====================================================

        lbl_ayuda = ctk.CTkLabel(
            self.frame_datos,
            text=(
                "Separe los estados y símbolos "
                "utilizando comas."
            ),
            text_color=TEXTO_SUAVE,
            font=ctk.CTkFont(
                size=12
            )
        )

        lbl_ayuda.grid(
            row=7,
            column=1,
            padx=20,
            pady=(0, 10),
            sticky="w"
        )

        # =====================================================
        # CREAR
        # =====================================================

        self.btn_crear = ctk.CTkButton(
            self.frame_datos,
            text="Crear autómata",
            width=220,
            height=44,
            command=self.crear_automata,
            fg_color=BOTON_PRINCIPAL,
            hover_color=BOTON_PRINCIPAL_HOVER,
            text_color=TEXTO_BOTON,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.btn_crear.grid(
            row=8,
            column=0,
            columnspan=2,
            padx=20,
            pady=(15, 12)
        )

        # =====================================================
        # RESULTADO
        # =====================================================

        self.lbl_resultado = ctk.CTkLabel(
            self.frame_datos,
            text="",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        self.lbl_resultado.grid(
            row=9,
            column=0,
            columnspan=2,
            padx=20,
            pady=(0, 18)
        )

    # =========================================================
    # SECCIÓN DE TRANSICIONES
    # =========================================================

    def crear_seccion_transiciones(self):

        self.frame_transiciones = (
            ctk.CTkFrame(
                self,
                fg_color=FONDO_APP,
                border_width=1,
                border_color=COLOR_BORDE,
                corner_radius=12
            )
        )

        self.frame_transiciones.grid(
            row=3,
            column=0,
            padx=30,
            pady=(15, 30),
            sticky="ew"
        )

        self.frame_transiciones.grid_columnconfigure(
            0,
            weight=1
        )

        # =====================================================
        # TÍTULO
        # =====================================================

        lbl_titulo = ctk.CTkLabel(
            self.frame_transiciones,
            text="Transiciones",
            text_color=TEXTO_TITULO,
            font=ctk.CTkFont(
                size=21,
                weight="bold"
            )
        )

        lbl_titulo.grid(
            row=0,
            column=0,
            pady=(18, 5)
        )

        self.lbl_info_transiciones = (
            ctk.CTkLabel(
                self.frame_transiciones,
                text=(
                    "Primero debe crear un autómata."
                ),
                text_color=TEXTO_SUAVE,
                font=ctk.CTkFont(
                    size=13
                )
            )
        )

        self.lbl_info_transiciones.grid(
            row=1,
            column=0,
            pady=(0, 15)
        )

        # =====================================================
        # CONTENEDOR DE SELECTORES
        # =====================================================

        self.frame_selectores = (
            ctk.CTkFrame(
                self.frame_transiciones,
                fg_color="transparent"
            )
        )

        self.frame_selectores.grid(
            row=2,
            column=0,
            padx=15,
            pady=5
        )

        # =====================================================
        # ORIGEN
        # =====================================================

        ctk.CTkLabel(
            self.frame_selectores,
            text="Origen",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=0,
            column=0,
            padx=8,
            pady=5
        )

        self.selector_origen = (
            ctk.CTkOptionMenu(
                self.frame_selectores,
                values=["-"],
                width=160,
                height=38,
                fg_color=BOTON_PRINCIPAL,
                button_color=BOTON_PRINCIPAL,
                button_hover_color=(
                    BOTON_PRINCIPAL_HOVER
                ),
                text_color=TEXTO_BOTON
            )
        )

        self.selector_origen.grid(
            row=1,
            column=0,
            padx=8,
            pady=5
        )

        # =====================================================
        # SÍMBOLO
        # =====================================================

        ctk.CTkLabel(
            self.frame_selectores,
            text="Símbolo",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=0,
            column=1,
            padx=8,
            pady=5
        )

        self.selector_simbolo = (
            ctk.CTkOptionMenu(
                self.frame_selectores,
                values=["-"],
                width=130,
                height=38,
                fg_color=BOTON_PRINCIPAL,
                button_color=BOTON_PRINCIPAL,
                button_hover_color=(
                    BOTON_PRINCIPAL_HOVER
                ),
                text_color=TEXTO_BOTON
            )
        )

        self.selector_simbolo.grid(
            row=1,
            column=1,
            padx=8,
            pady=5
        )

        # =====================================================
        # DESTINO
        # =====================================================

        ctk.CTkLabel(
            self.frame_selectores,
            text="Destino",
            text_color=TEXTO_NORMAL,
            font=ctk.CTkFont(
                weight="bold"
            )
        ).grid(
            row=0,
            column=2,
            padx=8,
            pady=5
        )

        self.selector_destino = (
            ctk.CTkOptionMenu(
                self.frame_selectores,
                values=["-"],
                width=160,
                height=38,
                fg_color=BOTON_PRINCIPAL,
                button_color=BOTON_PRINCIPAL,
                button_hover_color=(
                    BOTON_PRINCIPAL_HOVER
                ),
                text_color=TEXTO_BOTON
            )
        )

        self.selector_destino.grid(
            row=1,
            column=2,
            padx=8,
            pady=5
        )

        # =====================================================
        # AGREGAR TRANSICIÓN
        # =====================================================

        self.btn_agregar_transicion = (
            ctk.CTkButton(
                self.frame_selectores,
                text="Agregar transición",
                width=170,
                height=38,
                command=self.agregar_transicion,
                state="disabled",
                fg_color=BOTON_PRINCIPAL,
                hover_color=BOTON_PRINCIPAL_HOVER,
                text_color=TEXTO_BOTON,
                text_color_disabled=TEXTO_DESHABILITADO
            )
        )

        self.btn_agregar_transicion.grid(
            row=1,
            column=3,
            padx=15,
            pady=5
        )

        # =====================================================
        # LISTA DE TRANSICIONES
        # =====================================================

        self.txt_transiciones = (
            ctk.CTkTextbox(
                self.frame_transiciones,
                height=180,
                fg_color=FONDO_ENTRADA,
                text_color=TEXTO_NORMAL,
                border_width=1,
                border_color=COLOR_BORDE,
                font=(
                    "Consolas",
                    14
                )
            )
        )

        self.txt_transiciones.grid(
            row=3,
            column=0,
            padx=25,
            pady=(15, 20),
            sticky="ew"
        )

        self.txt_transiciones.configure(
            state="disabled"
        )

    # =========================================================
    # CARGAR ESTADOS
    # =========================================================

    def actualizar_lista_estados(self):

        try:

            estados = validar_estados(
                self.entry_estados.get()
            )

            estados_ordenados = sorted(
                estados
            )

            self.selector_inicial.configure(
                values=estados_ordenados
            )

            self.selector_inicial.set(
                estados_ordenados[0]
            )

            messagebox.showinfo(
                "Estados cargados",
                (
                    "Los estados fueron cargados "
                    "correctamente."
                )
            )

        except ValueError as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # =========================================================
    # CREAR AUTÓMATA
    # =========================================================

    def crear_automata(self):

        try:

            datos = validar_datos_automata(
                nombre=self.entry_nombre.get(),
                tipo=self.selector_tipo.get(),
                texto_estados=self.entry_estados.get(),
                texto_alfabeto=self.entry_alfabeto.get(),
                estado_inicial=self.selector_inicial.get(),
                texto_estados_finales=(
                    self.entry_finales.get()
                )
            )

            if datos["tipo"] == "AFD":

                automata = AFD(
                    nombre=datos["nombre"],
                    estados=datos["estados"],
                    alfabeto=datos["alfabeto"],
                    estado_inicial=datos[
                        "estado_inicial"
                    ],
                    estados_finales=datos[
                        "estados_finales"
                    ]
                )

            else:

                automata = AFN(
                    nombre=datos["nombre"],
                    estados=datos["estados"],
                    alfabeto=datos["alfabeto"],
                    estado_inicial=datos[
                        "estado_inicial"
                    ],
                    estados_finales=datos[
                        "estados_finales"
                    ]
                )

            self.automata = automata

            self.ventana_principal.establecer_automata(
                automata,
                datos["tipo"]
            )

            self.preparar_transiciones()

            self.lbl_resultado.configure(
                text=(
                    f"{datos['tipo']} creado "
                    f"correctamente: "
                    f"{datos['nombre']}"
                ),
                text_color=COLOR_EXITO
            )

            messagebox.showinfo(
                "Autómata creado",
                (
                    f"El {datos['tipo']} "
                    "fue creado correctamente."
                )
            )

        except ValueError as error:

            self.ventana_principal.actualizar_barra_estado(
                (
                    "Estado: Datos incorrectos "
                    "para crear el autómata."
                ),
                "advertencia"
            )

            messagebox.showerror(
                "Datos incorrectos",
                str(error)
            )

    # =========================================================
    # PREPARAR TRANSICIONES
    # =========================================================

    def preparar_transiciones(self):

        if self.automata is None:

            return

        estados = sorted(
            self.automata.estados
        )

        simbolos = sorted(
            self.automata.alfabeto
        )

        tipo = (
            self.ventana_principal
            .tipo_automata_actual
        )

        if tipo == "AFN":

            simbolos.append(
                "ε"
            )

        self.selector_origen.configure(
            values=estados
        )

        self.selector_destino.configure(
            values=estados
        )

        self.selector_simbolo.configure(
            values=simbolos
        )

        self.selector_origen.set(
            estados[0]
        )

        self.selector_destino.set(
            estados[0]
        )

        self.selector_simbolo.set(
            simbolos[0]
        )

        self.btn_agregar_transicion.configure(
            state="normal"
        )

        self.lbl_info_transiciones.configure(
            text=(
                f"Agregando transiciones al "
                f"{tipo}: "
                f"{self.automata.nombre}"
            ),
            text_color=TEXTO_NORMAL
        )

        self.actualizar_lista_transiciones()

    # =========================================================
    # AGREGAR TRANSICIÓN
    # =========================================================

    def agregar_transicion(self):

        if self.automata is None:

            self.ventana_principal.actualizar_barra_estado(
                (
                    "Estado: Debe crear un autómata "
                    "antes de agregar transiciones."
                ),
                "advertencia"
            )

            messagebox.showwarning(
                "Sin autómata",
                (
                    "Debe crear un autómata "
                    "antes de agregar transiciones."
                )
            )

            return

        try:

            tipo = (
                self.ventana_principal
                .tipo_automata_actual
            )

            datos = validar_transicion(
                origen=(
                    self.selector_origen.get()
                ),
                simbolo=(
                    self.selector_simbolo.get()
                ),
                destino=(
                    self.selector_destino.get()
                ),
                estados=self.automata.estados,
                alfabeto=self.automata.alfabeto,
                tipo=tipo
            )

            self.automata.agregar_transicion(
                datos["origen"],
                datos["simbolo"],
                datos["destino"]
            )

            self.actualizar_lista_transiciones()

            cantidad = sum(
                len(destinos)
                for destinos
                in self.automata
                .transiciones.values()
            )

            self.ventana_principal.actualizar_barra_estado(
                (
                    f"Estado: {tipo} cargado - "
                    f"{self.automata.nombre} | "
                    f"{cantidad} transiciones"
                ),
                "exito"
            )

        except ValueError as error:

            self.ventana_principal.actualizar_barra_estado(
                "Estado: Transición inválida.",
                "advertencia"
            )

            messagebox.showerror(
                "Transición inválida",
                str(error)
            )

    # =========================================================
    # ACTUALIZAR LISTA DE TRANSICIONES
    # =========================================================

    def actualizar_lista_transiciones(self):

        self.txt_transiciones.configure(
            state="normal"
        )

        self.txt_transiciones.delete(
            "1.0",
            "end"
        )

        if (
            self.automata is None
            or not self.automata.transiciones
        ):

            self.txt_transiciones.insert(
                "end",
                (
                    "Todavía no se han agregado "
                    "transiciones."
                )
            )

        else:

            transiciones = (
                self.automata
                .mostrar_transiciones()
            )

            for numero, transicion in enumerate(
                transiciones,
                start=1
            ):

                self.txt_transiciones.insert(
                    "end",
                    f"{numero}. {transicion}\n"
                )

        self.txt_transiciones.configure(
            state="disabled"
        )