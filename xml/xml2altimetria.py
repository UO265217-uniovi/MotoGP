import xml.etree.ElementTree as ET

class Svg(object):
    
    def __init__(self):
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="1.1", viewBox="0 0 1200 600")
    
    def addRect(self, x, y, width, height, fill, strokeWidth, stroke):
        ET.SubElement(self.raiz, 'rect', attrib={
            'x': str(x),
            'y': str(y),
            'width': str(width),
            'height': str(height),
            'fill': fill,
            'stroke-width': str(strokeWidth), # Nombre corregido para SVG
            'stroke': stroke
        })
    
    def addCircle(self, cx, cy, r, fill):
        ET.SubElement(self.raiz, 'circle', attrib={
            'cx': str(cx),
            'cy': str(cy),
            'r': str(r),
            'fill': fill
        })
    
    def addLine(self, x1, y1, x2, y2, stroke, strokeWidth):
        ET.SubElement(self.raiz, 'line', attrib={
            'x1': str(x1),
            'y1': str(y1),
            'x2': str(x2),
            'y2': str(y2),
            'stroke': stroke,
            'stroke-width': str(strokeWidth) # Nombre corregido
        })
    
    def addPolyline(self, points, stroke, strokeWidth, fill):
        ET.SubElement(self.raiz, 'polyline', attrib={
            'points': points,
            'stroke': stroke,
            'stroke-width': str(strokeWidth), # Nombre corregido
            'fill': fill
        })
    
    def addText(self, texto, x, y, fontFamily, fontSize, style):
        elemento = ET.SubElement(self.raiz, 'text', attrib={
            'x': str(x),
            'y': str(y),
            'font-family': fontFamily, # Nombre corregido
            'font-size': str(fontSize), # Nombre corregido
            'style': style
        })
        elemento.text = texto
    
    def escribir(self, nombreArchivoSVG):
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoSVG, encoding='utf-8', xml_declaration=True)
    
    def ver(self):
        print("\nElemento raiz = ", self.raiz.tag)
        if self.raiz.text != None:
            print("Contenido = ", self.raiz.text.strip('\n'))
        else:
            print("Contenido = ", self.raiz.text)
        print("Atributos = ", self.raiz.attrib)
        
        for hijo in self.raiz.findall('.//'):
            print("\nElemento = ", hijo.tag)
            if hijo.text != None:
                print("Contenido = ", hijo.text.strip('\n'))
            else:
                print("Contenido = ", hijo.text)
            print("Atributos = ", hijo.attrib)


def main():
    NAMESPACE = '{http://www.uniovi.es}'
    
    try:
        tree = ET.parse('circuitoEsquema.xml')
        raiz = tree.getroot()
    except FileNotFoundError:
        print("Error: No se encuentra el archivo 'circuitoEsquema.xml'")
        return

    distancias = [0]
    alturas = []       
    total_d = 0

    origen = raiz.find(f".//{NAMESPACE}origen/{NAMESPACE}coordenadas")
    if origen is not None:
        alt_text = origen.find(f"{NAMESPACE}alt").text
        alturas.append(float(alt_text))
    
    for tramo in raiz.findall(f".//{NAMESPACE}tramos/{NAMESPACE}tramo"):
        d_text = tramo.find(f"{NAMESPACE}distancia").text
        d = float(d_text)
        total_d += d
        distancias.append(total_d)
        
        coor = tramo.find(f"{NAMESPACE}coordenadas")
        alt_text = coor.find(f"{NAMESPACE}alt").text
        alturas.append(float(alt_text))

    if not distancias or not alturas:
        print("Error: No se han podido extraer datos del XML.")
        return

    w, h = 1200, 500
    mx, my = 80, 50
    
    max_d, min_d = max(distancias), min(distancias)
    max_a, min_a = max(alturas), min(alturas)
    
    span_d = (max_d - min_d) if (max_d - min_d) != 0 else 1
    span_a = (max_a - min_a) if (max_a - min_a) != 0 else 1

    def esc_x(x): return mx + (x - min_d) / span_d * (w - 2 * mx)
    def esc_y(y): return h - my - (y - min_a) / span_a * (h - 2 * my)

    puntos = " ".join([f"{esc_x(d):.2f},{esc_y(a):.2f}" for d, a in zip(distancias, alturas)])

    svg = Svg()
    
    # Ejes
    svg.addLine(mx, h-my, w-mx, h-my, 'black', 2)  # Eje X
    svg.addLine(mx, my, mx, h-my, 'black', 2)      # Eje Y
    
    # Etiquetas de ejes
    svg.addText("Distancia [m]", w//2, h-10, "Verdana", 25, "text-anchor: middle;")
    svg.addText("Altura [m]", 30, h//2, "Verdana", 25, "writing-mode: tb; glyph-orientation-vertical: 0;")
    svg.addText("Perfil altimétrico MotorLand Aragón", w//2, my, "Verdana", 30, "text-anchor: middle; fill: blue;")
    
    paso_x = 500
    for v in range(int(min_d), int(max_d) + 1, paso_x):
        x = esc_x(v)
        svg.addText(str(int(v)), x, h - my + 20, "Verdana", 15, "text-anchor: middle;")
        svg.addLine(x, h - my, x, h - my + 8, 'black', 1)
    
    paso_y = 10
    for v in range(int(min_a), int(max_a) + 1, paso_y):
        y = esc_y(v)
        svg.addText(str(int(v)), mx - 15, y + 5, "Verdana", 15, "text-anchor: middle;")
        svg.addLine(mx, y, mx - 8, y, 'black', 1)
    
    svg.addPolyline(puntos, 'blue', 4, 'none')
    
    svg.escribir("altimetria.svg")
    print("Creado el archivo: altimetria.svg")

if __name__ == "__main__":
    main()