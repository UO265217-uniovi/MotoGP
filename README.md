# INFO

    - URLGITHUB: https://uo265217-uniovi.github.io/MotoGP/

Aquí tienes la lista de herramientas y normas de validación formateada en Markdown (.md), lista para copiar y guardar en tu documentación del proyecto.

Markdown

# Lista de Herramientas de Validación - Proyecto MotoGP Desktop

Esta lista recoge los validadores oficiales y las herramientas necesarias para cumplir con las Pautas de Trabajo (P0) de la asignatura "Software y estándares para la Web".

## 1. Estructura y Estilos (W3C)

Es obligatorio que todos los documentos cumplan los estándares sin errores.

### Validador de HTML5 (Nu Html Checker)

- [cite_start]**Enlace:** [https://validator.w3.org/nu](https://validator.w3.org/nu) [cite: 2122]
- **Instrucciones:**
  - [cite_start]Utiliza la opción **"File Upload"** para validar tus archivos `.html` locales[cite: 2139].
  - [cite_start]Utiliza la opción **"Direct Input"** para validar el código HTML generado por JavaScript (copiando desde el inspector del navegador)[cite: 2143].
- [cite_start]**Objetivo:** 0 Errores y 0 Advertencias[cite: 2604].
  - [cite_start]_Nota:_ Se permiten advertencias informativas sobre el "trailing slash" (autocierre `/>`) en etiquetas vacías [cite: 2169-2171].

### Validador de CSS3

- [cite_start]**Enlace:** [https://jigsaw.w3.org/css-validator/](https://jigsaw.w3.org/css-validator/) [cite: 2185]
- **Instrucciones:**
  - [cite_start]Valida mediante **"Carga de Archivo"**[cite: 2215].
  - [cite_start]**IMPORTANTE:** Despliega la pestaña "Más opciones" y selecciona **"Todas las advertencias"**[cite: 2218].
- **Objetivo:** 0 Errores. [cite_start]Las advertencias solo se permiten si están justificadas con comentarios en el código [cite: 2608-2609]:
  1.  [cite_start]**Herencia de colores:** Justificar de qué elemento padre hereda el color[cite: 2610].
  2.  [cite_start]**Redefinición de propiedades:** Solo permitido dentro de `@media-queries`[cite: 2611].

---

## 2. Accesibilidad Web

[cite_start]Para utilizar estas herramientas, es necesario desplegar el proyecto en un servidor (ej. GitHub Pages)[cite: 2290].

### Nivel Requerido

- [cite_start]**Nivel:** AAA (WCAG 2.0)[cite: 1514, 2289].
- [cite_start]**Resultado esperado:** 0 Errores automáticos[cite: 2614].

### Herramientas

- **WAVE (Web Accessibility Evaluation Tool):**
  - [cite_start]**Enlace:** [http://wave.webaim.org/](http://wave.webaim.org/) [cite: 2291]
  - **Uso:** Informe visual de errores y contrastes.
- **AChecker:**
  - [cite_start]**Enlace:** [https://achecks.ca/achecker](https://achecks.ca/achecker) [cite: 2342]
  - [cite_start]**Configuración:** Seleccionar la guía **WCAG 2.0 AAA** en las opciones[cite: 2344].
- **TAW (Opcional):**
  - [cite_start]**Enlace:** [http://www.tawdis.net/](http://www.tawdis.net/) [cite: 2394]

---

## 3. Adaptabilidad (Diseño Responsivo)

### I Love Adaptive

- [cite_start]**Enlace:** [http://iloveadaptive.com/](http://iloveadaptive.com/) [cite: 2273]
- [cite_start]**Uso:** Comprobar la visualización simultánea en móviles, tablets y monitores[cite: 2588].
- [cite_start]**Requisito:** El contenido debe adaptarse correctamente a cualquier resolución sin perder información[cite: 2285].

---

## 4. XML y DTD/XSD

Se recomienda el uso de extensiones dentro del propio editor de código.

- [cite_start]**Visual Studio Code:** Extensión _"XML Language Support by Red Hat"_[cite: 1966].
- [cite_start]**Notepad++:** Plugin _"XML Tools"_ (requiere configuración para DTDs)[cite: 1974].
