import os
import sys


def obtener_ruta_base():
    """
    Obtiene la carpeta base de la aplicación.

    Funciona tanto ejecutando con Python
    como después de empaquetar con PyInstaller.
    """

    if getattr(
        sys,
        "frozen",
        False
    ):
        return sys._MEIPASS

    return os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )


def configurar_graphviz():
    """
    Agrega Graphviz incluido con la aplicación
    al PATH durante la ejecución.
    """

    ruta_base = obtener_ruta_base()

    ruta_graphviz = os.path.join(
        ruta_base,
        "graphviz_bin"
    )

    if os.path.isdir(
        ruta_graphviz
    ):

        os.environ["PATH"] = (
            ruta_graphviz
            + os.pathsep
            + os.environ.get(
                "PATH",
                ""
            )
        )

    return ruta_graphviz