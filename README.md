# astc-optimizer
Un script que te facilita comprimir archivos pngs a archivos .astc para mejorar el rendimiento y reducir el peso de un mod.

## Notas IMPORTANTES
* Este script borra tus pngs y los reemplaza con archivos comprimidos .astc
Asi que ten una copia de seguridad de tu mod antes de ejecutar este script, ya que esta acción es irreversible y **NO ME HAGO RESPONSABLE POR PERDIDAS**.

* Ya sabemos que al comprimir algo pierde calidad, y se vera pixelado, pero es el precio a pagar por el rendimiento, asi que estas enterado.

# Cómo usarlo

Asegurate de instalar [Astc Encoder](https://github.com/ARM-software/astc-encoder/releases)

Al descomprimir tendras 3 programas, el recomendado es **astcenc-sse4.1**

Luego debes agregarlo al PATH cómo "**astcenc**" para que este disponible gobalmente en tu CMD o Terminal, así solo tendras que llamarlo en la consola.

> Verificación
Para ver si esta instalado correctamente ejecuta 
```bash
astcenc -version
```
Deberia salirte algo cómo esto en consola:
```
astcenc v5.3.0, 64-bit sse4.1+popcnt
Copyright (c) 2011-2025 Arm Limited. All rights reserved.
```


> Uso
Con el script colocado en `/tu mod/optimizer.py`, solo abre una terminal en esa misma carpeta y ejecuta:
```bash
python png_to_astc.py
```

Te dira la cantidad de archivos a convertir y como ultima confirmación te pedira esto:
```
¿Continuar con la conversión? (s/n): 
```
Solo deberás aceptar si estas seguro ya que esta opción **borra todos tus pngs** y los reemplaza con archivos comprimidos **.astc**

# Si usas mi herramienta asegurate de darle una estrellita, te lo agradeceria muchisimo ❤️.