import customtkinter as ctk

from utilidades.rutas import (
    configurar_graphviz
)

from interfaz.ventana_principal import (
    VentanaPrincipal
)


def main():

    # Configurar Graphviz incluido
    configurar_graphviz()

    # Apariencia inicial
    ctk.set_appearance_mode(
        "system"
    )

    # Tema
    ctk.set_default_color_theme(
        "blue"
    )

    # Crear aplicación
    app = VentanaPrincipal()

    # Ejecutar
    app.mainloop()


if __name__ == "__main__":
    main()