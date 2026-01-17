# astc-optimizer

Un script de Python que convierte automáticamente archivos PNG a formato ASTC comprimido para mejorar el rendimiento y reducir el tamaño de tus mods.

## ⚠️ Advertencias Importantes

> **🔴 ESTE SCRIPT ELIMINA TUS ARCHIVOS PNG ORIGINALES**

- Los archivos PNG serán reemplazados permanentemente por archivos `.astc` comprimidos
- **HAZ UNA COPIA DE SEGURIDAD** de tu mod antes de ejecutar este script
- Esta acción es **IRREVERSIBLE** - no podrás recuperar los PNG originales
- **NO ME HAGO RESPONSABLE POR PÉRDIDAS DE DATOS**

> **📉 Sobre la calidad**

- La compresión ASTC reduce la calidad visual de las imágenes
- Pueden verse pixeladas o con artefactos de compresión
- Es el compromiso necesario para obtener mejor rendimiento

---

## 📋 Requisitos Previos

### 1. Instalar ASTC Encoder

1. Descarga [ASTC Encoder](https://github.com/ARM-software/astc-encoder/releases) desde las releases oficiales
2. Descomprime el archivo descargado
3. Encontrarás 3 ejecutables en la carpeta `bin/`:
   - `astcenc-avx2` (CPUs modernas con AVX2)
   - `astcenc-sse4.1` ⭐ **RECOMENDADO** (mejor compatibilidad)
   - `astcenc-sse2` (CPUs antiguas)

### 2. Configurar ASTC Encoder en el PATH

Dependiendo de tu sistema operativo:

#### 🐧 Linux / MacOS

```bash
cd ~/Descargas/astcenc-X.X.X-linux-x64/bin

# Dale permisos de ejecución
chmod +x astcenc-sse4.1

# Cópialo al PATH del sistema
sudo cp astcenc-sse4.1 /usr/local/bin/astcenc
```

#### 🪟 Windows

1. Renombra `astcenc-sse4.1.exe` a `astcenc.exe`
2. Mueve el archivo a `C:\Windows\System32\` o agrega su ubicación al PATH del sistema

### 3. Verificar la instalación

Abre una terminal/CMD y ejecuta:

```bash
astcenc -version
```

Deberías ver algo como:

```
astcenc v5.3.0, 64-bit sse4.1+popcnt
Copyright (c) 2011-2025 Arm Limited. All rights reserved.
```

Si ves este mensaje, ¡estás listo! ✅

---

## 🚀 Uso del Script

### Instalación

1. Descarga `png_to_astc.py` y colócalo en la carpeta raíz de tu mod:

```
tu_mod/
├── png_to_astc.py  ← Aquí
├── textures/
│   └── items/
│       └── espada.png
└── sounds/
```

2. Dale permisos de ejecución (solo en Linux/MacOS):

```bash
chmod +x png_to_astc.py
```

### Ejecución Básica

Abre una terminal en la carpeta de tu mod y ejecuta:

```bash
python png_to_astc.py
```

El script buscará **recursivamente** todos los archivos `.png` en la carpeta actual y subcarpetas.

### Opciones Avanzadas

```bash
# Convertir PNGs en una carpeta específica
python png_to_astc.py textures/

# Cambiar el tamaño de bloque (afecta calidad vs compresión)
python png_to_astc.py -b 4x4    # Mejor calidad, archivos más grandes
python png_to_astc.py -b 6x6    # Balance (por defecto)
python png_to_astc.py -b 8x8    # Más compresión, menor calidad

# Cambiar la calidad de compresión
python png_to_astc.py -q veryfast    # Rápido, menor calidad
python png_to_astc.py -q thorough    # Balance (por defecto)
python png_to_astc.py -q exhaustive  # Mejor calidad, más lento

# Combinar opciones
python png_to_astc.py textures/ -b 4x4 -q exhaustive
```

### Proceso de Conversión

1. El script mostrará cuántos archivos PNG encontró:

```
Encontrados 42 archivos PNG
Directorio: /home/user/mi_mod
Configuración: 6x6, calidad thorough

¿Continuar con la conversión? (s/n):
```

2. Escribe `s` y presiona Enter para confirmar

3. El script convertirá y eliminará los PNG automáticamente:

```
Convirtiendo: textures/items/espada.png
✓ Creado: textures/items/espada.astc
✓ Eliminado: textures/items/espada.png

==================================================
Conversión completada:
  ✓ Exitosas: 42
  ✗ Fallidas: 0
==================================================
```

---

## 📊 Tamaños de Bloque y Calidad

### Tamaños de Bloque

| Tamaño | Calidad | Compresión | Uso Recomendado |
|--------|---------|------------|-----------------|
| 4x4    | ⭐⭐⭐⭐⭐ | 🔵🔵 | Texturas importantes, UI |
| 6x6    | ⭐⭐⭐⭐ | 🔵🔵🔵 | Balance general (predeterminado) |
| 8x8    | ⭐⭐⭐ | 🔵🔵🔵🔵 | Texturas de fondo, efectos |
| 12x12  | ⭐⭐ | 🔵🔵🔵🔵🔵 | Máxima compresión |

### Niveles de Calidad

- `veryfast` - Conversión rápida, menor calidad final
- `fast` - Rápido con calidad aceptable
- `medium` - Balance entre velocidad y calidad
- `thorough` - **Recomendado** - Buena calidad, velocidad aceptable
- `exhaustive` - Mejor calidad posible, muy lento

---

## ❓ Solución de Problemas

### Error: "astcenc no está instalado"

- Verifica que ejecutaste `astcenc -version` correctamente
- Asegúrate de haber copiado el ejecutable al PATH
- En Windows, reinicia la terminal después de agregar al PATH

### Error: "Host does not support AVX2"

Tu CPU no soporta AVX2. Usa `astcenc-sse4.1` o `astcenc-sse2` en su lugar.

### Error: "Permission denied"

En Linux/MacOS, asegúrate de dar permisos:
```bash
chmod +x png_to_astc.py
```

---

## 💡 Consejos

- **Prueba primero en una copia**: Haz pruebas en una carpeta de prueba antes de convertir todo tu mod
- **Compara visualmente**: Revisa cómo se ven las texturas convertidas en el juego
- **Ajusta según necesidad**: Usa mejor calidad (4x4) para texturas importantes y más compresión (8x8) para fondos
- **Haz backups**: Siempre mantén una copia de tus PNG originales en otro lugar

---

## 📜 Licencia

Este script es de uso libre. Úsalo bajo tu propio riesgo.

---

## ⭐ Apóyame

Si esta herramienta te fue útil, **dale una estrella al repositorio** ⭐

¡Tu apoyo significa mucho! ❤️

---

## 🤝 Contribuciones

¿Encontraste un bug o tienes una mejora? ¡Los pull requests son bienvenidos!

---

**Hecho con ❤️ para la comunidad de modding**
