import xml.etree.ElementTree as ET

class Svg(object):
    
    def __init__(self):
        """
        Crea el elemento raíz, el espacio de nombres y la versión
        """
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="2.0")
    
    def addRect(self, x, y, width, height, fill, strokeWidth, stroke):
        """
        Añade un elemento rect
        """
        ET.SubElement(self.raiz, 'rect',
                     x=x,
                     y=y,
                     width=width,
                     height=height,
                     fill=fill,
                     strokeWidth=strokeWidth,
                     stroke=stroke)
    
    def addCircle(self, cx, cy, r, fill):
        """
        Añade un elemento circle
        """
        ET.SubElement(self.raiz, 'circle',
                     cx=cx,
                     cy=cy,
                     r=r,
                     fill=fill)
    
    def addLine(self, x1, y1, x2, y2, stroke, strokeWidth):
        """
        Añade un elemento line
        """
        ET.SubElement(self.raiz, 'line',
                     x1=x1,
                     y1=y1,
                     x2=x2,
                     y2=y2,
                     stroke=stroke,
                     strokeWidth=strokeWidth)
    
    def addPolyline(self, points, stroke, strokeWidth, fill):
        """
        Añade un elemento polyline
        """
        ET.SubElement(self.raiz, 'polyline',
                     points=points,
                     stroke=stroke,
                     strokeWidth=strokeWidth,
                     fill=fill)
    
    def addText(self, texto, x, y, fontFamily, fontSize, style):
        """
        Añade un elemento texto
        """
        ET.SubElement(self.raiz, 'text',
                     x=x,
                     y=y,
                     fontFamily=fontFamily,
                     fontSize=fontSize,
                     style=style).text = texto
    
    def escribir(self, nombreArchivoSVG):
        """
        Escribe el archivo SVG con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        """
        Introduce indentación y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)
        arbol.write(nombreArchivoSVG,
                   encoding='utf-8',
                   xml_declaration=True)
    
    def ver(self):
        """
        Muestra el archivo SVG. Se utiliza para depurar
        """
        print("\nElemento raiz = ", self.raiz.tag)
        if self.raiz.text != None:
            print("Contenido = ", self.raiz.text.strip('\n'))
        else:
            print("Contenido = ", self.raiz.text)
        print("Atributos = ", self.raiz.attrib)
        
        # Recorrido de los elementos del árbol usando XPath
        for hijo in self.raiz.findall('.//'):  # Expresión XPath
            print("\nElemento = ", hijo.tag)
            if hijo.text != None:
                print("Contenido = ", hijo.text.strip('\n'))
            else:
                print("Contenido = ", hijo.text)
            print("Atributos = ", hijo.attrib)


def main():
    NAMESPACE = '{http://www.uniovi.es}'
    tree = ET.parse('circuitoEsquema.xml')
    raiz = tree.getroot()

    distancias = [0]   # Distancia acumulada
    alturas = []       # Altitud
    total_d = 0

    # Usando XPath: origen
    origen = raiz.find(f".//{NAMESPACE}origen/{NAMESPACE}coordenadas")
    if origen is not None:
        alt = float(origen.find(f"{NAMESPACE}alt").text)
        alturas.append(alt)
    
    # Usando XPath: tramos
    for tramo in raiz.findall(f".//{NAMESPACE}tramos/{NAMESPACE}tramo"):
        d = float(tramo.find(f"{NAMESPACE}distancia").text)
        total_d += d
        distancias.append(total_d)
        coor = tramo.find(f"{NAMESPACE}coordenadas")
        alt = float(coor.find(f"{NAMESPACE}alt").text)
        alturas.append(alt)

    # Parámetros SVG y escalado
    w, h = 1200, 500
    mx, my = 80, 50
    max_d, min_d = max(distancias), min(distancias)
    max_a, min_a = max(alturas), min(alturas)
    span_d, span_a = max_d - min_d, max_a - min_a

    def esc_x(x): return mx + (x - min_d) / span_d * (w - 2 * mx)
    def esc_y(y): return h - my - (y - min_a) / span_a * (h - 2 * my)

    puntos = " ".join([f"{esc_x(d):.2f},{esc_y(a):.2f}" for d, a in zip(distancias, alturas)])

    svg = Svg()
    
    # Ejes
    svg.addLine(str(mx), str(h-my), str(w-mx), str(h-my), 'black', '2')  # Eje X
    svg.addLine(str(mx), str(my), str(mx), str(h-my), 'black', '2')      # Eje Y
    
    # Etiquetas de ejes
    svg.addText("Distancia [m]", str(w//2), str(h-10), "Verdana", "25", "text-anchor: middle;")
    svg.addText("Altura [m]", "30", str(h//2), "Verdana", "25", "writing-mode: tb; glyph-orientation-vertical: 0;")
    svg.addText("Perfil altimétrico MotorLand Aragón", str(w//2), str(my), "Verdana", "30", "text-anchor: middle; fill: blue;")
    
    # Ticks en X (cada 500m)
    for v in range(int(min_d), int(max_d) + 1, 500):
        x = mx + (v - min_d) / span_d * (w - 2 * mx)
        svg.addText(str(int(v)), str(x), str(h - my + 20), "Verdana", "15", "text-anchor: middle;")
        svg.addLine(str(x), str(h - my), str(x), str(h - my + 8), 'black', '1')
    
    # Ticks en Y (cada 10m)
    for v in range(int(min_a), int(max_a) + 1, 10):
        y = h - my - (v - min_a) / span_a * (h - 2 * my)
        svg.addText(str(int(v)), str(mx - 15), str(y + 5), "Verdana", "15", "text-anchor: middle;")
        svg.addLine(str(mx), str(y), str(mx - 8), str(y), 'black', '1')
    
    # Polilínea del perfil
    svg.addPolyline(puntos, 'blue', '4', 'none')
    
    svg.escribir("altimetria.svg")
    print("Creado el archivo: altimetria.svg")


if __name__ == "__main__":
    main()
