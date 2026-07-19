#!/usr/bin/env python3
"""
ASTC Optimizer - Convierte PNG a ASTC con interfaz de consola interactiva.
by Ari - https://github.com/Ari-Aguilar/astc-optimizer
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# ─────────────────────────────────────────────
#  COLORES ANSI
# ─────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"

    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GRAY    = "\033[37m"
    DARK    = "\033[90m"

    # Fondo oscuro para highlight de selección
    SEL_BG  = "\033[48;5;236m"
    SEL_FG  = "\033[97m"

def box(text, color=C.WHITE, width=50):
    """Dibuja un recuadro alrededor del texto."""
    border = color + "┌" + "─" * (width - 2) + "┐" + C.RESET
    pad    = color + "│" + C.RESET + " " * (width - 2) + color + "│" + C.RESET
    lines  = text.split("\n")
    result = [border, pad]
    for line in lines:
        visible_len = len(_strip_ansi(line))
        padding = width - 2 - visible_len - 2
        result.append(color + "│" + C.RESET + " " + line + " " * max(0, padding) + " " + color + "│" + C.RESET)
    result.append(pad)
    result.append(color + "└" + "─" * (width - 2) + "┘" + C.RESET)
    return "\n".join(result)

def _strip_ansi(text):
    import re
    return re.sub(r'\033\[[0-9;]*m', '', text)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_status(emoji, msg, color=C.GRAY):
    print(f" {C.DARK}[{C.RESET} {emoji} {C.DARK}]{C.RESET} {color}{msg}{C.RESET}")

def print_ok(msg):
    print_status("✅", msg, C.GREEN)

def print_err(msg):
    print_status("❌", msg, C.RED)

def print_warn(msg):
    print_status("⚠️ ", msg, C.YELLOW)

def print_info(msg):
    print_status("📂", msg, C.GRAY)

# ─────────────────────────────────────────────
#  ASCII ART TITLES
# ─────────────────────────────────────────────

ASCII_ASTC = r"""
  █████╗ ███████╗████████╗ ██████╗
 ██╔══██╗██╔════╝╚══██╔══╝██╔════╝
 ███████║███████╗   ██║   ██║
 ██╔══██║╚════██║   ██║   ██║
 ██║  ██║███████║   ██║   ╚██████╗
 ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝
  ██████╗ ██████╗ ████████╗
 ██╔═══██╗██╔══██╗╚══██╔══╝
 ██║   ██║██████╔╝   ██║
 ██║   ██║██╔═══╝    ██║
 ╚██████╔╝██║        ██║
  ╚═════╝ ╚═╝        ╚═╝
"""

ASCII_FOLDERS = r"""
 ███████╗ ██████╗ ██╗     ██████╗ ███████╗██████╗ ███████╗
 ██╔════╝██╔═══██╗██║     ██╔══██╗██╔════╝██╔══██╗██╔════╝
 █████╗  ██║   ██║██║     ██║  ██║█████╗  ██████╔╝███████╗
 ██╔══╝  ██║   ██║██║     ██║  ██║██╔══╝  ██╔══██╗╚════██║
 ██║     ╚██████╔╝███████╗██████╔╝███████╗██║  ██║███████║
 ╚═╝      ╚═════╝ ╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚══════╝
"""

ASCII_OPTIM = r"""
  ██████╗ ██████╗ ████████╗██╗███╗   ███╗
 ██╔═══██╗██╔══██╗╚══██╔══╝██║████╗ ████║
 ██║   ██║██████╔╝   ██║   ██║██╔████╔██║
 ██║   ██║██╔═══╝    ██║   ██║██║╚██╔╝██║
 ╚██████╔╝██║        ██║   ██║██║ ╚═╝ ██║
  ╚═════╝ ╚═╝        ╚═╝   ╚═╝╚═╝     ╚═╝
"""

ASCII_RESULT = r"""
 ██████╗ ███████╗███████╗██╗   ██╗██╗  ████████╗
 ██╔══██╗██╔════╝██╔════╝██║   ██║██║  ╚══██╔══╝
 ██████╔╝█████╗  ███████╗██║   ██║██║     ██║
 ██╔══██╗██╔══╝  ╚════██║██║   ██║██║     ██║
 ██║  ██║███████╗███████║╚██████╔╝███████╗██║
 ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝
"""

ASCII_ERROR = r"""
 ███████╗██████╗ ██████╗  ██████╗ ██████╗
 ██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
 █████╗  ██████╔╝██████╔╝██║   ██║██████╔╝
 ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗
 ███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║
 ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
"""

# ─────────────────────────────────────────────
#  DETECCIÓN DEL EJECUTABLE
# ─────────────────────────────────────────────

ENCODER_NAMES = ["astcenc", "astcenc-sse4.1", "astcenc-sse2", "astcenc-avx2", "astcenc-neon"]
DOWNLOAD_URL  = "https://github.com/ARM-software/astc-encoder/releases"

# Nombres de carpetas que pueden excluirse del escaneo (case-insensitive)
IGNORABLE_FOLDER_NAMES = {"icon", "icons"}

def _find_local_encoder(script_dir):
    """Busca el ejecutable junto al script o en el PATH."""
    # 1) Junto al script (con cualquier nombre conocido)
    for name in ENCODER_NAMES:
        local = script_dir / name
        if local.exists():
            return str(local)
        if os.name == "nt":
            local_exe = script_dir / (name + ".exe")
            if local_exe.exists():
                return str(local_exe)
    # 2) En el PATH del sistema
    for name in ENCODER_NAMES:
        try:
            result = subprocess.run(
                [name, "-version"],
                capture_output=True, text=True
            )
            if result.returncode == 0 or "astcenc" in (result.stdout + result.stderr).lower():
                return name
        except FileNotFoundError:
            continue
    return None

def check_encoder():
    """
    Devuelve el comando del encoder si está disponible, o None si no se encontró.
    """
    script_dir = Path(__file__).resolve().parent
    return _find_local_encoder(script_dir)


def _is_inside_ignored_folder(png_path, root_path):
    """Devuelve True si alguna carpeta del path relativo se llama icon/icons."""
    try:
        rel_parts = png_path.relative_to(root_path).parts[:-1]  # sin el nombre del archivo
    except ValueError:
        rel_parts = png_path.parts[:-1]
    for part in rel_parts:
        if part.lower() in IGNORABLE_FOLDER_NAMES:
            return True
    return False


def screen_no_encoder(missing_name="astcenc"):
    """Pantalla de error: encoder no detectado."""
    clear()

    for line in ASCII_ERROR.split("\n"):
        print(C.RED + C.BOLD + line + C.RESET)

    print(f"  {C.GRAY}No se detectó el ejecutable del compresor{C.RESET}")
    print()

    # Panel de error
    print(f"  {C.RED}┌─ ❌  No se detectó: {C.WHITE}{missing_name}{C.RED} {'─' * (30 - len(missing_name))}┐{C.RESET}")
    print(f"  {C.RED}│{C.RESET}  {C.YELLOW}El compresor ASTC no fue encontrado en el PATH          {C.RED}│{C.RESET}")
    print(f"  {C.RED}│{C.RESET}  {C.YELLOW}ni junto a este script.                                 {C.RED}│{C.RESET}")
    print(f"  {C.RED}└──────────────────────────────────────────────────────────┘{C.RESET}")
    print()

    # Panel solución
    print(f"  {C.CYAN}┌─ 🛠️  Solución ───────────────────────────────────────────┐{C.RESET}")
    print(f"  {C.CYAN}│{C.RESET}")

    steps = [
        ("📥", "Descargar ASTC Encoder:",     f"{C.CYAN}{DOWNLOAD_URL}{C.RESET}"),
        ("📦", "Descomprimir el archivo",      f"{C.DARK}extrae el .zip / .tar.gz descargado{C.RESET}"),
        ("🔍", "Dentro de la carpeta bin/",    f"{C.DARK}encontrarás los ejecutables{C.RESET}"),
        ("✏️ ", "Renombrar el ejecutable a:",  f"{C.WHITE}astcenc{C.RESET}{C.DARK}  (ej: astcenc-sse4.1 → astcenc){C.RESET}"),
        ("📂", "Mover junto a este script:",   f"{C.DARK}en la misma carpeta que {C.WHITE}png_to_astc.py{C.RESET}"),
        ("🚀", "Volver a ejecutar el script",  f"{C.DARK}y selecciona 'Iniciar Optimización'{C.RESET}"),
    ]

    for emoji, label, detail in steps:
        print(f"  {C.CYAN}│{C.RESET}  {C.DARK}[{C.RESET} {emoji} {C.DARK}]{C.RESET}  {C.WHITE}{label}{C.RESET}")
        print(f"  {C.CYAN}│{C.RESET}         {detail}")
        print(f"  {C.CYAN}│{C.RESET}")

    # Nota Windows
    print(f"  {C.CYAN}│{C.RESET}  {C.DARK}──────────────────────────────────────────────────{C.RESET}")
    print(f"  {C.CYAN}│{C.RESET}  {C.DARK}[{C.RESET} 🪟 {C.DARK}]{C.RESET}  {C.GRAY}Windows: renombra a {C.WHITE}astcenc.exe{C.RESET}")
    print(f"  {C.CYAN}│{C.RESET}  {C.DARK}[{C.RESET} 🐧 {C.DARK}]{C.RESET}  {C.GRAY}Linux/Mac: ejecuta {C.WHITE}chmod +x astcenc{C.RESET}")
    print(f"  {C.CYAN}│{C.RESET}")
    print(f"  {C.CYAN}└──────────────────────────────────────────────────────────┘{C.RESET}")
    print()

    opts = ["🔄  Reintentar detección", "🚪  Salir"]
    _print_options_initial(opts, C.RED)
    choice = arrow_select(opts, color_active=C.RED)
    return choice


# ─────────────────────────────────────────────
#  SELECCIÓN CON FLECHAS
# ─────────────────────────────────────────────

if os.name == "nt":
    import msvcrt

    def _getch():
        ch = msvcrt.getwch()
        if ch in ('\x00', '\xe0'):
            ch2 = msvcrt.getwch()
            if ch2 == 'H': return 'UP'
            if ch2 == 'P': return 'DOWN'
            if ch2 == 'M': return 'RIGHT'
            if ch2 == 'K': return 'LEFT'
        if ch == '\r': return 'ENTER'
        return ch
else:
    import tty, termios

    def _getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A': return 'UP'
                    if ch3 == 'B': return 'DOWN'
                    if ch3 == 'C': return 'RIGHT'
                    if ch3 == 'D': return 'LEFT'
            if ch in ('\r', '\n'): return 'ENTER'
            if ch == '\x03': raise KeyboardInterrupt
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def arrow_select(options, prompt="", start=0, color_active=C.CYAN):
    """
    Muestra una lista de opciones navegables con flechas.
    Devuelve el índice seleccionado.
    """
    idx = start
    n   = len(options)

    while True:
        # Redibujar opciones
        sys.stdout.write(f"\033[{n}A")  # subir n líneas
        for i, opt in enumerate(options):
            if i == idx:
                line = f"  {color_active}▶  {opt}{C.RESET}"
            else:
                line = f"  {C.DARK}   {C.GRAY}{opt}{C.RESET}"
            print(line + " " * 10)

        key = _getch()
        if key == 'UP':
            idx = (idx - 1) % n
        elif key == 'DOWN':
            idx = (idx + 1) % n
        elif key == 'ENTER':
            return idx


def _print_options_initial(options, color_active=C.CYAN):
    """Imprime las opciones por primera vez."""
    for i, opt in enumerate(options):
        if i == 0:
            print(f"  {color_active}▶  {opt}{C.RESET}")
        else:
            print(f"  {C.DARK}   {C.GRAY}{opt}{C.RESET}")

# ─────────────────────────────────────────────
#  PANTALLAS
# ─────────────────────────────────────────────

def screen_main():
    """Pantalla principal."""
    clear()

    # ASCII title en ROJO con borde
    for line in ASCII_ASTC.split("\n"):
        print(C.RED + C.BOLD + line + C.RESET)

    print()
    print(f"  {C.GRAY}Optimizador de texturas PNG → ASTC{C.RESET}")
    print()
    print_status("🚀", f"GITHUB: {C.CYAN}https://github.com/Ari-Aguilar/astc-optimizer{C.RESET}", C.DARK)
    print()

    # Advertencias
    print(f"  {C.RED}┌─ ⚠️  ADVERTENCIAS ──────────────────────────────────────┐{C.RESET}")
    print(f"  {C.RED}│{C.RESET}  {C.YELLOW}Este script ELIMINA los PNG originales de forma        {C.RED}│{C.RESET}")
    print(f"  {C.RED}│{C.RESET}  {C.YELLOW}permanente. Haz una copia de seguridad antes.          {C.RED}│{C.RESET}")
    print(f"  {C.RED}│{C.RESET}  {C.YELLOW}La compresión ASTC puede generar artefactos visuales.  {C.RED}│{C.RESET}")
    print(f"  {C.RED}└──────────────────────────────────────────────────────────┘{C.RESET}")
    print()

    opts = [
        "🔥  Iniciar Optimización",
        "📂  Moverme a otra localización",
        "🚪  Salir",
    ]
    _print_options_initial(opts, C.RED)
    choice = arrow_select(opts, color_active=C.RED)
    return choice


def screen_folder(current_path=None):
    """Pantalla para cambiar de carpeta."""
    clear()

    for line in ASCII_FOLDERS.split("\n"):
        print(C.GREEN + C.BOLD + line + C.RESET)

    print(f"  {C.GRAY}Moverme a otra localización{C.RESET}")
    print()

    if current_path:
        print_status("📍", f"Localización actual: {C.CYAN}{current_path}{C.RESET}", C.DARK)
        print()

    print(f"  {C.DARK}[ {C.RESET}📂{C.DARK} ]{C.RESET} {C.GRAY}Nueva localización:{C.RESET}")
    print(f"  {C.DARK}    Ej. {C.DARK}/home/ari/proyectos/mi_mod/textures{C.RESET}")
    print()
    sys.stdout.write(f"  {C.CYAN}▶  {C.WHITE}")
    sys.stdout.flush()

    # Volver a modo normal para leer input
    if os.name != "nt":
        import termios, tty
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    path_input = input("").strip()
    print(C.RESET, end="")

    if not path_input:
        return current_path or Path(".").resolve()
    return Path(path_input).expanduser().resolve()


def screen_ignore_icons():
    """Pregunta si se deben ignorar las carpetas icon/icons."""
    print(f"  {C.CYAN}┌─ Ignorar carpetas de íconos ─────────────────────────────┐{C.RESET}")
    print(f"  {C.CYAN}│{C.RESET}  {C.DARK}¿Quieres excluir carpetas llamadas {C.WHITE}icon{C.DARK}/{C.WHITE}icons{C.DARK}?{C.RESET}")
    print(f"  {C.CYAN}└──────────────────────────────────────────────────────────┘{C.RESET}")
    print()

    opts = [
        "🚫  Sí, ignorar carpetas icon/icons",
        "✅  No, incluir todos los PNG",
    ]
    _print_options_initial(opts, C.CYAN)
    choice = arrow_select(opts, color_active=C.CYAN)
    print()
    return choice == 0


def screen_optimize(root_path):
    """Pantalla de optimización: escaneo + selección de opciones."""
    clear()

    for line in ASCII_OPTIM.split("\n"):
        print(C.BLUE + C.BOLD + line + C.RESET)

    print(f"  {C.GRAY}Resultado del escaneo{C.RESET}")
    print()

    # Escanear PNGs
    root_path = Path(root_path)
    if not root_path.exists():
        print_err(f"El directorio no existe: {root_path}")
        time.sleep(2)
        return None, None, None

    png_files = list(root_path.rglob("*.png"))

    if not png_files:
        print_warn("No se encontraron archivos PNG en la ruta especificada.")
        time.sleep(2)
        return None, None, None

    print(f"  {C.DARK}[{C.RESET} {C.YELLOW}!{C.RESET} {C.DARK}]{C.RESET}  {C.WHITE}Encontrados {C.YELLOW}{len(png_files)}{C.WHITE} archivos PNG{C.RESET}")
    print()

    # ── Ignorar carpetas icon/icons ─────────────────────────
    ignore_icons = screen_ignore_icons()

    if ignore_icons:
        before = len(png_files)
        png_files = [p for p in png_files if not _is_inside_ignored_folder(p, root_path)]
        excluded = before - len(png_files)

        print_status("🚫", f"Excluidos por carpeta icon/icons: {C.YELLOW}{excluded}{C.RESET}", C.DARK)
        print(f"  {C.DARK}[{C.RESET} {C.WHITE}✓{C.RESET} {C.DARK}]{C.RESET}  {C.WHITE}Quedan {C.YELLOW}{len(png_files)}{C.WHITE} archivos PNG para convertir{C.RESET}")
        print()

        if not png_files:
            print_warn("No quedan archivos PNG tras excluir icon/icons.")
            time.sleep(2)
            return None, None, None

    # ── Seleccionar resolución ──────────────────────────────
    print(f"  {C.CYAN}┌─ Seleccionar Resolución (bloque) ───────────────────────┐{C.RESET}")
    print(f"  {C.CYAN}│{C.RESET}  {'Tamaño':<8}{'Calidad':<16}{'Compresión':<14}{'Uso Recomendado'}{C.CYAN}  │{C.RESET}")
    print(f"  {C.CYAN}│{C.RESET}  {'─'*60}{C.CYAN}  │{C.RESET}")
    block_opts = [
        ("4x4",   "⭐⭐⭐⭐⭐", "🔵🔵",      "Texturas UI / importantes"),
        ("6x6",   "⭐⭐⭐⭐ ", "🔵🔵🔵",    "Balance general ✅"),
        ("8x8",   "⭐⭐⭐  ",  "🔵🔵🔵🔵",  "Fondos / efectos"),
        ("12x12", "⭐⭐   ",   "🔵🔵🔵🔵🔵","Máxima compresión"),
    ]
    for b in block_opts:
        print(f"  {C.CYAN}│{C.RESET}  {C.WHITE}{b[0]:<8}{C.RESET}{b[1]:<16}{b[2]:<14}{C.DARK}{b[3]}{C.RESET}{C.CYAN}  │{C.RESET}")
    print(f"  {C.CYAN}└──────────────────────────────────────────────────────────┘{C.RESET}")
    print()

    block_labels = [f"{b[0]}  {b[1]}  {b[2]}  {b[3]}" for b in block_opts]
    _print_options_initial(block_labels, C.CYAN)
    block_choice = arrow_select(block_labels, color_active=C.CYAN)
    chosen_block = block_opts[block_choice][0]

    print()

    # ── Seleccionar calidad ─────────────────────────────────
    print(f"  {C.CYAN}┌─ Seleccionar Calidad ────────────────────────────────────┐{C.RESET}")
    quality_opts = [
        ("veryfast",  "Conversión rápida, menor calidad final"),
        ("fast",      "Rápido con calidad aceptable"),
        ("medium",    "Balance entre velocidad y calidad"),
        ("thorough",  "Buena calidad, velocidad aceptable ✅"),
        ("exhaustive","Mejor calidad posible, muy lento"),
    ]
    for q in quality_opts:
        print(f"  {C.CYAN}│{C.RESET}  {C.WHITE}{q[0]:<14}{C.RESET}{C.DARK}{q[1]}{C.RESET}")
    print(f"  {C.CYAN}└──────────────────────────────────────────────────────────┘{C.RESET}")
    print()

    quality_labels = [f"{q[0]:<14}  {q[1]}" for q in quality_opts]
    _print_options_initial(quality_labels, C.CYAN)
    quality_choice = arrow_select(quality_labels, color_active=C.CYAN)
    chosen_quality = quality_opts[quality_choice][0]

    return png_files, chosen_block, chosen_quality


def screen_converting(png_files, block_size, quality, encoder_cmd):
    """Ejecuta la conversión y muestra progreso."""
    clear()

    for line in ASCII_OPTIM.split("\n"):
        print(C.BLUE + C.BOLD + line + C.RESET)

    print(f"  {C.GRAY}Convirtiendo archivos...{C.RESET}")
    print()
    print_status("⚙️ ", f"Bloque: {C.CYAN}{block_size}{C.RESET}  Calidad: {C.CYAN}{quality}{C.RESET}", C.DARK)
    print_status("🔧", f"Encoder: {C.CYAN}{encoder_cmd}{C.RESET}", C.DARK)
    print()

    success = 0
    fail    = 0
    total   = len(png_files)

    for i, png_path in enumerate(png_files, 1):
        png_file  = Path(png_path)
        astc_file = png_file.with_suffix('.astc')

        bar_done  = int((i / total) * 30)
        bar       = C.CYAN + "█" * bar_done + C.DARK + "░" * (30 - bar_done) + C.RESET
        pct       = int((i / total) * 100)

        sys.stdout.write(f"\r  {C.DARK}[{C.RESET}{bar}{C.DARK}]{C.RESET} {C.WHITE}{pct:>3}%{C.RESET}  {C.DARK}{png_file.name[:40]}{C.RESET}   ")
        sys.stdout.flush()

        try:
            cmd = [
                encoder_cmd, '-cl',
                str(png_file), str(astc_file),
                block_size, f'-{quality}'
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0 and astc_file.exists() and astc_file.stat().st_size > 0:
                png_file.unlink()
                success += 1
            else:
                fail += 1

        except Exception:
            fail += 1

    print(f"\r  {C.DARK}[{C.RESET}{C.GREEN}{'█' * 30}{C.DARK}]{C.RESET} {C.GREEN}100%{C.RESET}  {C.DARK}Completado{'  ' * 20}{C.RESET}")
    print()

    return success, fail


def screen_results(success, fail):
    """Pantalla de resultados finales."""
    clear()

    for line in ASCII_RESULT.split("\n"):
        print(C.MAGENTA + C.BOLD + line + C.RESET)

    print(f"  {C.GRAY}¡Felicidades, convertido!{C.RESET}")
    print()

    print_status("✅", f"Convertidos: {C.GREEN}{success}{C.RESET}", C.DARK)
    print_status("❌", f"Errores:     {C.RED}{fail}{C.RESET}", C.DARK)
    print()

    opts = [
        "📂  Moverme a otra carpeta",
        "🚪  Salir",
    ]
    _print_options_initial(opts, C.MAGENTA)
    choice = arrow_select(opts, color_active=C.MAGENTA)
    return choice


# ─────────────────────────────────────────────
#  FLUJO PRINCIPAL
# ─────────────────────────────────────────────

def main():
    current_path = Path(".").resolve()

    # ── Verificar encoder al arrancar ──────────
    encoder_cmd = check_encoder()
    while encoder_cmd is None:
        choice = screen_no_encoder("astcenc")
        if choice == 0:
            # Reintentar
            encoder_cmd = check_encoder()
        else:
            clear()
            print_ok("¡Hasta luego!")
            print()
            sys.exit(0)

    while True:
        try:
            choice = screen_main()

            if choice == 0:
                # Verificar encoder de nuevo (pudo moverse)
                encoder_cmd = check_encoder()
                if encoder_cmd is None:
                    retry = screen_no_encoder("astcenc")
                    if retry == 1:
                        clear(); print_ok("¡Hasta luego!"); print(); sys.exit(0)
                    continue

                result = screen_optimize(current_path)
                png_files, block_size, quality = result

                if png_files is None:
                    continue

                success, fail = screen_converting(png_files, block_size, quality, encoder_cmd)
                post = screen_results(success, fail)

                if post == 0:
                    current_path = screen_folder(current_path)
                else:
                    clear()
                    print_ok("¡Hasta luego!")
                    print()
                    sys.exit(0)

            elif choice == 1:
                current_path = screen_folder(current_path)

            elif choice == 2:
                clear()
                print_ok("¡Hasta luego!")
                print()
                sys.exit(0)

        except KeyboardInterrupt:
            clear()
            print_warn("Operación cancelada por el usuario.")
            print()
            sys.exit(0)


if __name__ == "__main__":
    main()
