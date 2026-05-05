; ============================================================
;  SeguridadMaster - Script de instalacion InnoSetup
;  Requiere: InnoSetup 6.x  https://jrsoftware.org/isinfo.php
; ============================================================

#define AppName      "SeguridadMaster"
#define AppVersion   "1.0"
#define AppPublisher "DATEC"
#define AppExeName   "SeguridadMaster.exe"
#define ReleaseDir   "C:\Users\andresvargas\source\repos\SeguridadMaster\SeguridadMaster\bin\Release\net8.0-windows"

[Setup]
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppId={{EDC0650A-A7A2-4B5D-ACF2-64AD890C5AFE}
AppVerName={#AppName} {#AppVersion}
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
OutputBaseFilename=SeguridadMaster_Setup
OutputDir=Installer
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64compatible
; Permite solo una instalacion a la vez
AppMutex=SeguridadMasterMutex
; Informacion de desinstalacion en Panel de Control
UninstallDisplayName={#AppName}
UninstallDisplayIcon={app}\{#AppExeName}
; Minimo Windows 10
MinVersion=10.0

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon";   Description: "Crear acceso directo en el &Escritorio";  GroupDescription: "Accesos directos:"
Name: "startmenuicon"; Description: "Crear acceso directo en el &Menu Inicio"; GroupDescription: "Accesos directos:"

; ─────────────────────────────────────────────────────────
;  Archivos
; ─────────────────────────────────────────────────────────
[Files]
; Ejecutable y biblioteca principal
Source: "{#ReleaseDir}\SeguridadMaster.exe";               DestDir: "{app}"; Flags: ignoreversion
Source: "{#ReleaseDir}\SeguridadMaster.dll";               DestDir: "{app}"; Flags: ignoreversion
Source: "{#ReleaseDir}\SeguridadMaster.runtimeconfig.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ReleaseDir}\SeguridadMaster.deps.json";         DestDir: "{app}"; Flags: ignoreversion

; Dependencias NuGet
Source: "{#ReleaseDir}\Microsoft.Win32.TaskScheduler.dll"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ReleaseDir}\System.Diagnostics.EventLog.dll";   DestDir: "{app}"; Flags: ignoreversion

; Runtime nativo de Windows
Source: "{#ReleaseDir}\runtimes\win\lib\net8.0\System.Diagnostics.EventLog.dll"; DestDir: "{app}\runtimes\win\lib\net8.0"; Flags: ignoreversion

; Recursos de idioma de TaskScheduler
Source: "{#ReleaseDir}\de\*";    DestDir: "{app}\de";    Flags: ignoreversion
Source: "{#ReleaseDir}\es\*";    DestDir: "{app}\es";    Flags: ignoreversion
Source: "{#ReleaseDir}\fr\*";    DestDir: "{app}\fr";    Flags: ignoreversion
Source: "{#ReleaseDir}\it\*";    DestDir: "{app}\it";    Flags: ignoreversion
Source: "{#ReleaseDir}\ja\*";    DestDir: "{app}\ja";    Flags: ignoreversion
Source: "{#ReleaseDir}\pl\*";    DestDir: "{app}\pl";    Flags: ignoreversion
Source: "{#ReleaseDir}\ru\*";    DestDir: "{app}\ru";    Flags: ignoreversion
Source: "{#ReleaseDir}\sv\*";    DestDir: "{app}\sv";    Flags: ignoreversion
Source: "{#ReleaseDir}\tr\*";    DestDir: "{app}\tr";    Flags: ignoreversion
Source: "{#ReleaseDir}\zh-CN\*"; DestDir: "{app}\zh-CN"; Flags: ignoreversion
Source: "{#ReleaseDir}\zh-Hant\*"; DestDir: "{app}\zh-Hant"; Flags: ignoreversion

; ─────────────────────────────────────────────────────────
;  Accesos directos
; ─────────────────────────────────────────────────────────
[Icons]
; Menu Inicio
Name: "{group}\{#AppName}";           Filename: "{app}\{#AppExeName}"; Tasks: startmenuicon
Name: "{group}\Desinstalar {#AppName}"; Filename: "{uninstallexe}";    Tasks: startmenuicon

; Escritorio
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon

; ─────────────────────────────────────────────────────────
;  Ejecutar al finalizar la instalacion
; ─────────────────────────────────────────────────────────
[Run]
Filename: "{app}\{#AppExeName}"; Description: "Iniciar {#AppName} ahora"; Flags: nowait postinstall skipifsilent runascurrentuser

; ─────────────────────────────────────────────────────────
;  Verificacion de .NET 8.0 Desktop Runtime (Pascal Script)
; ─────────────────────────────────────────────────────────
[Code]

// Comprueba si .NET 8 Desktop Runtime esta instalado verificando la existencia
// de la carpeta del runtime en el sistema de archivos (mas confiable que el registro).
function IsDotNet8DesktopInstalled(): Boolean;
var
  FindRec: TFindRec;
  BasePath: string;
begin
  Result := False;
  BasePath := ExpandConstant('{pf}') + '\dotnet\shared\Microsoft.WindowsDesktop.App\';
  if FindFirst(BasePath + '8.*', FindRec) then
  begin
    repeat
      if FindRec.Attributes and FILE_ATTRIBUTE_DIRECTORY <> 0 then
      begin
        Result := True;
        Break;
      end;
    until not FindNext(FindRec);
    FindClose(FindRec);
  end;
end;

function InitializeSetup(): Boolean;
var
  Respuesta: Integer;
begin
  Result := True;

  if not IsDotNet8DesktopInstalled() then
  begin
    Respuesta := MsgBox(
      '.NET 8.0 Desktop Runtime no esta instalado en este equipo.' + #13#10 + #13#10 +
      'SeguridadMaster requiere .NET 8.0 Desktop Runtime para funcionar.' + #13#10 +
      'Por favor, descargue e instale el runtime desde:' + #13#10 +
      'https://dotnet.microsoft.com/download/dotnet/8.0' + #13#10 + #13#10 +
      'Haga clic en Aceptar para abrir la pagina de descarga en su navegador,' + #13#10 +
      'o en Cancelar para salir del instalador.',
      mbError,
      MB_OKCANCEL
    );

    if Respuesta = IDOK then
      ShellExec('open', 'https://dotnet.microsoft.com/download/dotnet/8.0', '', '', SW_SHOWNORMAL, ewNoWait, Respuesta);

    Result := False;
  end;
end;
