import customtkinter as ctk

from utilidades.rutas import (
    configurar_graphviz
)

from utilidades.registro_logs import (
    registrar_info,
    registrar_error,
    registrar_critical,
    cerrar_logging
)

from interfaz.ventana_principal import (
    VentanaPrincipal
)


def main():

    app = None

    try:

        # =====================================================
        # INICIO DEL SISTEMA DE LOGS
        # =====================================================

        registrar_info(
            "SISTEMA",
            "Aplicación iniciada correctamente"
        )

        # =====================================================
        # CONFIGURAR GRAPHVIZ
        # =====================================================

        try:

            configurar_graphviz()

            registrar_info(
                "GRAPHVIZ",
                "Graphviz configurado correctamente"
            )

        except Exception as error:

            registrar_error(
                "GRAPHVIZ",
                (
                    "No fue posible configurar Graphviz: "
                    f"{error}"
                )
            )

            raise

        # =====================================================
        # APARIENCIA
        # =====================================================

        ctk.set_appearance_mode(
            "system"
        )

        ctk.set_default_color_theme(
            "blue"
        )

        # =====================================================
        # CREAR APLICACIÓN
        # =====================================================

        app = VentanaPrincipal()

        registrar_info(
            "INTERFAZ",
            "Ventana principal creada correctamente"
        )

        # =====================================================
        # CIERRE CONTROLADO
        # =====================================================

        def cerrar_aplicacion():

            registrar_info(
                "SISTEMA",
                "Aplicación cerrada por el usuario"
            )

            cerrar_logging()

            app.destroy()

        app.protocol(
            "WM_DELETE_WINDOW",
            cerrar_aplicacion
        )

        # =====================================================
        # EJECUTAR
        # =====================================================

        app.mainloop()

    except Exception as error:

        try:

            registrar_critical(
                "SISTEMA",
                (
                    "Error crítico durante la ejecución "
                    f"de la aplicación: {error}"
                )
            )

        finally:

            cerrar_logging()

        raise


if __name__ == "__main__":
    main()