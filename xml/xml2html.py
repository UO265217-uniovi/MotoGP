import xml.etree.ElementTree as ET

class HtmlDoc:
    def __init__(self):
        self.parts = []
    def add(self, html):
        self.parts.append(html)
    def write(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write('\n'.join(self.parts))

def main():
    NS = '{http://www.uniovi.es}'
    tree = ET.parse('circuitoEsquema.xml')
    root = tree.getroot()
    nombre = root.find(f"{NS}nombre").text

    html = HtmlDoc()
    html.add('<!DOCTYPE html>')
    html.add('<html lang="es">')
    html.add('  <head>')
    html.add('    <meta charset="UTF-8" />')
    html.add('    <title>MotoGP - Circuito</title>')
    html.add('    <meta name="author" content="Iván Roque Álvarez Lamas" />')
    html.add('    <meta name="description" content="Circuito MotoGP Desktop" />')
    html.add('    <meta name="keywords" content="MotoGP, Desktop, Circuito" />')
    html.add('    <meta name="viewport" content="width=device-width, initial-scale=1.0" />')
    html.add('    <link rel="stylesheet" type="text/css" href="estilo/estilo.css" />')
    html.add('    <link rel="stylesheet" type="text/css" href="estilo/layout.css" />')
    html.add('    <link rel="icon" href="multimedia/favicon.ico" type="image/x-icon" />')
    html.add('  </head>')
    html.add('  <body>')
    html.add('    <header>')
    html.add('      <h1>MotoGP Desktop</h1>')
    html.add('      <nav>')
    html.add('        <a href="index.html" title="Página de inicio">Inicio</a>')
    html.add('        <a href="piloto.html" title="Información del piloto">Piloto</a>')
    html.add('        <a class="active" href="circuito.html" title="Circuito del mundial">Circuito</a>')
    html.add('        <a href="meteorologia.html" title="Datos meteorologicos">Meteorología</a>')
    html.add('        <a href="clasificaciones.html" title="Resultados y posiciones">Clasificaciones</a>')
    html.add('        <a href="juegos.html" title="Juegos y actividades">Juegos</a>')
    html.add('        <a href="ayuda.html" title="Ayuda del proyecto">Ayuda</a>')
    html.add('      </nav>')
    html.add('    </header>')
    html.add('    <p><a href="index.html" title="Volver a la página de inicio">Inicio</a> > <strong>Circuito</strong></p>')
    html.add('    <main>')
    html.add('      <section>')
    html.add(f'        <h2>{nombre}</h2>')
    html.add('        <section>')
    html.add(f'          <h3>Presentación de {nombre}</h3>')
    localidad = root.find(f"{NS}localidad").text
    pais = root.find(f"{NS}pais").text
    patrocinador = root.find(f"{NS}patrocinador").text
    fecha = root.find(f"{NS}fecha").text
    vueltas = root.find(f"{NS}vueltas").text
    html.add(f'          <p>El circuito de {nombre} está situado en {localidad}, {pais}. Patrocinador principal: {patrocinador}. Fecha del evento: {fecha}, total de vueltas: {vueltas}.</p>')
    galeria_fotos = root.find(f"{NS}galeria_fotos")
    if galeria_fotos is not None:
        foto = galeria_fotos.find(f"{NS}foto")
        html.add('          <picture>')
        html.add(f'            <source srcset="{foto.attrib["url"]}" media="(max-width: 799px)" />')
        html.add(f'            <img src="{foto.attrib["url"]}" alt="Foto del circuito {nombre}" />')
        html.add('          </picture>')
    html.add('          <ul>')
    for tag in ['longitud', 'anchura_media', 'hora_inicio']:
        val = root.find(f"{NS}{tag}")
        texto = val.text if val is not None else ''
        unidad = val.attrib["unidad"] if val is not None and "unidad" in val.attrib else ''
        etiqueta = tag.replace('_',' ').capitalize()
        html.add(f'            <li>{etiqueta}: {texto} {unidad}</li>')
    html.add('          </ul>')
    galeria_videos = root.find(f"{NS}galeria_videos")
    if galeria_videos is not None:
        video = galeria_videos.find(f"{NS}video")
        html.add('          <video controls width="854" height="480">')
        html.add(f'            <source src="{video.attrib["url"]}" type="video/mp4" />')
        html.add('            Resumen circuito. Tu navegador no soporta el vídeo.')
        html.add('          </video>')
    html.add('        </section>')
    # Referencias externas
    refs = root.find(f"{NS}referencias")
    if refs is not None:
        html.add('        <aside>')
        html.add('          <h3>Enlaces externos</h3>')
        html.add('          <ul>')
        for ref in refs.findall(f"{NS}referencia"):
            url = ref.text.strip()
            html.add(f'            <li><a href="{url}" title="{nombre} referencia" target="_blank">{url}</a></li>')
        html.add('          </ul>')
        html.add('        </aside>')
    # Clasificación y vencedor
    clasifs = root.find(f"{NS}clasificados")
    venc = root.find(f"{NS}vencedor")
    if clasifs is not None and venc is not None:
        html.add('        <section>')
        html.add('          <h3>Resultados</h3>')
        html.add('          <table>')
        html.add('            <caption>Clasificación MotoGP</caption>')
        html.add('            <thead>')
        html.add('              <tr><th>Nombre</th><th>Puntos</th></tr>')
        html.add('            </thead>')
        html.add('            <tbody>')
        for c in clasifs.findall(f"{NS}clasificacion_participante"):
            nom = c.find(f"{NS}nombre").text
            pts = c.find(f"{NS}puntos").text
            html.add(f'              <tr><td>{nom}</td><td>{pts}</td></tr>')
        html.add('            </tbody>')
        html.add('          </table>')
        nombre_v = venc.find(f"{NS}nombre").text
        tiempo_v = venc.find(f"{NS}tiempo_carrera").text
        html.add(f'          <p>Ganador del evento: <strong>{nombre_v} ({tiempo_v})</strong></p>')
        html.add('        </section>')
    html.add('      </section>')
    html.add('    </main>')
    html.add('  </body>')
    html.add('</html>')
    html.write("InfoCircuito.html")

if __name__ == "__main__":
    main()
