---
tags:
  - recurso
  - design-system
aliases:
  - Licencia de Material Symbols
description: >-
  Origen y licencia de la fuente de iconos Material Symbols Outlined que usa Terracotta en presentaciones/.
---

# Licencia de Material Symbols

- **Origen:** repositorio oficial `google/material-design-icons` en GitHub, carpeta `variablefont/` (fuente variable Material Symbols Outlined y su archivo de codepoints), descargado el 01-11-2026.
- **Licencia:** Apache 2.0 (Google). Permite uso comercial, modificación y redistribución conservando el aviso de licencia.
- **Qué hay aquí:** `material-symbols-completo-300.woff2` es la fuente completa instanciada a peso 300, relleno 0, grado 0 y tamaño óptico 24 (los valores de Terracotta), y `material-symbols.codepoints` es la lista de nombres. `material-symbols-ea.woff2` es el subconjunto con los iconos del catálogo (`ea_elementos/iconos.py`), el que va incrustado en cada HTML.
- **Etiquetas:** `material-symbols-etiquetas.json` guarda las categorías, la popularidad y los sinónimos en inglés de cada icono (de `fonts.google.com/metadata/icons?key=material_symbols`, 01-11-2026), para `iconos.buscar_completo()`.
- **Actualizar la familia (regla N3):** volver a descargar del repositorio oficial la fuente variable `MaterialSymbolsOutlined[FILL,GRAD,opsz,wght].ttf` y su `.codepoints`, instanciarla a wght 300, FILL 0, GRAD 0, opsz 24 con `fontTools.varLib.instancer`, guardarla como `material-symbols-completo-300.woff2`, y regenerar las etiquetas desde la URL de metadatos.
- **Regenerar el subconjunto:** `python3 build_galeria_elementos.py` (llama a `iconos.generar_fuente()`).
