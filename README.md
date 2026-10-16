# Simulador de Autómatas

**Avances_ProyectoF_Automatas** es una aplicación de escritorio desarrollada en **Python** para trabajar con autómatas finitos, expresiones regulares y validación de logs.

El proyecto utiliza **CustomTkinter** para la interfaz gráfica, **Graphviz** para la generación de diagramas y **pytest** para las pruebas automáticas.

El punto de entrada de la aplicación es:

```text
main.py
```

---

# Funciones principales

Actualmente el simulador permite:

- Crear autómatas finitos deterministas (**AFD**).
- Crear autómatas finitos no deterministas (**AFN**).
- Utilizar transiciones **ε** en AFN.
- Definir estados, alfabeto, estado inicial y estados finales.
- Agregar transiciones entre estados.
- Simular cadenas en AFD y AFN.
- Mostrar el recorrido realizado durante una simulación.
- Convertir un **AFN a AFD**.
- Minimizar un **AFD**.
- Generar diagramas mediante Graphviz.
- Visualizar diagramas utilizando estados simplificados y leyendas.
- Ajustar el tamaño de los diagramas.
- Acercar y alejar diagramas.
- Abrir el diagrama en una ventana independiente.
- Guardar y abrir autómatas mediante archivos JSON.
- Trabajar con expresiones regulares.
- Validar la sintaxis de expresiones regulares.
- Convertir expresiones regulares a notación postfix.
- Construir un AFN mediante el algoritmo de Thompson.
- Generar un AFD a partir de una expresión regular.
- Validar cadenas utilizando expresiones regulares.
- Generar automáticamente archivos de logs.
- Registrar eventos `INFO`, `WARNING`, `ERROR` y `CRITICAL`.
- Validar el formato de los archivos de logs.
- Detectar registros de logs inválidos.
- Filtrar logs por nivel de severidad.
- Filtrar logs por módulo.
- Mostrar resúmenes y cantidades por nivel de log.
- Utilizar tema claro, oscuro o el tema configurado en el sistema.

---

# 1. Tecnologías utilizadas

El proyecto utiliza principalmente:

| Tecnología | Uso |
| --- | --- |
| Python 3.12 | Lenguaje principal |
| CustomTkinter | Interfaz gráfica |
| Graphviz | Generación de diagramas |
| Pillow | Procesamiento y visualización de imágenes |
| pytest | Pruebas automáticas |
| PyInstaller | Generación del ejecutable |
| Inno Setup | Generación del instalador |

---

# 2. Estructura del proyecto

| Carpeta o archivo | Función |
| --- | --- |
| `algoritmos/` | Algoritmos de simulación, conversión, minimización, expresiones regulares, Thompson y análisis de logs |
| `interfaz/` | Pantallas desarrolladas con CustomTkinter |
| `modelos/` | Clases principales de los autómatas y expresiones regulares |
| `utilidades/` | Validaciones, persistencia, generación de diagramas, logs, tema y rutas |
| `tests/` | Pruebas automáticas realizadas con pytest |
| `recursos/` | Recursos utilizados por la aplicación |
| `graphviz_bin/` | Archivos utilizados para ejecutar Graphviz en Windows |
| `graphviz_tcl_backup/` | Respaldo de archivos auxiliares de Graphviz |
| `main.py` | Punto de entrada del programa |
| `requirements.txt` | Dependencias del proyecto |
| `SimuladorAutomatas.spec` | Configuración de PyInstaller |
| `instalador.iss` | Configuración de Inno Setup |
| `.gitignore` | Archivos y carpetas que no deben almacenarse en Git |

---

# 3. Modelos principales

## `modelos/`

| Archivo | Responsabilidad |
| --- | --- |
| `automata.py` | Clase base para los autómatas |
| `afd.py` | Implementación de Autómata Finito Determinista |
| `afn.py` | Implementación de Autómata Finito No Determinista |
| `expresion_regular.py` | Representación de una expresión regular |

Los autómatas almacenan principalmente:

```text
Nombre
Estados
Alfabeto
Estado inicial
Estados finales
Transiciones
```

---

# 4. Algoritmos

## `algoritmos/`

### `epsilon.py`

Gestiona operaciones relacionadas con transiciones ε, incluyendo el cálculo de la **ε-cerradura**.

### `simulador.py`

Ejecuta simulaciones detalladas de AFD y AFN y permite conocer el recorrido realizado por una cadena.

### `conversion.py`

Convierte un AFN en un AFD equivalente utilizando construcción de subconjuntos y ε-cerradura.

### `minimizacion.py`

Reduce un AFD mediante refinamiento de particiones conservando el lenguaje aceptado.

### `procesador_regex.py`

Procesa expresiones regulares y prepara su representación para utilizarla en los algoritmos posteriores.

Entre sus funciones se encuentra el manejo de:

```text
|
*
+
?
()
ε
```

También se utiliza concatenación explícita internamente para facilitar el procesamiento.

### `thompson.py`

Implementa el **algoritmo de Thompson** para construir un AFN equivalente a partir de una expresión regular.

Permite trabajar con:

- Símbolos.
- Concatenación.
- Unión.
- Cerradura de Kleene `*`.
- Operador `+`.
- Operador opcional `?`.
- Epsilon `ε`.

### `integracion_regex.py`

Integra los diferentes componentes de expresiones regulares.

Permite realizar procesos como:

```text
Expresión regular
        ↓
Validación
        ↓
Procesamiento
        ↓
Thompson
        ↓
AFN
        ↓
AFD
        ↓
Simulación
```

### `analizador_logs.py`

Analiza y valida archivos de logs.

Permite:

- Leer archivos `.txt` y `.log`.
- Validar cada registro.
- Identificar registros válidos.
- Identificar registros inválidos.
- Separar fecha, hora, nivel, módulo y mensaje.
- Contar registros según su nivel.
- Analizar logs mediante expresiones regulares.

---

# 5. Expresiones regulares

La aplicación posee una sección específica para trabajar con expresiones regulares.

Una expresión como:

```text
(0|1)*01
```

puede ser procesada por el sistema.

El flujo utilizado es:

```text
Expresión regular
        ↓
Validación sintáctica
        ↓
Procesamiento
        ↓
Conversión a postfix
        ↓
Algoritmo de Thompson
        ↓
AFN
        ↓
Conversión AFN → AFD
```

La aplicación también permite validar directamente si una cadena pertenece al lenguaje representado por la expresión regular.

Por ejemplo:

```text
Expresión:
(0|1)*01
```

Ejemplos:

| Cadena | Resultado |
| --- | --- |
| `01` | Aceptada |
| `101` | Aceptada |
| `1101` | Aceptada |
| `00` | Rechazada |
| `111` | Rechazada |

---

# 6. Creación de autómatas

La pantalla **Nuevo autómata** permite crear:

```text
AFD
AFN
```

El usuario debe proporcionar:

```text
Nombre
Estados
Alfabeto
Estado inicial
Estados finales
```

Posteriormente puede agregar las transiciones.

En los AFN se permite utilizar:

```text
ε
```

sin necesidad de incluirlo manualmente dentro del alfabeto.

---

# 7. Simulación de cadenas

La opción **Simular cadena** permite comprobar si una cadena es aceptada o rechazada.

La aplicación muestra:

- Cadena evaluada.
- Recorrido realizado.
- Estados alcanzados.
- Resultado final.

Los estados visuales utilizan:

```text
Verde   → operación correcta o cadena aceptada
Naranja → advertencia o cadena rechazada
Rojo    → error
```

---

# 8. Conversión AFN → AFD

La aplicación permite convertir un AFN en un AFD equivalente.

Durante el proceso se utiliza:

```text
ε-cerradura
Construcción de subconjuntos
Tabla de transición
```

Al finalizar se muestra:

- Cantidad de estados del AFN.
- Cantidad de estados del AFD.
- Tabla de transición.
- Resultado de la conversión.

El AFD generado puede utilizarse como el autómata actual.

---

# 9. Minimización de AFD

La sección **Minimizar AFD** permite generar un AFD equivalente con menor cantidad de estados cuando existen estados equivalentes.

El sistema muestra:

```text
Estados originales
Estados del AFD mínimo
Estados eliminados
Resultado de la minimización
```

El AFD mínimo también puede utilizarse posteriormente como autómata actual.

---

# 10. Diagramas

Los diagramas se generan utilizando **Graphviz**.

La aplicación incluye:

- Visualización dentro de la ventana principal.
- Ajuste automático del diagrama.
- Zoom.
- Barras de desplazamiento.
- Visualización al 100 %.
- Ventana independiente para una visualización ampliada.

Cuando los nombres de los estados son demasiado largos, la representación gráfica utiliza alias como:

```text
A
B
C
D
```

Debajo del diagrama se muestra una leyenda con la relación entre cada alias y el nombre real del estado.

Ejemplo:

```text
A = q0
B = {q0,q1}
C = {q1,q2}
```

Esto permite mantener los diagramas legibles incluso después de realizar conversiones o minimizaciones.

---

# 11. Sistema de logs

El simulador genera automáticamente archivos de logs durante su ejecución.

Los archivos se almacenan localmente en:

```text
logs/
```

y utilizan nombres similares a:

```text
logs_2026-10-15.txt
```

El formato utilizado es:

```text
FECHA Y HORA | NIVEL | MÓDULO | MENSAJE
```

Ejemplo:

```text
2026-10-15 22:30:00 | INFO     | SISTEMA      | Aplicación iniciada correctamente.
2026-10-15 22:31:10 | WARNING  | REGEX        | Expresión regular inválida.
2026-10-15 22:32:20 | ERROR    | ARCHIVO      | No fue posible abrir el autómata.
```

Los niveles disponibles son:

```text
INFO
WARNING
ERROR
CRITICAL
```

Los archivos generados dentro de `logs/` no se almacenan en Git.

---

# 12. Validación de logs

La sección **Validación de logs** permite analizar los archivos generados por la aplicación.

El usuario puede:

- Abrir automáticamente el log del día.
- Seleccionar otro archivo `.txt` o `.log`.
- Actualizar el archivo actualmente cargado.
- Filtrar registros por nivel.
- Filtrar registros por módulo.
- Combinar filtros.
- Limpiar filtros.
- Consultar registros válidos.
- Consultar registros inválidos.

El sistema también muestra un resumen como:

```text
INFO       203
WARNING      4
ERROR        0
CRITICAL     1

Registros válidos:   208
Registros inválidos:   0
```

## Registro válido

Un registro válido cumple el formato:

```text
Fecha y hora | Nivel | Módulo | Mensaje
```

Ejemplo:

```text
2026-10-15 23:20:15 | INFO | DIAGRAMA | Diagrama generado correctamente.
```

## Registro inválido

Un registro inválido es una línea que no cumple con la estructura requerida.

Ejemplo:

```text
ESTO NO ES UN LOG VALIDO
```

El sistema podría indicar:

```text
Línea 209:
El registro no cumple el formato esperado.

Contenido:
ESTO NO ES UN LOG VALIDO
```

Un registro inválido no significa necesariamente que la aplicación haya fallado.

Por ejemplo:

```text
ERROR
```

es un nivel válido de log que informa un problema ocurrido durante la ejecución.

En cambio, un **registro inválido** significa que la propia línea del archivo no cumple con la estructura esperada.

---

# 13. Interfaz gráfica

La aplicación utiliza una paleta visual centralizada en:

```text
utilidades/tema.py
```

Existen tres modos de apariencia:

```text
Sistema
Claro
Oscuro
```

Los colores se aplican de manera consistente a:

- Fondos.
- Paneles.
- Botones.
- Entradas.
- Títulos.
- Mensajes.
- Advertencias.
- Errores.
- Controles deshabilitados.

---

# 14. Barra de estado

La parte inferior de la aplicación muestra información sobre la operación actual.

Los colores representan:

| Color | Significado |
| --- | --- |
| Verde | Operación realizada correctamente |
| Naranja | Advertencia o resultado rechazado |
| Rojo | Error |
| Normal | Estado informativo |

Ejemplo:

```text
Estado: AFD - MiAutomata | Cadena aceptada
```

o:

```text
Estado: Logs validados - 208 válidos
```

---

# 15. Persistencia

Los autómatas pueden almacenarse mediante archivos JSON.

Esto permite:

```text
Crear autómata
      ↓
Guardar
      ↓
Cerrar programa
      ↓
Abrir nuevamente
      ↓
Recuperar autómata
```

---

# 16. Pruebas automáticas

El proyecto utiliza **pytest**.

Actualmente la batería completa contiene:

```text
150 pruebas
```

Las pruebas verifican, entre otras cosas:

- AFD.
- AFN.
- ε-cerradura.
- Validaciones.
- Persistencia.
- Simulación.
- Conversión AFN → AFD.
- Minimización.
- Generación de diagramas.
- Expresiones regulares.
- Procesamiento de regex.
- Thompson.
- Integración regex → AFN → AFD.
- Sistema de logs.
- Validación de logs.
- Integración general de la Fase 2.

El resultado actual esperado es:

```text
150 passed
```

---

# 17. Ejecutar las pruebas

En Windows puede utilizarse:

```powershell
$env:PATH = "$PWD\graphviz_bin;$env:PATH"

New-Item -ItemType Directory -Force "$HOME\Documents\pytest_temp_automatas"

$env:TEMP = "$HOME\Documents\pytest_temp_automatas"
$env:TMP = "$HOME\Documents\pytest_temp_automatas"

python -m pytest -v -p no:cacheprovider --basetemp="$HOME\Documents\pytest_temp_automatas"
```

Al finalizar debe aparecer:

```text
150 passed
```

---

# 18. Preparar el proyecto

Estas instrucciones están orientadas principalmente a Windows con Python 3.12.

## Clonar el repositorio

```powershell
git clone https://github.com/cristhyanlopez5-CRL24/Avances_ProyectoF_Automatas.git

cd Avances_ProyectoF_Automatas
```

## Crear entorno virtual

```powershell
py -3.12 -m venv venv
```

Activarlo:

```powershell
.\venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
```

---

# 19. Ejecutar la aplicación

Con el entorno virtual activo:

```powershell
python main.py
```

`main.py` configura automáticamente Graphviz mediante:

```text
utilidades/rutas.py
```

---

# 20. Generar ejecutable

Los archivos ejecutables no deben almacenarse directamente en el repositorio.

Para generar la aplicación:

```powershell
python -m PyInstaller SimuladorAutomatas.spec
```

PyInstaller genera:

```text
build/
dist/
```

Estas carpetas están excluidas mediante `.gitignore`.

---

# 21. Generar instalador

Después de generar correctamente el ejecutable:

1. Abrir `instalador.iss` con Inno Setup.
2. Verificar la ruta del programa generado.
3. Presionar **Compile** o `F9`.
4. Generar el instalador.

Los instaladores finales tampoco deben almacenarse en Git.

---

# 22. Archivos excluidos del repositorio

El proyecto utiliza `.gitignore` para evitar subir archivos generados o innecesarios.

Entre ellos:

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
logs/*.txt
```

Por lo tanto, los archivos de logs generados durante la ejecución permanecen únicamente de forma local.

---

# 23. Flujo general del sistema

El funcionamiento general puede representarse así:

```text
                     SIMULADOR
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     Autómatas           Regex           Logs
        │                │                │
   AFD / AFN        Validación       Generación
        │                │                │
   Simulación       Thompson         Validación
        │                │                │
 AFN → AFD            AFN            Filtros
        │                │                │
 Minimización          AFD          Severidades
        │                │                │
   Diagramas        Simulación       Resultados
```

---

# 24. Flujo de expresiones regulares

```text
Regex
  │
  ▼
Validación
  │
  ▼
Procesamiento
  │
  ▼
Postfix
  │
  ▼
Thompson
  │
  ▼
AFN
  │
  ▼
AFD
  │
  ▼
Simulación
```

---

# 25. Flujo de logs

```text
Aplicación
    │
    ▼
Evento
    │
    ▼
INFO / WARNING / ERROR / CRITICAL
    │
    ▼
Archivo TXT
    │
    ▼
Validación de formato
    │
    ├── Registro válido
    │
    └── Registro inválido
            │
            ▼
      Visor de logs
            │
            ▼
      Nivel + Módulo
```

---

# 26. Estado actual del proyecto

La aplicación integra actualmente las funcionalidades desarrolladas durante la **Fase 1** y la **Fase 2**.

La Fase 2 incluye principalmente:

```text
Expresiones regulares
Procesamiento de regex
Algoritmo de Thompson
Regex → AFN
Regex → AFD
Validación de cadenas
Sistema automático de logs
Validación de logs
Filtros de logs
Resumen por severidad
Mejoras visuales
Mejoras del visor de diagramas
```

La batería completa del proyecto se encuentra actualmente en:

```text
150 pruebas aprobadas
```

---

# 27. Control de versiones

El desarrollo se realiza mediante Git y GitHub utilizando ramas individuales y una rama de integración.

Durante la Fase 2 se utiliza:

```text
Rama personal
      ↓
Pull Request
      ↓
fase-2
```

La rama:

```text
main
```

se mantiene como versión estable hasta finalizar completamente la integración y revisión de la fase actual.
