# INFO

    - URLGITHUB: https://uo265217-uniovi.github.io/MotoGP/

# Lista de Herramientas de Validación y Normativa - Proyecto MotoGP Desktop

Esta lista recoge los validadores oficiales y las herramientas necesarias para cumplir con las Pautas de Trabajo (P0) de la asignatura "Software y estándares para la Web", así como los requisitos críticos para evitar la invalidación del proyecto.

## 1. Estructura y Estilos (W3C)

Es obligatorio que todos los documentos cumplan los estándares sin errores.

### Validador de HTML5 (Nu Html Checker)

- **Enlace:** [https://validator.w3.org/nu](https://validator.w3.org/nu)
- **Instrucciones:**
  - Utiliza la opción **"File Upload"** para validar tus archivos `.html` locales.
  - Utiliza la opción **"Direct Input"** para validar el código HTML generado por JavaScript (copiando desde el inspector del navegador).
- **Objetivo:** 0 Errores y 0 Advertencias.
  - _Nota:_ Se permiten advertencias informativas sobre el "trailing slash" (autocierre `/>`) en etiquetas vacías.

### Validador de CSS3

- **Enlace:** [https://jigsaw.w3.org/css-validator/](https://jigsaw.w3.org/css-validator/)
- **Instrucciones:**
  - Valida mediante **"Carga de Archivo"**.
  - **IMPORTANTE:** Despliega la pestaña "Más opciones" y selecciona **"Todas las advertencias"**.
- **Objetivo:** 0 Errores. Las advertencias solo se permiten si están justificadas con comentarios en el código:
  1.  **Herencia de colores:** Justificar de qué elemento padre hereda el color para garantizar el contraste.
  2.  **Redefinición de propiedades:** Solo permitido si deriva del uso de `@media-queries`.

---

## 2. Accesibilidad Web

Para utilizar estas herramientas, es necesario desplegar el proyecto en un servidor (ej. GitHub Pages).

### Nivel Requerido

- **Nivel:** AAA (WCAG 2.0).
- **Resultado esperado:** 0 Errores automáticos y 0 errores de contraste.

### Herramientas

- **WAVE (Web Accessibility Evaluation Tool):**
  - **Enlace:** [http://wave.webaim.org/](http://wave.webaim.org/)
  - **Uso:** Informe visual de errores y contrastes.
- **AChecker:**
  - **Enlace:** [https://achecks.ca/achecker](https://achecks.ca/achecker)
  - **Configuración:** Seleccionar la guía **WCAG 2.0 AAA** en las opciones.
- **TAW (Opcional):**
  - **Enlace:** [http://www.tawdis.net/](http://www.tawdis.net/)

---

## 3. Adaptabilidad (Diseño Responsivo)

### I Love Adaptive

- **Enlace:** [http://iloveadaptive.com/](http://iloveadaptive.com/)
- **Uso:** Comprobar la visualización simultánea en móviles, tablets y monitores.
- **Requisito:** El contenido debe adaptarse correctamente a cualquier resolución sin perder información.

---

## 4. Requisitos Críticos y Excepciones (Dónde usarlas)

El incumplimiento de las siguientes normas generales deriva en la **invalidación del proyecto** (calificación de 0). A continuación se detallan las prohibiciones y **dónde exactamente** se permiten las excepciones.

### A. Uso de `id` y `class` en selectores CSS

- **Norma:** "El uso de selectores id y class no está permitido".
- **EXCEPCIONES PERMITIDAS:**
  1.  **Práctica 3 - Ejercicio 2 (Elemento activo del menú):** Se permite usar una clase (ej. `.active`) exclusivamente para resaltar el enlace de la página que se está visualizando actualmente.

### B. Uso de Atributos `id` en HTML

- **Norma:** Evitar ids para estilar.
- **REQUISITO OBLIGATORIO:**
  1.  **Práctica 2 - Ejercicio 6 (Accesibilidad en tablas):** Es obligatorio usar atributos `id` en las celdas de encabezado (`<th>`) para vincularlas con las celdas de datos (`<td>`) mediante el atributo `headers`.

### C. Uso de etiquetas `<div>` (Bloques anónimos)

- **Norma:** "No está permitido el uso de bloques anónimos (div)". Se deben usar etiquetas semánticas (`section`, `article`, etc.).
- **EXCEPCIÓN PERMITIDA:**
  1.  **Práctica 9 - Ejercicio 3 (Mapas Dinámicos):** Se permite usar un `div` exclusivamente como contenedor para el mapa dinámico (Google Maps o MapBox) y usar su selector en CSS, debido a las restricciones técnicas de las APIs.

### D. JavaScript y Librerías

- **Norma:** Se debe usar ECMAScript puro ("vanilla"). "No se permite el uso de ningún tipo de bibliotecas externas".
- **EXCEPCIÓN PERMITIDA:**
  1.  **Práctica 8 (Todo el ejercicio) y Práctica 9 (Mapas/Menú):** Se permite y/o requiere el uso de **jQuery** para el consumo de servicios web (AJAX) y manipulación del DOM en estos ejercicios específicos.

### E. Atributos HTML5 Especiales

- **Norma:** Uso restringido de atributos no estándar.
- **EXCEPCIÓN PERMITIDA:**
  1.  **Práctica 6 - Ejercicio 3 (Juego de Memoria):** Se permite el uso de atributos `data-` (ej. `data-estado`) explícitamente para gestionar la lógica y el estado de las cartas.
