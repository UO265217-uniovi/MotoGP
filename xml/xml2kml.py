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
        self.kml = ET.Element('kml', xmlns='http://www.opengis.net/kml/2.2')
        self.doc = ET.SubElement(self.kml, 'Document')

    def add_line(self, name, coords, color):
        placemark = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(placemark, 'name').text = name
        style = ET.SubElement(placemark, 'Style')
        linestyle = ET.SubElement(style, 'LineStyle')
        ET.SubElement(linestyle, 'color').text = color
        ET.SubElement(linestyle, 'width').text = '5'
        linestring = ET.SubElement(placemark, 'LineString')
        ET.SubElement(linestring, 'extrude').text = '1'
        ET.SubElement(linestring, 'tessellate').text = '1'
        ET.SubElement(linestring, 'altitudeMode').text = 'clampToGround'
        ET.SubElement(linestring, 'coordinates').text = "\n".join(coords)

    def write(self, filename):
        tree = ET.ElementTree(self.kml)
        tree.write(filename, encoding='utf-8', xml_declaration=True)

def main():
    tree = ET.parse('circuitoEsquema.xml')
    root = tree.getroot()

    # 1. Agrupa coordenadas por sector, conectando sectores (sin altitud)
    sectores_coords = {}
    # Origen: siempre primer punto, lo metemos en el primer sector
    origen_coord = root.find(f"{NAMESPACE}origen/{NAMESPACE}coordenadas")
    origen_pt = None
    if origen_coord is not None:
        lon = origen_coord.find(f"{NAMESPACE}lon").text
        lat = origen_coord.find(f"{NAMESPACE}lat").text
        origen_pt = f"{lon},{lat}"

    last_sector = None
    last_coord = origen_pt
    for tramo in root.findall(f"{NAMESPACE}tramos/{NAMESPACE}tramo"):
        sector = tramo.attrib['sector']
        c = tramo.find(f"{NAMESPACE}coordenadas")
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
        last_sector = sector
        last_coord = coord

    kml = Kml()
    # 2. Añade cada sector
    for sector in sorted(sectores_coords.keys(), key=int):
        nombre = f"Sector {sector}"
        color = SECTOR_COLORS.get(sector, 'ff000000')
        coords = sectores_coords[sector]
        kml.add_line(nombre, coords, color)

    kml.write('circuito.kml')

if __name__ == "__main__":
    main()