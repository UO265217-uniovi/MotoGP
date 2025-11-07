import xml.etree.ElementTree as ET

class Svg:
    def __init__(self, width, height):
        self.root = ET.Element('svg', xmlns="http://www.w3.org/2000/svg",
                              width=str(width), height=str(height),
                              version="2.0")
    def addPolyline(self, points, stroke="blue", strokeWidth="3", fill="none"):
        ET.SubElement(self.root, "polyline", points=points,
                      stroke=stroke, strokeWidth=str(strokeWidth), fill=fill)
    def addAxis(self, width, height, margin_x, margin_y):
        # Eje horizontal
        ET.SubElement(self.root, "line",
                      x1=str(margin_x), y1=str(height-margin_y),
                      x2=str(width-margin_x), y2=str(height-margin_y),
                      stroke="black", strokeWidth="2")
        # Eje vertical
        ET.SubElement(self.root, "line",
                      x1=str(margin_x), y1=str(margin_y),
                      x2=str(margin_x), y2=str(height-margin_y),
                      stroke="black", strokeWidth="2")

    def addText(self, text, x, y, color="black", fontSize="20", anchor="middle", rotate=None):
        t = ET.SubElement(self.root, "text", x=str(x), y=str(y),
                          fill=color, fontSize=str(fontSize), text_anchor=anchor)
        if rotate is not None:
            t.attrib["transform"] = f"rotate({rotate} {x},{y})"
        t.text = text

    def addTicks(self, ticks, axis, margin_x, margin_y, width, height, min_val, max_val, fontSize=15):
        if axis == "x":
            for v in ticks:
                x = margin_x + (v-min_val) / (max_val-min_val) * (width-2*margin_x)
                y = height-margin_y+20
                self.addText(str(int(v)), x, y, fontSize=fontSize)
                ET.SubElement(self.root, "line", x1=str(x), y1=str(height-margin_y),
                              x2=str(x), y2=str(height-margin_y+8), stroke="black")
        elif axis == "y":
            for v in ticks:
                x = margin_x-15
                y = height-margin_y - (v-min_val) / (max_val-min_val) * (height-2*margin_y)
                self.addText(str(int(v)), x, y+5, fontSize=fontSize)
                ET.SubElement(self.root, "line", x1=str(margin_x), y1=str(y),
                              x2=str(margin_x-8), y2=str(y), stroke="black")

    def write(self, filename):
        tree = ET.ElementTree(self.root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)

def main():
    NAMESPACE = '{http://www.uniovi.es}'
    tree = ET.parse('circuitoEsquema.xml')
    raiz = tree.getroot()

    distancias = [0]   # Distancia acumulada
    alturas = []       # Altitud
    total_d = 0

    # Origen
    origen = raiz.find(f"{NAMESPACE}origen/{NAMESPACE}coordenadas")
    if origen is not None:
        alt = float(origen.find(f"{NAMESPACE}alt").text)
        alturas.append(alt)
    # Tramos
    for tramo in raiz.findall(f"{NAMESPACE}tramos/{NAMESPACE}tramo"):
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

    def esc_x(x): return mx + (x-min_d) / span_d * (w-2*mx)
    def esc_y(y): return h-my - (y-min_a) / span_a * (h-2*my)

    puntos = " ".join([f"{esc_x(d):.2f},{esc_y(a):.2f}" for d, a in zip(distancias, alturas)])

    svg = Svg(w, h)
    svg.addAxis(w, h, mx, my)
    svg.addText("Distancia [m]", w//2, h-10, fontSize="25")
    svg.addText("Altura [m]", 30, h//2, fontSize="25", anchor="middle", rotate="-90")
    svg.addText("Perfil altimétrico MotorLand Aragón", w//2, my, color="blue", fontSize="30", anchor="middle")
    # Añade ticks cada 500m en X y cada 10m en Y
    svg.addTicks(list(range(int(min_d), int(max_d)+1, 500)), "x", mx, my, w, h, min_d, max_d)
    svg.addTicks(list(range(int(min_a), int(max_a)+1, 10)), "y", mx, my, w, h, min_a, max_a)
    svg.addPolyline(puntos, stroke="blue", strokeWidth="4", fill="none")
    svg.write("altimetria.svg")

if __name__ == "__main__":
    main()
