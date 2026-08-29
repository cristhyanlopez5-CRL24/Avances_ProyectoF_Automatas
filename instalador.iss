#define MyAppName "Simulador de Autómatas"
#define MyAppVersion "1.0"
#define MyAppPublisher "Proyecto Universitario"
#define MyAppExeName "SimuladorAutomatas.exe"

[Setup]

; ============================================================
; INFORMACIÓN GENERAL
; ============================================================

AppId={{F39E05C9-4F04-4C92-BEAC-2B6B7FC10A62}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

; ============================================================
; CARPETA DE INSTALACIÓN
; ============================================================

DefaultDirName={localappdata}\Programs\SimuladorAutomatas
DefaultGroupName={#MyAppName}

DisableProgramGroupPage=yes

; Instalación sin requerir administrador
PrivilegesRequired=lowest

; ============================================================
; SALIDA DEL INSTALADOR
; ============================================================

OutputDir=instalador
OutputBaseFilename=SimuladorAutomatas_Setup

; ============================================================
; COMPRESIÓN
; ============================================================

Compression=lzma2
SolidCompression=yes

; ============================================================
; APARIENCIA
; ============================================================

WizardStyle=modern

; ============================================================
; INFORMACIÓN DE DESINSTALACIÓN
; ============================================================

UninstallDisplayName={#MyAppName}

; ============================================================
; VERSIÓN
; ============================================================

VersionInfoVersion=1.0.0.0
VersionInfoDescription=Simulador de Autómatas
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}


[Languages]

Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"


[Tasks]

Name: "desktopicon"; \
Description: "Crear acceso directo en el escritorio"; \
GroupDescription: "Accesos directos:"; \
Flags: unchecked


[Files]

; ============================================================
; COPIAR TODO EL PROGRAMA GENERADO POR PYINSTALLER
; ============================================================

Source: "dist\SimuladorAutomatas\*"; \
DestDir: "{app}"; \
Flags: ignoreversion recursesubdirs createallsubdirs


[Icons]

; ============================================================
; MENÚ INICIO
; ============================================================

Name: "{autoprograms}\{#MyAppName}"; \
Filename: "{app}\{#MyAppExeName}"; \
WorkingDir: "{app}"


; ============================================================
; ESCRITORIO
; ============================================================

Name: "{autodesktop}\{#MyAppName}"; \
Filename: "{app}\{#MyAppExeName}"; \
WorkingDir: "{app}"; \
Tasks: desktopicon


[Run]

; ============================================================
; EJECUTAR AL FINALIZAR LA INSTALACIÓN
; ============================================================

Filename: "{app}\{#MyAppExeName}"; \
Description: "Ejecutar {#MyAppName}"; \
WorkingDir: "{app}"; \
Flags: nowait postinstall skipifsilent