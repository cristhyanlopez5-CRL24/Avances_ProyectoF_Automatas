# Simulador de Autómatas

**Avances_ProyectoF_Automatas** contiene una aplicación de escritorio desarrollada en **Python** para crear, simular, convertir, minimizar y visualizar autómatas finitos.

La interfaz utiliza **CustomTkinter** y los diagramas se generan con **Graphviz**. El punto de entrada de la aplicación es [main.py](main.py).

## Funciones principales

- Crear autómatas finitos deterministas (**AFD**) y no deterministas (**AFN**).
- Definir estados, alfabeto, estado inicial, estados finales y transiciones.
- Trabajar con transiciones **ε** en AFN.
- Simular cadenas y mostrar su recorrido.
- Convertir un AFN a AFD mediante construcción de subconjuntos y ε-cerradura.
- Minimizar un AFD.
- Generar diagramas del autómata.
- Guardar y abrir autómatas mediante archivos JSON.
- Utilizar tema claro, oscuro o el tema del sistema.

## 1. Estructura del repositorio

| Carpeta o archivo | Función |
| --- | --- |
| [algoritmos/](algoritmos/) | Contiene los algoritmos de simulación, ε-cerradura, conversión AFN → AFD y minimización. |
| [interfaz/](interfaz/) | Contiene las ventanas y controles de la aplicación construidos con CustomTkinter. |
| [modelos/](modelos/) | Define las clases principales del proyecto: `Automata`, `AFD` y `AFN`. |
| [utilidades/](utilidades/) | Contiene validaciones, persistencia JSON, generación de diagramas y manejo de rutas. |
| [tests/](tests/) | Pruebas automáticas realizadas con pytest. |
| [recursos/](recursos/) | Recursos utilizados por la aplicación y diagramas de ejemplo. |
| [graphviz_bin/](graphviz_bin/) | Actualmente contiene el motor de Graphviz utilizado por la aplicación en Windows. |
| [graphviz_tcl_backup/](graphviz_tcl_backup/) | Archivos auxiliares de respaldo relacionados con Graphviz. Actualmente no forman parte directa del flujo principal. |
| [main.py](main.py) | Punto de entrada de la aplicación. |
| [requirements.txt](requirements.txt) | Dependencias necesarias para desarrollar y ejecutar el proyecto. |
| [SimuladorAutomatas.spec](SimuladorAutomatas.spec) | Configuración utilizada por PyInstaller para generar la aplicación ejecutable. |
| [instalador.iss](instalador.iss) | Script de Inno Setup utilizado para generar un instalador de Windows. |
| [.gitignore](.gitignore) | Evita subir al repositorio archivos generados, ejecutables, entornos virtuales, cachés y otros archivos innecesarios. |

## 2. Archivos principales

### modelos/

| Archivo | Responsabilidad |
| --- | --- |
| [automata.py](modelos/automata.py) | Clase base que almacena estados, alfabeto, estado inicial, estados finales y transiciones. |
| [afd.py](modelos/afd.py) | Implementa las reglas y simulación de un AFD. |
| [afn.py](modelos/afn.py) | Implementa AFN, múltiples destinos y transiciones ε. |

### algoritmos/

| Archivo | Responsabilidad |
| --- | --- |
| [epsilon.py](algoritmos/epsilon.py) | Calcula ε-cerraduras y movimientos entre conjuntos de estados. |
| [simulador.py](algoritmos/simulador.py) | Ejecuta simulaciones detalladas de AFD y AFN. |
| [conversion.py](algoritmos/conversion.py) | Convierte un AFN en un AFD equivalente. |
| [minimizacion.py](algoritmos/minimizacion.py) | Minimiza AFD mediante refinamiento de particiones. |

### interfaz/

| Archivo | Responsabilidad |
| --- | --- |
| [ventana_principal.py](interfaz/ventana_principal.py) | Ventana principal y navegación de la aplicación. |
| [crear_automata.py](interfaz/crear_automata.py) | Pantalla para crear AFD y AFN. |
| [simular_cadena.py](interfaz/simular_cadena.py) | Pantalla para evaluar cadenas. |
| [conversion_afn_afd.py](interfaz/conversion_afn_afd.py) | Interfaz de conversión AFN → AFD. |
| [minimizar_afd.py](interfaz/minimizar_afd.py) | Interfaz de minimización. |
| [ver_diagrama.py](interfaz/ver_diagrama.py) | Genera y muestra el diagrama del autómata. |

### utilidades/

| Archivo | Responsabilidad |
| --- | --- |
| [validaciones.py](utilidades/validaciones.py) | Valida datos introducidos por el usuario. |
| [persistencia.py](utilidades/persistencia.py) | Guarda y recupera autómatas mediante JSON. |
| [graficador.py](utilidades/graficador.py) | Construye el grafo y solicita a Graphviz la generación de imágenes. |
| [rutas.py](utilidades/rutas.py) | Configura las rutas necesarias para Graphviz y los recursos del programa. |

## 3. Funcionamiento general

1. `main.py` configura Graphviz e inicia `VentanaPrincipal`.
2. La interfaz recibe y valida los datos introducidos por el usuario.
3. Se crea un objeto `AFD` o `AFN` dentro de `modelos/`.
4. Los módulos de `algoritmos/` realizan simulaciones, conversiones y minimizaciones.
5. `utilidades/graficador.py` genera la representación gráfica.
6. `utilidades/persistencia.py` permite guardar y recuperar autómatas en formato JSON.

La aplicación trabaja con **un autómata actual a la vez**.

## 4. Archivos que no se almacenan en el repositorio

El repositorio mantiene principalmente el **código fuente, pruebas, documentación y archivos necesarios para reconstruir el proyecto**.

Los siguientes elementos se generan localmente y están excluidos mediante `.gitignore`:

```text
venv/
.venv/
build/
dist/
__pycache__/
*.pyc
*.pyo
*.exe
*.msi
*.dll
*.pyd
*.zip
*.rar
*.7z
*.pkg
*.pyz
*.toc
*.log
*.tmp
```

Por esta razón, el repositorio ya no almacena el entorno virtual, resultados de compilación, instaladores finales, ZIP de entregas, cachés de Python ni el archivo temporal `recursos/diagramas/automata_actual.png`.

Estos elementos pueden volver a generarse cuando sean necesarios y no forman parte del código fuente que debe mantenerse bajo control de versiones.

## 5. Preparar el proyecto

Estas instrucciones están orientadas a **Windows con Python 3.12**.

### Clonar el repositorio

```powershell
git clone https://github.com/cristhyanlopez5-CRL24/Avances_ProyectoF_Automatas.git
cd Avances_ProyectoF_Automatas
```

También es posible descargar el código utilizando **Code → Download ZIP** desde GitHub.

### Crear un entorno virtual

El entorno virtual no se incluye en el repositorio. Cada equipo debe crear el suyo:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Si `py` no está disponible:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Ejecutar la aplicación

```powershell
.\.venv\Scripts\python.exe main.py
```

Actualmente la aplicación utiliza el Graphviz incluido en `graphviz_bin/`. `main.py` llama a `configurar_graphviz()` de `utilidades/rutas.py` para agregarlo al `PATH` del proceso.

> **Nota:** la integración de Graphviz será revisada posteriormente para evitar mantener ejecutables y bibliotecas binarias dentro del repositorio.

## 6. Ejecutar las pruebas

Después de instalar las dependencias:

```powershell
.\.venv\Scripts\python.exe -c "from utilidades.rutas import configurar_graphviz; configurar_graphviz(); import pytest; raise SystemExit(pytest.main(['-q', 'tests']))"
```

Si Graphviz ya está correctamente disponible en el `PATH`:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

## 7. Generar el ejecutable localmente

Los ejecutables y archivos de compilación **no deben subirse al repositorio**.

```powershell
.\.venv\Scripts\python.exe -m PyInstaller SimuladorAutomatas.spec
```

PyInstaller crea automáticamente `build/` y `dist/`. Estas carpetas están excluidas por `.gitignore`.

## 8. Generar el instalador localmente

Después de generar correctamente `dist/SimuladorAutomatas/`:

1. Abre `instalador.iss` con Inno Setup.
2. Comprueba que exista `dist/SimuladorAutomatas/`.
3. Selecciona **Compile** o presiona **F9**.
4. Inno Setup genera el instalador correspondiente.

El instalador generado también está excluido del repositorio.

## 9. Ejemplo de uso

Para crear un AFD que acepte cadenas terminadas en `01`:

| Estado | Con `0` | Con `1` |
| --- | --- | --- |
| `q0` | `q1` | `q0` |
| `q1` | `q1` | `q2` |
| `q2` | `q1` | `q0` |

Configuración:

```text
Estados: q0, q1, q2
Alfabeto: 0, 1
Estado inicial: q0
Estado final: q2
```

| Cadena | Resultado |
| --- | --- |
| `01` | Aceptada |
| `101` | Aceptada |
| `0001` | Aceptada |
| `10` | Rechazada |
| `111` | Rechazada |

Para un AFN pueden utilizarse transiciones ε. La opción ε aparece automáticamente en la interfaz y no debe agregarse manualmente al alfabeto.

## 10. Solución de problemas

| Situación | Qué revisar |
| --- | --- |
| `ModuleNotFoundError` para `customtkinter`, `PIL` o `graphviz` | Instalar las dependencias de `requirements.txt` usando el mismo entorno virtual con el que se ejecuta la aplicación. |
| No se genera el diagrama | Actualmente debe existir `graphviz_bin/` y `utilidades/rutas.py` debe poder localizarlo. |
| Los botones de simulación o diagrama están deshabilitados | Primero debe crearse o abrirse un autómata. |
| Una cadena válida se rechaza | Revisar estado inicial, estados finales y transiciones. |
| Aparece `automata_actual.png` después de ejecutar la aplicación | Es normal. Es un archivo generado automáticamente y `.gitignore` evita que se suba al repositorio. |

## Control de versiones

El repositorio utiliza `.gitignore` para evitar que archivos generados o dependencias locales sean incluidos accidentalmente en nuevos commits.

El código fuente y los archivos de configuración permanecen versionados, mientras que los ejecutables, instaladores, entornos virtuales, archivos comprimidos y resultados de compilación se generan localmente cuando sean necesarios.