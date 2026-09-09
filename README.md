# Simulador de Autómatas

**Avances_ProyectoF_Automatas** contiene una aplicación de escritorio para crear, simular, convertir y minimizar autómatas finitos. Está desarrollada en **Python**, utiliza **CustomTkinter** para las ventanas y **Graphviz** para generar los diagramas.

Este README explica la función de cada carpeta, cómo se relacionan sus archivos y qué se necesita para ejecutar la aplicación. El punto de entrada del código fuente es [main.py](main.py), ubicado en la raíz del repositorio.

## Funciones de la aplicación

- Crear autómatas finitos deterministas (**AFD**) y no deterministas (**AFN**).
- Agregar estados, alfabeto, estado inicial, estados finales y transiciones mediante el formulario de creación.
- Trabajar con transiciones **ε** en los AFN.
- Evaluar cadenas y mostrar si son aceptadas o rechazadas, junto con el recorrido realizado.
- Convertir un AFN en un AFD mediante construcción de subconjuntos y ε-cerradura.
- Minimizar un AFD mediante refinamiento de particiones.
- Generar y mostrar el diagrama del autómata.
- Guardar y abrir autómatas en archivos **JSON**.
- Seleccionar apariencia clara, oscura o según el sistema.

## 1. ¿Para qué sirve cada carpeta?

| Carpeta | ¿Qué contiene? | ¿Cómo participa en la aplicación? |
| --- | --- | --- |
| [modelos/](modelos/) | Las clases `Automata`, `AFD` y `AFN`. | Mantiene los datos del autómata y las reglas que deben cumplir sus estados, símbolos y transiciones. |
| [interfaz/](interfaz/) | Las pantallas y los controles construidos con CustomTkinter. | Recibe los datos del usuario, llama a los modelos y algoritmos, y muestra los resultados. |
| [algoritmos/](algoritmos/) | Simulación detallada, operaciones con ε, conversión y minimización. | Realiza los procedimientos de teoría de autómatas que se solicitan desde las pantallas. |
| [utilidades/](utilidades/) | Validaciones, lectura y escritura de JSON, generación de diagramas y manejo de rutas. | Proporciona funciones de apoyo que utilizan varias partes del programa. |
| [recursos/](recursos/) | La subcarpeta `diagramas/` con imágenes PNG. | Al ejecutar desde la raíz, aquí se genera la imagen que aparece en **Ver diagrama**. |
| [graphviz_bin/](graphviz_bin/) | `dot.exe`, otros ejecutables y las bibliotecas DLL de Graphviz para Windows. | Es el motor que convierte la descripción del autómata en una imagen. `main.py` configura su ubicación mediante `utilidades/rutas.py`. |
| [graphviz_tcl_backup/](graphviz_tcl_backup/) | Bibliotecas Tcl relacionadas con Graphviz, como `tcldot.dll` y `tcl86t.dll`. | Es una carpeta de respaldo. El código de arranque y la configuración de empaquetado no la utilizan directamente. |
| [tests/](tests/) | Pruebas automáticas escritas para pytest. | Comprueba el comportamiento de los modelos, algoritmos, validaciones, archivos JSON y diagramas durante el desarrollo. |
| [venv/](venv/) | Un entorno virtual de Python creado en Windows. | Contiene el intérprete y paquetes del entorno de desarrollo. En otro equipo se debe crear un entorno propio, como se explica más adelante. |
| [build/](build/) | Archivos intermedios generados por PyInstaller. | Se usa durante la construcción del ejecutable; no es la carpeta de distribución para el usuario. |
| [dist/](dist/) | La aplicación empaquetada dentro de `SimuladorAutomatas/`. | Permite ejecutar el programa en Windows con las dependencias incluidas. Debe conservarse completa. |
| [instalador/](instalador/) | `SimuladorAutomatas_Setup.exe`. | Contiene el instalador que copia la aplicación al equipo y permite crear accesos directos. |
| [Proyecto Final/](Proyecto%20Final/) | El archivo `PoyectoF.py`, actualmente vacío. | No contiene el punto de entrada de la aplicación ni interviene en su ejecución actual. |

### Subcarpetas y archivos generados

| Ubicación | Función |
| --- | --- |
| `recursos/diagramas/` | Contiene imágenes como `afd_termina_01.png`, `afn_epsilon.png` y `automata_actual.png`. Esta última se vuelve a generar al actualizar el diagrama. |
| `dist/SimuladorAutomatas/_internal/` | Contiene Python y las dependencias empaquetadas. Incluye recursos de CustomTkinter, Pillow (`PIL/`), Tcl/Tk (`_tcl_data/`, `_tk_data/`, `tcl8/`) y Graphviz (`graphviz_bin/`). Estas carpetas permiten que funcione el `.exe`. |
| `dist/SimuladorAutomatas/recursos/diagramas/` | Almacena los diagramas cuando la aplicación empaquetada se ejecuta desde su propia carpeta. |
| `build/SimuladorAutomatas/` | Guarda análisis de dependencias, archivos `.toc`, paquetes `.pyz` y `.pkg`, advertencias y otros resultados del empaquetado. Su subcarpeta `localpycs/` contiene módulos compilados para ese proceso. |
| `venv/Lib/site-packages/` | Almacena los paquetes instalados en el entorno virtual. Sus subcarpetas pertenecen a esas dependencias. |
| `venv/Scripts/` | Contiene `python.exe`, `pip.exe`, pytest, PyInstaller y los scripts de activación del entorno de Windows. |
| `__pycache__/` dentro de las carpetas Python | Guarda archivos `.pyc` generados automáticamente por Python al importar módulos. No se editan manualmente y Python puede volver a crearlos. |

Los archivos `__init__.py` de las carpetas de código permiten organizarlas como paquetes de Python. Aunque estén vacíos, ayudan a realizar importaciones como `from modelos.afd import AFD`.

## 2. Archivos principales de cada módulo

### `modelos/`: representación del autómata

| Archivo | Responsabilidad |
| --- | --- |
| [automata.py](modelos/automata.py) | Clase base con nombre, estados, alfabeto, estado inicial, estados finales y transiciones. Valida los datos comunes y define las operaciones que implementan AFD y AFN. |
| [afd.py](modelos/afd.py) | Impide transiciones ε y destinos duplicados para una misma combinación de estado y símbolo. Permite simular cadenas y comprobar si el AFD tiene todas sus transiciones. |
| [afn.py](modelos/afn.py) | Permite varios destinos para un mismo estado y símbolo, además de transiciones ε. Simula cadenas manteniendo los conjuntos de estados posibles. |

Las transiciones se almacenan con la estructura `(estado_origen, símbolo): conjunto_de_destinos`. En un AFD, cada transición registrada tiene un solo destino; en un AFN puede tener varios.

### `interfaz/`: ventanas y navegación

| Archivo | Responsabilidad |
| --- | --- |
| [ventana_principal.py](interfaz/ventana_principal.py) | Crea la ventana principal, el menú lateral y la barra de estado. Conserva el autómata actual, coordina las pantallas, permite abrir y guardar archivos y cambia la apariencia. |
| [crear_automata.py](interfaz/crear_automata.py) | Recoge los datos del nuevo AFD o AFN, valida el formulario y permite agregar sus transiciones. |
| [simular_cadena.py](interfaz/simular_cadena.py) | Recibe una cadena, ejecuta la simulación y presenta la aceptación o rechazo con el detalle del recorrido. |
| [conversion_afn_afd.py](interfaz/conversion_afn_afd.py) | Ejecuta la conversión, muestra los subconjuntos y la tabla resultante, y permite usar el AFD generado como autómata actual. |
| [minimizar_afd.py](interfaz/minimizar_afd.py) | Presenta el resultado de la minimización y permite usar el AFD mínimo como autómata actual. |
| [ver_diagrama.py](interfaz/ver_diagrama.py) | Solicita el PNG del autómata, lo carga con Pillow y lo muestra en la pantalla. Incluye **Actualizar diagrama**. |

### `algoritmos/`: procesamiento

| Archivo | Responsabilidad |
| --- | --- |
| [epsilon.py](algoritmos/epsilon.py) | Calcula la ε-cerradura y los movimientos entre conjuntos de estados. La ε-cerradura reúne los estados alcanzables sin consumir símbolos. |
| [simulador.py](algoritmos/simulador.py) | Simula AFD y AFN con información de cada paso y prepara el texto de los resultados para la interfaz. |
| [conversion.py](algoritmos/conversion.py) | Construye un AFD equivalente a partir de los subconjuntos alcanzables de un AFN. Considera ε y representa el subconjunto vacío como `∅` cuando aparece. |
| [minimizacion.py](algoritmos/minimizacion.py) | Elimina estados inalcanzables, agrega un estado trampa si faltan transiciones y agrupa estados equivalentes mediante refinamiento de particiones. |

### `utilidades/`: funciones de apoyo

| Archivo | Responsabilidad |
| --- | --- |
| [validaciones.py](utilidades/validaciones.py) | Limpia y verifica lo ingresado: nombre, estados, alfabeto, estado inicial, estados finales, transiciones y cadenas. |
| [persistencia.py](utilidades/persistencia.py) | Convierte un autómata a JSON y reconstruye un objeto AFD o AFN al abrir un archivo. |
| [graficador.py](utilidades/graficador.py) | Construye la descripción DOT del grafo y genera imágenes con Graphviz. Distingue el estado inicial y los estados finales y agrupa símbolos entre un mismo origen y destino. |
| [rutas.py](utilidades/rutas.py) | Localiza los recursos al ejecutar con Python o PyInstaller y añade `graphviz_bin/` al `PATH` del proceso. |

El generador admite **PNG, SVG y PDF** desde código. La pantalla **Ver diagrama** utiliza **PNG**.

### `tests/`: comprobación del funcionamiento

| Archivo | Qué comprueba |
| --- | --- |
| `test_afd.py` | Cadenas aceptadas y rechazadas, transiciones completas y simulación detallada de AFD. |
| `test_afn.py` | ε-cerradura, movimientos, recorridos y simulación de AFN. |
| `test_conversion.py` | Subconjuntos, transiciones y coincidencia de resultados entre un AFN y su AFD convertido. |
| `test_minimizacion.py` | Estados inalcanzables, equivalentes y coincidencia de resultados tras minimizar. |
| `test_graficador.py` | Descripción DOT, representación de estados y generación de un archivo PNG. |
| `test_persistencia.py` | Guardado, carga y conservación del comportamiento mediante JSON. |
| `test_validaciones.py` | Datos incorrectos, estados repetidos, símbolos y uso de ε. |

## 3. ¿Cómo trabajan juntas estas carpetas?

1. **Inicio:** `main.py` llama a `configurar_graphviz()` de `utilidades/rutas.py`, configura CustomTkinter y crea `VentanaPrincipal`. Después inicia el ciclo de eventos con `mainloop()` para atender los botones y las ventanas.
2. **Creación:** `interfaz/crear_automata.py` envía el formulario a `utilidades/validaciones.py`. Si los datos son válidos, crea un objeto de `modelos/afd.py` o `modelos/afn.py`. La ventana principal lo conserva como `automata_actual`.
3. **Simulación:** la pantalla de simulación toma ese objeto y la cadena ingresada. `algoritmos/simulador.py` calcula el recorrido; para un AFN también utiliza las operaciones de `epsilon.py`. La interfaz presenta el resultado.
4. **Conversión y minimización:** las pantallas llaman a `algoritmos/conversion.py` o `algoritmos/minimizacion.py`. Cada operación genera un nuevo AFD. Los botones **Usar AFD convertido** y **Usar AFD mínimo** lo convierten en el autómata actual.
5. **Diagrama:** `interfaz/ver_diagrama.py` llama a `utilidades/graficador.py`. El paquete Python `graphviz` prepara el grafo y el motor `dot.exe` de `graphviz_bin/` genera el PNG. Pillow carga la imagen para mostrarla.
6. **Guardado y apertura:** la ventana principal utiliza `utilidades/persistencia.py` para guardar el autómata en un JSON o reconstruirlo desde un archivo seleccionado por el usuario.

El programa trabaja con **un autómata actual a la vez**. Los botones se habilitan según su tipo: **AFN → AFD** corresponde a un AFN y **Minimizar AFD** corresponde a un AFD.

## 4. Otros archivos de la raíz

| Archivo | Función |
| --- | --- |
| [main.py](main.py) | Inicia la aplicación. Es el archivo que se debe ejecutar para abrir el simulador desde Python. |
| [requirements.txt](requirements.txt) | Registra las versiones de los paquetes del entorno, incluyendo CustomTkinter, Graphviz, Pillow, pytest y PyInstaller. Reúne dependencias de ejecución y herramientas de desarrollo. |
| [SimuladorAutomatas.spec](SimuladorAutomatas.spec) | Indica a PyInstaller cómo empaquetar `main.py`, incluir `graphviz_bin/` y producir `dist/SimuladorAutomatas/` sin ventana de consola. |
| [instalador.iss](instalador.iss) | Script de Inno Setup que copia el contenido completo de `dist/SimuladorAutomatas/` y genera el instalador en `instalador/`. |
| [Ejercicio1.py](Ejercicio1.py) | Ejercicio independiente de expresiones regulares para comprobar formatos de DPI y NIT. No inicia el simulador. |
| [Ejercicios de automatas pyhton.zip](Ejercicios%20de%20automatas%20pyhton.zip) | Archivo comprimido adicional del repositorio. El arranque de la aplicación no lo utiliza. |

## 5. Cómo ejecutar la aplicación

### Opción A: instalarla en Windows

1. Abre [instalador/SimuladorAutomatas_Setup.exe](instalador/SimuladorAutomatas_Setup.exe) y descarga el archivo desde GitHub.
2. Ejecuta el instalador y sigue sus pasos.
3. Si lo deseas, marca la opción para crear el acceso directo en el escritorio.
4. Abre **Simulador de Autómatas** desde el acceso directo o el menú Inicio.

El script configura la instalación en `%LOCALAPPDATA%\Programs\SimuladorAutomatas`, sin requerir permisos de administrador. La distribución incluye Python y las dependencias necesarias; el usuario final no necesita crear un entorno virtual.

### Opción B: usar la aplicación empaquetada

1. Descarga el repositorio mediante **Code → Download ZIP** y extráelo.
2. Entra en `dist/SimuladorAutomatas/`.
3. Ejecuta `SimuladorAutomatas.exe`.

**Conserva toda la carpeta `SimuladorAutomatas/`, incluyendo `_internal/`.** Copiar únicamente el `.exe` deja fuera las dependencias que necesita.

### Opción C: ejecutar o modificar el código fuente

Estas instrucciones están orientadas a **Windows con Python 3.12**. El entorno incluido en el repositorio registra Python **3.12.9**. También se necesita el componente **Tcl/Tk** de Python para las ventanas.

**1. Obtén el repositorio.** Puedes descargarlo con **Code → Download ZIP** o clonarlo si tienes Git:

```powershell
git clone https://github.com/cristhyanlopez5-CRL24/Avances_ProyectoF_Automatas.git
cd Avances_ProyectoF_Automatas
```

Si descargaste el ZIP, abre una terminal dentro de la carpeta extraída que contiene `main.py` y `requirements.txt`.

**2. Crea tu propio entorno virtual.** La carpeta `venv/` publicada contiene rutas del equipo donde se creó y no se debe asumir que funcionará en otro equipo. Los siguientes comandos crean un entorno nuevo llamado `.venv`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Si el comando `py` no está disponible, puedes usar `python -m venv .venv`, comprobando antes que `python --version` corresponda a la versión que vas a utilizar. Los comandos llaman directamente al intérprete del entorno, por lo que no es necesario activar `.venv`.

**3. Abre el simulador desde la raíz:**

```powershell
.\.venv\Scripts\python.exe main.py
```

Mantén `graphviz_bin/` junto a `main.py`. La aplicación configura su ruta automáticamente. El paquete Python `graphviz` y el motor `dot.exe` son componentes distintos: ambos participan en la generación de diagramas.

Los ejecutables incluidos son para **Windows**. En otros sistemas se necesita una instalación de Graphviz compatible y Tcl/Tk disponible para Python; los `.exe` del repositorio no sirven para esos sistemas.

## 6. Ejemplo de uso: cadenas que terminan en 01

1. Abre **Nuevo autómata**.
2. Escribe el nombre `Termina en 01` y selecciona el tipo **AFD**.
3. Ingresa los estados `q0,q1,q2` y presiona **Cargar estados**.
4. Ingresa el alfabeto `0,1`, selecciona `q0` como estado inicial y escribe `q2` en estados finales.
5. Presiona **Crear autómata**.
6. En la sección **Transiciones**, selecciona origen, símbolo y destino, y presiona **Agregar transición** para cada combinación de esta tabla:

| Estado de origen | Destino con `0` | Destino con `1` |
| --- | --- | --- |
| `q0` | `q1` | `q0` |
| `q1` | `q1` | `q2` |
| `q2` | `q1` | `q0` |

7. Abre **Simular cadena**, escribe una cadena y presiona **Simular**.

| Cadena | Resultado esperado |
| --- | --- |
| `01` | Aceptada |
| `101` | Aceptada |
| `0001` | Aceptada |
| `10` | Rechazada |
| `111` | Rechazada |
| Campo vacío, que representa `ε` | Rechazada en este autómata |

Puedes consultar **Ver diagrama** y guardar el trabajo con **Guardar autómata**. El archivo JSON se guarda en la ubicación que elijas y se recupera con **Abrir autómata**.

Para trabajar con un **AFN**, selecciona ese tipo al crearlo. La opción `ε` aparece automáticamente entre los símbolos de transición: **no la agregues al alfabeto**. Para evaluar la cadena vacía, deja vacío el campo de simulación. Los símbolos del alfabeto introducidos mediante el formulario deben ser de un solo carácter.

## 7. Ejecutar las pruebas

Después de instalar `requirements.txt`, ejecuta lo siguiente desde la raíz. El comando configura primero el Graphviz incluido, porque las pruebas no arrancan a través de `main.py`:

```powershell
.\.venv\Scripts\python.exe -c "from utilidades.rutas import configurar_graphviz; configurar_graphviz(); import pytest; raise SystemExit(pytest.main(['-q', 'tests']))"
```

Si Graphviz ya está disponible en el `PATH` de la terminal, también puedes utilizar:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

La prueba que genera un PNG necesita tanto el paquete Python `graphviz` como el motor de Graphviz disponible.

## 8. Generar el ejecutable y el instalador

Estos pasos se realizan en **Windows**, después de instalar las dependencias y comprobar el funcionamiento del código.

**Ejecutable con PyInstaller:**

```powershell
.\.venv\Scripts\python.exe -m PyInstaller SimuladorAutomatas.spec
```

PyInstaller utiliza `build/` para los archivos intermedios y genera la distribución en `dist/SimuladorAutomatas/`.

**Instalador con Inno Setup:**

1. Abre `instalador.iss` en Inno Setup.
2. Comprueba que ya exista `dist/SimuladorAutomatas/` con la distribución completa.
3. Selecciona **Compile** o presiona **F9**.
4. El resultado se genera en `instalador/SimuladorAutomatas_Setup.exe`.

Los cambios en los archivos `.py` se reflejan al ejecutar `main.py`. Para distribuir esos cambios mediante el `.exe` o el instalador, debes volver a generar ambos en ese orden.

## 9. Solución de problemas comunes

| Situación | Qué revisar |
| --- | --- |
| Aparece `ModuleNotFoundError` para `customtkinter`, `PIL` o `graphviz`. | Instala `requirements.txt` con el Python de `.venv` y ejecuta la aplicación con ese mismo intérprete. El paquete que proporciona `PIL` se llama `pillow`. |
| No se encuentra `dot` o no se genera el diagrama. | Comprueba que `graphviz_bin/dot.exe` y sus DLL estén presentes. Inicia la aplicación con `main.py` para que se configure la ruta. |
| El `.exe` falla después de copiarlo a otra ubicación. | Copia la carpeta completa `dist/SimuladorAutomatas/`, incluyendo `_internal/`, o utiliza el instalador. |
| Los botones de simulación o diagrama están deshabilitados. | Crea o abre un autómata. Conversión y minimización también dependen del tipo cargado. |
| Una cadena válida se rechaza. | Revisa el estado inicial, los estados finales y las transiciones. En un AFD, si falta la transición necesaria para consumir un símbolo, la cadena se rechaza. |
| No aparece el archivo del diagrama donde esperabas. | La pantalla escribe en `recursos/diagramas/automata_actual.png` respecto al directorio desde donde se ejecutó el programa. Inícialo desde la raíz del código o mediante el acceso directo del instalador. |
