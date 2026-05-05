from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from datetime import datetime

OUTPUT = "C:/Users/andresvargas/source/repos/SeguridadMaster/Guia_Instalacion_SeguridadMaster.pdf"

doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2.5*cm,
    bottomMargin=2*cm,
    title="Guía de Instalación - SeguridadMaster",
    author="Datec"
)

styles = getSampleStyleSheet()

# ── Estilos personalizados ──────────────────────────────────────────────────
DARK_BLUE   = colors.HexColor("#1a2e4a")
MED_BLUE    = colors.HexColor("#2563eb")
LIGHT_BLUE  = colors.HexColor("#dbeafe")
ACCENT      = colors.HexColor("#dc2626")
GRAY_BG     = colors.HexColor("#f1f5f9")
GRAY_TEXT   = colors.HexColor("#475569")
GREEN       = colors.HexColor("#16a34a")
YELLOW_BG   = colors.HexColor("#fef9c3")
YELLOW_BR   = colors.HexColor("#ca8a04")

title_style = ParagraphStyle(
    "CustomTitle",
    parent=styles["Title"],
    fontSize=26,
    textColor=colors.white,
    alignment=TA_CENTER,
    spaceAfter=4,
    fontName="Helvetica-Bold",
)
subtitle_style = ParagraphStyle(
    "CustomSubtitle",
    parent=styles["Normal"],
    fontSize=11,
    textColor=colors.HexColor("#bfdbfe"),
    alignment=TA_CENTER,
    spaceAfter=2,
    fontName="Helvetica",
)
section_style = ParagraphStyle(
    "SectionHeader",
    parent=styles["Heading1"],
    fontSize=13,
    textColor=DARK_BLUE,
    fontName="Helvetica-Bold",
    spaceBefore=14,
    spaceAfter=6,
    borderPad=4,
)
subsection_style = ParagraphStyle(
    "SubSection",
    parent=styles["Heading2"],
    fontSize=11,
    textColor=MED_BLUE,
    fontName="Helvetica-Bold",
    spaceBefore=10,
    spaceAfter=4,
)
body_style = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontSize=10,
    textColor=colors.HexColor("#1e293b"),
    leading=15,
    spaceAfter=4,
    fontName="Helvetica",
    alignment=TA_JUSTIFY,
)
code_style = ParagraphStyle(
    "Code",
    parent=styles["Normal"],
    fontSize=9,
    fontName="Courier",
    textColor=DARK_BLUE,
    backColor=GRAY_BG,
    leftIndent=10,
    rightIndent=10,
    spaceBefore=2,
    spaceAfter=2,
    leading=13,
    borderPad=6,
)
note_style = ParagraphStyle(
    "Note",
    parent=styles["Normal"],
    fontSize=9,
    fontName="Helvetica-Oblique",
    textColor=GRAY_TEXT,
    leading=13,
    spaceAfter=4,
)
warning_style = ParagraphStyle(
    "Warning",
    parent=styles["Normal"],
    fontSize=10,
    fontName="Helvetica-Bold",
    textColor=colors.HexColor("#92400e"),
    leading=14,
    spaceAfter=2,
)
step_num_style = ParagraphStyle(
    "StepNum",
    parent=styles["Normal"],
    fontSize=10,
    fontName="Helvetica-Bold",
    textColor=MED_BLUE,
    leading=14,
)
footer_style = ParagraphStyle(
    "Footer",
    parent=styles["Normal"],
    fontSize=8,
    textColor=GRAY_TEXT,
    alignment=TA_CENTER,
    fontName="Helvetica",
)

def hr(color=colors.HexColor("#cbd5e1"), thickness=0.6):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=6, spaceBefore=2)

def section_title(text, number=None):
    prefix = f"{number}. " if number else ""
    return Paragraph(f"{prefix}{text}", section_style)

def step_row(number, text):
    """Fila de paso numerado con fondo alternado."""
    num_para = Paragraph(str(number), ParagraphStyle(
        "StepN", parent=styles["Normal"],
        fontSize=12, fontName="Helvetica-Bold",
        textColor=colors.white, alignment=TA_CENTER
    ))
    txt_para = Paragraph(text, body_style)
    bg = MED_BLUE if number % 2 != 0 else DARK_BLUE
    t = Table([[num_para, txt_para]], colWidths=[1*cm, 14.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), bg),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (0,0), 4),
        ("RIGHTPADDING", (0,0), (0,0), 4),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("ROWBACKGROUNDS", (1,0), (-1,-1), [colors.white]),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
    ]))
    return t

def info_box(text, bg=LIGHT_BLUE, border=MED_BLUE, icon="ℹ"):
    para = Paragraph(f"<b>{icon}  </b>{text}", body_style)
    t = Table([[para]], colWidths=[15.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX", (0,0), (-1,-1), 1.2, border),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
    ]))
    return t

def warning_box(text):
    para = Paragraph(f"<b>⚠  IMPORTANTE:  </b>{text}", warning_style)
    t = Table([[para]], colWidths=[15.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), YELLOW_BG),
        ("BOX", (0,0), (-1,-1), 1.2, YELLOW_BR),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
    ]))
    return t

# ── ENCABEZADO / PORTADA ────────────────────────────────────────────────────
def header_block():
    header_data = [[
        Paragraph("SeguridadMaster", title_style),
    ]]
    sub_data = [[
        Paragraph("Guía de Instalación y Configuración", subtitle_style),
    ]]
    date_str = datetime.today().strftime("%d de %B de %Y").replace(
        "January","enero").replace("February","febrero").replace("March","marzo"
        ).replace("April","abril").replace("May","mayo").replace("June","junio"
        ).replace("July","julio").replace("August","agosto").replace("September","septiembre"
        ).replace("October","octubre").replace("November","noviembre").replace("December","diciembre")
    meta_data = [[
        Paragraph(f"Versión 1.0  ·  {date_str}  ·  Datec", subtitle_style),
    ]]

    t = Table([header_data, sub_data, meta_data], colWidths=[15.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_BLUE),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 12),
        ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ("ROUNDEDCORNERS", (0,0), (-1,-1), 6),
    ]))
    return t

# ── TABLA DE REQUISITOS ──────────────────────────────────────────────────────
def req_table():
    data = [
        [Paragraph("<b>Requisito</b>", body_style), Paragraph("<b>Detalle</b>", body_style)],
        [Paragraph("Sistema Operativo", body_style), Paragraph("Windows 10 / Windows 11 (64-bit)", body_style)],
        [Paragraph("Framework", body_style), Paragraph(".NET 8.0 Runtime (Windows Desktop)", body_style)],
        [Paragraph("Privilegios", body_style), Paragraph("Administrador local (obligatorio)", body_style)],
        [Paragraph("Dependencias incluidas", body_style), Paragraph("Microsoft.Win32.TaskScheduler.dll, System.Diagnostics.EventLog.dll", body_style)],
        [Paragraph("App supervisora", body_style), Paragraph(r"C:\Program Files\Datec\SuperVisor\SuperVisor.WPF.exe", code_style)],
    ]
    t = Table(data, colWidths=[5*cm, 10.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK_BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, GRAY_BG]),
        ("BOX", (0,0), (-1,-1), 0.8, colors.HexColor("#94a3b8")),
        ("INNERGRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    return t

# ── TABLA PROPIEDADES DEL INSTALADOR ────────────────────────────────────────
def installer_table():
    data = [
        [Paragraph("<b>Propiedad</b>", body_style), Paragraph("<b>Detalle</b>", body_style)],
        [Paragraph("Nombre del instalador", body_style), Paragraph("SeguridadMaster_Setup.exe", code_style)],
        [Paragraph("Generado con", body_style), Paragraph("InnoSetup 6.x", body_style)],
        [Paragraph("Carpeta de instalación", body_style), Paragraph(r"C:\Program Files\SeguridadMaster\  (configurable en el asistente)", body_style)],
        [Paragraph("Accesos directos", body_style), Paragraph("Escritorio y Menú Inicio (seleccionables durante la instalación)", body_style)],
        [Paragraph("Verificación automática", body_style), Paragraph(".NET 8.0 Desktop Runtime — el instalador lo detecta y ofrece descargarlo si falta", body_style)],
        [Paragraph("Desinstalador", body_style), Paragraph("Registrado automáticamente en Panel de Control → Programas", body_style)],
        [Paragraph("Privilegios requeridos", body_style), Paragraph("Administrador (el instalador lo solicita vía UAC)", body_style)],
    ]
    t = Table(data, colWidths=[5*cm, 10.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK_BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, GRAY_BG]),
        ("BOX", (0,0), (-1,-1), 0.8, colors.HexColor("#94a3b8")),
        ("INNERGRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    return t

# ── TABLA FUNCIONES ──────────────────────────────────────────────────────────
def features_table():
    data = [
        [Paragraph("<b>Función</b>", body_style), Paragraph("<b>Descripción</b>", body_style), Paragraph("<b>Reversible</b>", body_style)],
        [Paragraph("Bloqueo USB", body_style),
         Paragraph("Deshabilita almacenamiento masivo USB vía GPO y driver USBSTOR. No afecta teclados, ratones ni escáneres HID.", body_style),
         Paragraph("<font color='#16a34a'><b>Sí</b></font>", body_style)],
        [Paragraph("Firewall RDP", body_style),
         Paragraph("Restringe acceso RDP (puerto 3389) a una lista blanca de IPs. Por defecto solo permite 127.0.0.1.", body_style),
         Paragraph("<font color='#16a34a'><b>Sí</b></font>", body_style)],
        [Paragraph("Bloqueo FTP", body_style),
         Paragraph("Añade regla de firewall para bloquear salida por el puerto 21.", body_style),
         Paragraph("<font color='#16a34a'><b>Sí</b></font>", body_style)],
        [Paragraph("Deshabilitar WiFi", body_style),
         Paragraph("Desactiva todos los adaptadores inalámbricos del equipo.", body_style),
         Paragraph("<font color='#16a34a'><b>Sí</b></font>", body_style)],
        [Paragraph("Hook de teclado", body_style),
         Paragraph("Bloquea Win, Alt+Tab, Alt+F4 y Ctrl+Esc. Escucha Ctrl+Shift+Alt+K para desbloquear.", body_style),
         Paragraph("<font color='#16a34a'><b>Sí</b></font>", body_style)],
        [Paragraph("Inicio automático", body_style),
         Paragraph("Registra tarea programada para arrancar con el inicio de sesión con privilegios de Administrador.", body_style),
         Paragraph("<font color='#dc2626'><b>Manual</b></font>", body_style)],
    ]
    t = Table(data, colWidths=[3.8*cm, 9*cm, 2.2*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), DARK_BLUE),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, GRAY_BG]),
        ("BOX", (0,0), (-1,-1), 0.8, colors.HexColor("#94a3b8")),
        ("INNERGRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("ALIGN", (2,0), (2,-1), "CENTER"),
    ]))
    return t

# ── CONSTRUCCIÓN DEL DOCUMENTO ───────────────────────────────────────────────
story = []

# Portada
story.append(header_block())
story.append(Spacer(1, 0.6*cm))
story.append(Paragraph(
    "Este documento describe los requisitos, procedimiento de instalación mediante el "
    "asistente <b>SeguridadMaster_Setup.exe</b>, configuración y uso básico de "
    "<b>SeguridadMaster</b>, la aplicación de seguridad perimetral desarrollada por "
    "Datec para entornos controlados.",
    body_style
))
story.append(Spacer(1, 0.3*cm))
story.append(hr())

# ── 1. DESCRIPCIÓN GENERAL ──────────────────────────────────────────────────
story.append(section_title("DESCRIPCIÓN GENERAL", 1))
story.append(Paragraph(
    "<b>SeguridadMaster</b> es una aplicación de escritorio WPF (.NET 8) para "
    "Windows que activa automáticamente un escudo de seguridad al iniciar sesión. "
    "Bloquea vectores de fuga de datos (USB, WiFi, FTP, RDP no autorizado), "
    "restringe combinaciones de teclas del sistema y lanza la aplicación supervisora "
    "<i>SuperVisor.WPF</i> de Datec. Todo se restaura al presionar la combinación "
    "secreta de desbloqueo.",
    body_style
))
story.append(Spacer(1, 0.3*cm))

# ── 2. REQUISITOS PREVIOS ───────────────────────────────────────────────────
story.append(section_title("REQUISITOS PREVIOS", 2))
story.append(req_table())
story.append(Spacer(1, 0.3*cm))
story.append(info_box(
    "Si .NET 8 Desktop Runtime no está instalado, descárguelo desde "
    "<b>https://dotnet.microsoft.com/download/dotnet/8.0</b> y elija "
    "<i>Desktop Runtime</i> para Windows x64."
))
story.append(Spacer(1, 0.2*cm))
story.append(warning_box(
    "La aplicación supervisora <b>SuperVisor.WPF.exe</b> debe estar instalada en "
    r"C:\Program Files\Datec\SuperVisor\ antes de ejecutar SeguridadMaster, "
    "de lo contrario la activación del escudo fallará."
))
story.append(Spacer(1, 0.3*cm))

# ── 3. INSTALADOR ──────────────────────────────────────────────────────────
story.append(section_title("INSTALADOR", 3))
story.append(Paragraph(
    "SeguridadMaster se distribuye mediante el asistente de instalación "
    "<b>SeguridadMaster_Setup.exe</b>, generado con InnoSetup 6. "
    "El instalador empaqueta todos los archivos necesarios, verifica los "
    "prerrequisitos del sistema y registra el desinstalador en Windows automáticamente.",
    body_style
))
story.append(Spacer(1, 0.2*cm))
story.append(installer_table())
story.append(Spacer(1, 0.3*cm))
story.append(info_box(
    "El instalador verifica automáticamente si .NET 8.0 Desktop Runtime está presente. "
    "Si no lo detecta, muestra un mensaje y abre la página de descarga oficial de Microsoft "
    "antes de continuar con la instalación.",
    icon="ℹ"
))
story.append(Spacer(1, 0.3*cm))

# ── 4. INSTALACIÓN ─────────────────────────────────────────────────────────
story.append(section_title("INSTALACIÓN PASO A PASO", 4))
story.append(Paragraph(
    "La instalación se realiza mediante el asistente <b>SeguridadMaster_Setup.exe</b>. "
    "El proceso es guiado y no requiere configuración manual de archivos. "
    "Al finalizar, SeguridadMaster queda listo para ejecutarse desde el acceso directo "
    "creado en el Escritorio o el Menú Inicio.",
    body_style
))
story.append(Spacer(1, 0.25*cm))

steps = [
    ("<b>Verificar prerrequisitos:</b> Confirme que <b>.NET 8 Desktop Runtime</b> está "
     "instalado en el equipo destino y que <font name='Courier'>SuperVisor.WPF.exe</font> "
     r"se encuentra en <font name='Courier'>C:\Program Files\Datec\SuperVisor\</font>. "
     "Si .NET 8 no está instalado, el instalador lo detectará automáticamente en el paso siguiente."),
    ("<b>Ejecutar el instalador como Administrador:</b> Haga <b>clic derecho</b> sobre "
     "<font name='Courier'>SeguridadMaster_Setup.exe</font> y seleccione "
     "<b>\"Ejecutar como administrador\"</b>. Acepte el diálogo de Control de Cuentas "
     "de Usuario (UAC) haciendo clic en <b>Sí</b>."),
    ("<b>Verificación de .NET 8:</b> Si el runtime no está instalado, el asistente mostrará "
     "un aviso y abrirá automáticamente la página de descarga de Microsoft. "
     "Instale el <b>.NET 8 Desktop Runtime (x64)</b> y vuelva a ejecutar el instalador."),
    ("<b>Pantalla de bienvenida:</b> Haga clic en <b>Siguiente</b> para continuar con el asistente."),
    ("<b>Seleccionar carpeta de instalación:</b> La carpeta predeterminada es "
     r"<font name='Courier'>C:\Program Files\SeguridadMaster\</font>. "
     "Puede mantener el valor predeterminado o elegir otra ubicación. Haga clic en <b>Siguiente</b>."),
    ("<b>Seleccionar accesos directos:</b> Marque las opciones deseadas: "
     "<i>Crear acceso directo en el Escritorio</i> y/o <i>Crear acceso directo en el Menú Inicio</i>. "
     "Haga clic en <b>Siguiente</b>."),
    ("<b>Confirmar e instalar:</b> Revise el resumen y haga clic en <b>Instalar</b>. "
     "El asistente copiará todos los archivos y registrará el desinstalador en Windows."),
    ("<b>Finalizar:</b> Al terminar, puede marcar <i>\"Iniciar SeguridadMaster ahora\"</i> "
     "y hacer clic en <b>Finalizar</b>. En el primer arranque, la aplicación registra "
     "automáticamente la tarea programada <font name='Courier'>SeguridadMaster_AutoStart</font> "
     "para iniciar con privilegios de Administrador en cada inicio de sesión."),
    ("<b>Verificar el estado:</b> La ventana principal muestra indicadores LED de estado "
     "para cada componente del escudo (Registro, Firewall, WiFi, Hook). "
     "Tras 2 segundos el escudo se activa y la barra de progreso debe alcanzar el 100%."),
]

for i, text in enumerate(steps, 1):
    story.append(step_row(i, text))
    story.append(Spacer(1, 0.15*cm))

story.append(Spacer(1, 0.1*cm))
story.append(info_box(
    "En ejecuciones posteriores, si la tarea programada ya está registrada, "
    "el sistema la omite y procede directamente con la activación del escudo.",
    icon="✓"
))
story.append(Spacer(1, 0.3*cm))

# ── 5. DESBLOQUEO ──────────────────────────────────────────────────────────
story.append(section_title("DESBLOQUEO DEL SISTEMA", 5))
story.append(Paragraph(
    "Para desactivar el escudo y restaurar el sistema al estado normal, "
    "utilice la combinación de teclas secreta:",
    body_style
))
story.append(Spacer(1, 0.2*cm))

# Cuadro combinación de teclas
combo_data = [[
    Paragraph("<b>Ctrl</b>", ParagraphStyle("K", parent=styles["Normal"],
        fontSize=14, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_CENTER)),
    Paragraph("+", ParagraphStyle("P", parent=styles["Normal"],
        fontSize=16, fontName="Helvetica-Bold", textColor=DARK_BLUE, alignment=TA_CENTER)),
    Paragraph("<b>Shift</b>", ParagraphStyle("K", parent=styles["Normal"],
        fontSize=14, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_CENTER)),
    Paragraph("+", ParagraphStyle("P", parent=styles["Normal"],
        fontSize=16, fontName="Helvetica-Bold", textColor=DARK_BLUE, alignment=TA_CENTER)),
    Paragraph("<b>Alt</b>", ParagraphStyle("K", parent=styles["Normal"],
        fontSize=14, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_CENTER)),
    Paragraph("+", ParagraphStyle("P", parent=styles["Normal"],
        fontSize=16, fontName="Helvetica-Bold", textColor=DARK_BLUE, alignment=TA_CENTER)),
    Paragraph("<b>K</b>", ParagraphStyle("K", parent=styles["Normal"],
        fontSize=14, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_CENTER)),
]]
combo_t = Table(combo_data, colWidths=[2.5*cm, 0.8*cm, 2.5*cm, 0.8*cm, 2.5*cm, 0.8*cm, 2.5*cm])
combo_t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (0,0), DARK_BLUE),
    ("BACKGROUND", (2,0), (2,0), DARK_BLUE),
    ("BACKGROUND", (4,0), (4,0), DARK_BLUE),
    ("BACKGROUND", (6,0), (6,0), MED_BLUE),
    ("TOPPADDING", (0,0), (-1,-1), 10),
    ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ("BOX", (0,0), (0,0), 1, colors.white),
    ("BOX", (2,0), (2,0), 1, colors.white),
    ("BOX", (4,0), (4,0), 1, colors.white),
    ("BOX", (6,0), (6,0), 1, colors.white),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
]))
story.append(combo_t)
story.append(Spacer(1, 0.25*cm))

story.append(Paragraph(
    "Al presionar la combinación, la aplicación realizará las siguientes acciones de forma automática:",
    body_style
))
unlock_steps = [
    "Detiene el hook de teclado global.",
    "Muestra la ventana de notificación de desbloqueo.",
    "Termina el proceso <font name='Courier'>SuperVisor.WPF.exe</font>.",
    "Restaura el acceso USB (rehabilita USBSTOR y elimina políticas GPO).",
    "Elimina las reglas de firewall RDP y FTP creadas por SeguridadMaster.",
    "Reactiva los adaptadores WiFi deshabilitados.",
    "Relanza <font name='Courier'>explorer.exe</font> si no está en ejecución.",
    "Cierra SeguridadMaster.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(s, body_style), leftIndent=20, bulletColor=MED_BLUE) for s in unlock_steps],
    bulletType="bullet",
    leftIndent=10,
))
story.append(Spacer(1, 0.3*cm))

# ── 6. DESINSTALACIÓN ──────────────────────────────────────────────────────
story.append(section_title("DESINSTALACIÓN", 6))
story.append(Paragraph(
    "El instalador registra automáticamente un desinstalador en Windows. "
    "La forma recomendada de desinstalar es a través del Panel de Control:",
    body_style
))
story.append(Spacer(1, 0.15*cm))

desinst = [
    ("Desinstalar desde Windows",
     "Abra <b>Panel de Control → Programas → Programas y características</b>, localice "
     "<b>SeguridadMaster</b> en la lista, haga clic derecho y seleccione <b>Desinstalar</b>. "
     "Alternativamente: <b>Configuración → Aplicaciones → SeguridadMaster → Desinstalar</b>. "
     "El desinstalador eliminará todos los archivos de programa y los accesos directos creados."),
    ("Eliminar la tarea programada",
     "Abra el <b>Programador de Tareas</b> de Windows (<font name='Courier'>taskschd.msc</font>), "
     "localice la tarea <font name='Courier'>SeguridadMaster_AutoStart</font> en la carpeta raíz "
     "y elimínela. Esta tarea es creada por la aplicación en el primer arranque y no la elimina el desinstalador."),
    ("Eliminar reglas de firewall residuales",
     "Si el sistema no fue desbloqueado correctamente antes de desinstalar, ejecute desde "
     "una consola de administrador:<br/>"
     "<font name='Courier'>netsh advfirewall firewall delete rule name=\"SeguridadMaster_RDP_Restricted\"</font><br/>"
     "<font name='Courier'>netsh advfirewall firewall delete rule name=\"SeguridadMaster_Block_FTP\"</font>"),
    ("Restaurar USB si es necesario",
     "Si el USB quedó bloqueado, ejecute desde una consola de administrador:<br/>"
     "<font name='Courier'>reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\USBSTOR /v Start /t REG_DWORD /d 3 /f</font>"),
]

for i, (title, desc) in enumerate(desinst, 1):
    row_data = [[
        Paragraph(f"<b>{i}. {title}</b>", subsection_style),
        Paragraph(desc, body_style),
    ]]
    t = Table(row_data, colWidths=[4.5*cm, 11*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), GRAY_BG),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0,0), (-1,-1), 0.4, colors.HexColor("#e2e8f0")),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.12*cm))

story.append(Spacer(1, 0.2*cm))

# ── 7. RESUMEN DE FUNCIONES ─────────────────────────────────────────────────
story.append(section_title("RESUMEN DE FUNCIONES DEL ESCUDO", 7))
story.append(features_table())
story.append(Spacer(1, 0.3*cm))

# ── 8. SOLUCIÓN DE PROBLEMAS ────────────────────────────────────────────────
story.append(section_title("SOLUCIÓN DE PROBLEMAS", 8))

problems = [
    (
        "El instalador no inicia o pide permisos",
        "Asegúrese de ejecutar <font name='Courier'>SeguridadMaster_Setup.exe</font> con "
        "<b>clic derecho → Ejecutar como administrador</b> y aceptar el diálogo UAC. "
        "Sin privilegios de Administrador la instalación no puede completarse."
    ),
    (
        "Error al activar el escudo",
        "Verifique que <font name='Courier'>SuperVisor.WPF.exe</font> existe en "
        r"<font name='Courier'>C:\Program Files\Datec\SuperVisor\</font>. "
        "Si la ruta es diferente, contacte al equipo de Datec."
    ),
    (
        "El WiFi no se deshabilita",
        "Confirme que el adaptador inalámbrico tiene en su descripción las palabras "
        "<i>Wireless</i> o <i>Wi-Fi</i>. Algunos adaptadores USB pueden no ser detectados."
    ),
    (
        "La combinación Ctrl+Shift+Alt+K no responde",
        "Asegúrese de que el escudo está completamente activado (barra de progreso al 100%). "
        "Pruebe en el escritorio, no dentro de otra aplicación en pantalla completa."
    ),
    (
        "El USB sigue bloqueado tras el desbloqueo",
        "Ejecute manualmente desde consola de administrador:<br/>"
        "<font name='Courier'>sc start USBSTOR</font><br/>"
        "<font name='Courier'>gpupdate /force</font>"
    ),
    (
        ".NET 8 Runtime no encontrado",
        "Descargue e instale <b>.NET 8 Desktop Runtime (x64)</b> desde el sitio oficial de Microsoft "
        "antes de ejecutar SeguridadMaster."
    ),
]

prob_data = [[Paragraph("<b>Problema</b>", body_style), Paragraph("<b>Solución</b>", body_style)]]
for p, s in problems:
    prob_data.append([Paragraph(p, body_style), Paragraph(s, body_style)])

pt = Table(prob_data, colWidths=[5.5*cm, 10*cm])
pt.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), DARK_BLUE),
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),
    ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, GRAY_BG]),
    ("BOX", (0,0), (-1,-1), 0.8, colors.HexColor("#94a3b8")),
    ("INNERGRID", (0,0), (-1,-1), 0.4, colors.HexColor("#cbd5e1")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("LEFTPADDING", (0,0), (-1,-1), 8),
]))
story.append(pt)
story.append(Spacer(1, 0.4*cm))

# ── FOOTER ──────────────────────────────────────────────────────────────────
story.append(hr(DARK_BLUE, 1))
story.append(Paragraph(
    "SeguridadMaster  ·  Datec  ·  Documento de uso interno  ·  "
    + datetime.today().strftime("%Y"),
    footer_style
))

# ── GENERAR PDF ─────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF generado: {OUTPUT}")
