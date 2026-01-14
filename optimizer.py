#!/usr/bin/env python3
"""
Script para convertir archivos PNG a ASTC y eliminar los PNG originales
Busca recursivamente en todas las subcarpetas, by Ari.
"""

import os
import subprocess
import sys
from pathlib import Path

def convert_png_to_astc(png_path, block_size="6x6", quality="thorough"):
    """
    Convierte un archivo PNG a ASTC
    
    Args:
        png_path: Ruta al archivo PNG
        block_size: Tamaño de bloque ASTC (4x4, 6x6, 8x8, etc.)
        quality: Calidad de compresión (veryfast, fast, medium, thorough, exhaustive)
    """
    png_file = Path(png_path)
    astc_file = png_file.with_suffix('.astc')
    
    print(f"Convirtiendo: {png_file}")
    
    try:
        # Comando para astcenc
        cmd = [
            'astcenc',
            '-cl',  # Usar compresión
            str(png_file),
            str(astc_file),
            block_size,
            f'-{quality}'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✓ Creado: {astc_file}")
            
            # Verificar que el archivo ASTC se creó correctamente
            if astc_file.exists() and astc_file.stat().st_size > 0:
                # Eliminar el PNG original
                png_file.unlink()
                print(f"✓ Eliminado: {png_file}")
                return True
            else:
                print(f"✗ Error: El archivo ASTC no se creó correctamente")
                return False
        else:
            print(f"✗ Error al convertir {png_file}")
            print(f"  {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("✗ Error: astcenc no está instalado")
        print("  Instálalo con: sudo dnf install astc-encoder")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error inesperado: {e}")
        return False

def find_and_convert_pngs(root_dir=".", block_size="6x6", quality="thorough"):
    """
    Busca recursivamente todos los archivos PNG y los convierte a ASTC
    
    Args:
        root_dir: Directorio raíz donde buscar
        block_size: Tamaño de bloque ASTC
        quality: Calidad de compresión
    """
    root_path = Path(root_dir).resolve()
    
    if not root_path.exists():
        print(f"✗ Error: El directorio {root_path} no existe")
        sys.exit(1)
    
    # Buscar todos los archivos PNG recursivamente
    png_files = list(root_path.rglob("*.png"))
    
    if not png_files:
        print(f"No se encontraron archivos PNG en {root_path}")
        return
    
    print(f"\nEncontrados {len(png_files)} archivos PNG")
    print(f"Directorio: {root_path}")
    print(f"Configuración: {block_size}, calidad {quality}\n")
    
    # Confirmar antes de proceder
    respuesta = input("¿Continuar con la conversión? (s/n): ")
    if respuesta.lower() != 's':
        print("Operación cancelada")
        return
    
    print("\nIniciando conversión...\n")
    
    success_count = 0
    fail_count = 0
    
    for png_file in png_files:
        if convert_png_to_astc(png_file, block_size, quality):
            success_count += 1
        else:
            fail_count += 1
        print()  # Línea en blanco entre conversiones
    
    print("=" * 50)
    print(f"Conversión completada:")
    print(f"  ✓ Exitosas: {success_count}")
    print(f"  ✗ Fallidas: {fail_count}")
    print("=" * 50)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convierte archivos PNG a ASTC recursivamente"
    )
    parser.add_argument(
        "directorio",
        nargs="?",
        default=".",
        help="Directorio donde buscar archivos PNG (default: directorio actual)"
    )
    parser.add_argument(
        "-b", "--block-size",
        default="6x6",
        help="Tamaño de bloque ASTC (default: 6x6). Opciones: 4x4, 5x5, 6x6, 8x8, 10x10, 12x12"
    )
    parser.add_argument(
        "-q", "--quality",
        default="thorough",
        choices=["veryfast", "fast", "medium", "thorough", "exhaustive"],
        help="Calidad de compresión (default: thorough)"
    )
    
    args = parser.parse_args()
    
    find_and_convert_pngs(args.directorio, args.block_size, args.quality)