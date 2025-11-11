import xml.etree.ElementTree as ET

NAMESPACE = '{http://www.uniovi.es}'
ET.register_namespace('', 'http://www.opengis.net/kml/2.2')

# Colores ABGR: sector 1 rojo, 2 verde, 3 azul
SECTOR_COLORS = {
    '1': 'ff0000ff',  # Rojo
    '2': 'ff00ff00',  # Verde
    '3': 'ffff0000',  # Azul
}

class Kml:
    def __init__(self):
        self.raiz = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
        self.doc = ET.SubElement(self.raiz, 'Document')

    def addLineString(self, nombre, extrude, tesela, listaCoordenadas, modoAltitud, color, ancho):
        """
        Añade un elemento con líneas
        """
        pm = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(pm, 'name').text = nombre
        
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls, 'extrude').text = extrude
        ET.SubElement(ls, 'tessellate').text = tesela
        ET.SubElement(ls, 'coordinates').text = listaCoordenadas
        ET.SubElement(ls, 'altitudeMode').text = modoAltitud
        
        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement(linea, 'color').text = color
        ET.SubElement(linea, 'width').text = ancho

    def escribir(self, nombreArchivoKML):
        """
        Escribe el archivo KML con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding='utf-8', xml_declaration=True)

def main():
    tree = ET.parse('circuitoEsquema.xml')
    root = tree.getroot()

    # Usando XPath: obtener coordenadas del origen
    origen_coord = root.find(f".//{NAMESPACE}origen/{NAMESPACE}coordenadas")
    origen_pt = None
    if origen_coord is not None:
        lon = origen_coord.find(f"{NAMESPACE}lon").text
        lat = origen_coord.find(f"{NAMESPACE}lat").text
        origen_pt = f"{lon},{lat}"

    # Agrupar coordenadas por sector usando XPath
    sectores_coords = {}
    last_coord = origen_pt

    # Usando XPath para obtener todos los tramos
    for tramo in root.findall(f".//{NAMESPACE}tramos/{NAMESPACE}tramo"):
        sector = tramo.attrib['sector']
        
        # Usando XPath para obtener coordenadas
        c = tramo.find(f"./{NAMESPACE}coordenadas")
        lon = c.find(f"{NAMESPACE}lon").text
        lat = c.find(f"{NAMESPACE}lat").text
        coord = f"{lon},{lat}"
        
        # Crea lista de sector si no existe
        if sector not in sectores_coords:
            sectores_coords[sector] = []
            # El primer punto del primer sector es el origen
            if last_coord:
                sectores_coords[sector].append(last_coord)
        
        sectores_coords[sector].append(coord)
        last_coord = coord

    kml = Kml()
    
    # Añade cada sector al KML
    for sector in sorted(sectores_coords.keys(), key=int):
        nombre = f"Sector {sector}"
        color = SECTOR_COLORS.get(sector, 'ff000000')
        coords = sectores_coords[sector]
        listaCoordenadas = "\n".join(coords)
        
        kml.addLineString(nombre, '1', '1', listaCoordenadas, 'clampToGround', color, '5')

    kml.escribir('circuito.kml')
    print("Creado el archivo: circuito.kml")

if __name__ == "__main__":
    main()
