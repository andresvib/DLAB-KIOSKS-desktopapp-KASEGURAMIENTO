# SeguridadMaster

Aplicación de escritorio WPF (.NET 8) para Windows que activa un escudo de seguridad perimetral: bloquea dispositivos USB, restringe acceso WiFi, FTP y RDP, y aplica un hook de teclado global. Se distribuye mediante instalador generado con InnoSetup.

---

## Funcionalidades

| Función | Descripción | Reversible |
|---|---|---|
| **Bloqueo USB** | Deshabilita almacenamiento masivo USB vía GPO y driver USBSTOR. No afecta teclados, ratones ni escáneres HID. | Sí |
| **Firewall RDP** | Restringe acceso RDP (puerto 3389) a una lista blanca de IPs. Por defecto solo permite `127.0.0.1`. | Sí |
| **Bloqueo FTP** | Añade regla de firewall para bloquear salida por el puerto 21. | Sí |
| **Deshabilitar WiFi** | Desactiva todos los adaptadores inalámbricos del equipo. | Sí |
| **Hook de teclado** | Bloquea Win, Alt+Tab, Alt+F4 y Ctrl+Esc a nivel de sistema. | Sí |
| **Inicio automático** | Registra tarea programada para arrancar con privilegios de Administrador en cada inicio de sesión. | Manual |

### Desbloqueo

Para restaurar el sistema al estado normal, presione la combinación:

```
Ctrl + Shift + Alt + K
```

Al presionarla, la aplicación detiene el hook, elimina las reglas de firewall, reactiva USB y WiFi, y se cierra.

---

## Requisitos

- Windows 10 / Windows 11 (64-bit)
- [.NET 8.0 Desktop Runtime (x64)](https://dotnet.microsoft.com/download/dotnet/8.0)
- Privilegios de Administrador local
- `SuperVisor.WPF.exe` instalado en `C:\Program Files\Datec\SuperVisor\`

---

## Instalación

1. Descargue el instalador `SeguridadMaster_Setup.exe`.
2. Haga **clic derecho** sobre el archivo y seleccione **Ejecutar como administrador**.
3. Acepte el diálogo de UAC.
4. Si .NET 8.0 Desktop Runtime no está instalado, el asistente lo detectará y abrirá la página de descarga automáticamente.
5. Siga los pasos del asistente: seleccione la carpeta de instalación y los accesos directos deseados.
6. Haga clic en **Instalar** y luego en **Finalizar**.

> La carpeta de instalación predeterminada es `C:\Program Files\SeguridadMaster\`.

---

## Uso

- Al iniciar, la aplicación se auto-registra en el **Programador de Tareas** de Windows (`SeguridadMaster_AutoStart`) para arrancar en cada inicio de sesión con privilegios de Administrador.
- Tras 2 segundos, el escudo se activa automáticamente.
- La ventana principal muestra indicadores de estado (LED) para cada componente: Registro, Firewall, WiFi y Hook de teclado.
- Para desbloquear el sistema use **Ctrl + Shift + Alt + K**.

---

## Desinstalación

**Método recomendado:**  
Panel de Control → Programas → Programas y características → **SeguridadMaster** → Desinstalar.

**Limpieza manual adicional** (si el sistema no fue desbloqueado antes de desinstalar):

```bat
:: Eliminar tarea programada
schtasks /delete /tn "SeguridadMaster_AutoStart" /f

:: Eliminar reglas de firewall
netsh advfirewall firewall delete rule name="SeguridadMaster_RDP_Restricted"
netsh advfirewall firewall delete rule name="SeguridadMaster_Block_FTP"

:: Restaurar USB
reg add HKLM\SYSTEM\CurrentControlSet\Services\USBSTOR /v Start /t REG_DWORD /d 3 /f
```

---

## Tecnologías

- [.NET 8.0 / WPF](https://learn.microsoft.com/dotnet/desktop/wpf/)
- [Microsoft.Win32.TaskScheduler v2.12.2](https://github.com/dahall/TaskScheduler)
- [InnoSetup 6](https://jrsoftware.org/isinfo.php) — generación del instalador
- [ReportLab](https://www.reportlab.com/) — generación del manual en PDF

---

## Estructura del proyecto

```
SeguridadMaster/
├── Helpers/
│   ├── KeyboardHook.cs          # Hook global de teclado (Win32 API)
│   ├── NativeMethods.cs         # Importaciones P/Invoke
│   └── RegistryManager.cs       # Gestión de políticas de Registro y USB
├── Models/
│   └── SecurityConfig.cs
├── Services/
│   ├── NetworkService.cs        # Firewall y adaptadores de red
│   └── WindowsServiceManager.cs
├── MainWindow.xaml              # Interfaz principal
├── NotificacionDesbloqueo.xaml  # Ventana de notificación
└── SeguridadMaster.csproj
├── SeguridadMaster_Installer.iss   # Script InnoSetup
├── generar_guia.py                 # Generador del manual PDF
└── Guia_Instalacion_SeguridadMaster.pdf
```

---

## Desarrollado por

**Datec** — Uso interno.
