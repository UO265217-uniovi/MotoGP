# -*- coding: utf-8 -*-
"""
Genera archivo HTML a partir de XML usando XPath
@version 1.0
@author: [Tu nombre]
"""

import xml.etree.ElementTree as ET


class Html(object):
    """
    Genera archivos HTML a partir de información XML
    @version 1.0
    """
    
    def __init__(self):
        """
        Crea la lista para almacenar las partes del HTML
        """
        self.partes = []
    
    def agregar(self, linea):
        """
        Añade una línea al HTML
        """
        self.partes.append(linea)
    
    def escribir(self, nombreArchivoHTML):
        """
        Escribe el archivo HTML con codificación UTF-8
        """
        with open(nombreArchivoHTML, 'w', encoding='utf-8') as archivo:
            archivo.write('\n'.join(self.partes))


def main():
    NAMESPACE = '{http://www.uniovi.es}'
    
    # Parsear el archivo XML usando XPath
    tree = ET.parse('circuitoEsquema.xml')
    raiz = tree.getroot()
    
    # Extraer información usando expresiones XPath
    nombre = raiz.find(f".//{NAMESPACE}nombre").text
    localidad = raiz.find(f".//{NAMESPACE}localidad").text
    pais = raiz.find(f".//{NAMESPACE}pais").text
    patrocinador = raiz.find(f".//{NAMESPACE}patrocinador").text
    fecha = raiz.find(f".//{NAMESPACE}fecha").text
    vueltas = raiz.find(f".//{NAMESPACE}vueltas").text
    
    # Crear objeto Html
    html = Html()
    
    # Estructura HTML
    html.agregar('<!DOCTYPE html>')
    html.agregar('<html lang="es">')
    html.agregar('  <head>')
    html.agregar('    <meta charset="UTF-8" />')
    html.agregar(f'    <title>MotoGP - {nombre}</title>')
    html.agregar('')
    html.agregar('    <meta name="author" content="Iván Roque Álvarez Lamas" />')
    html.agregar(f'    <meta name="description" content="Circuito MotoGP Desktop" />')
    html.agregar('    <meta name="keywords" content="MotoGP, Desktop, Circuito" />')
    html.agregar('    <meta name="viewport" content="width=device-width, initial-scale=1.0" />')
    html.agregar('')
    html.agregar('    <link rel="stylesheet" type="text/css" href="../estilo/estilo.css" />')
    html.agregar('    <link rel="stylesheet" type="text/css" href="../estilo/layout.css" />')
    html.agregar('')
    html.agregar('    <link rel="icon" href="../multimedia/favicon.ico" type="image/x-icon" />')
    html.agregar('  </head>')
    html.agregar('  <body>')
    html.agregar('    <header>')
    html.agregar('      <h1>MotoGP Desktop</h1>')
    html.agregar('      <nav>')
    html.agregar('        <a href="../index.html" title="Página de inicio">Inicio</a>')
    html.agregar('        <a href="../piloto.html" title="Información del piloto">Piloto</a>')
    html.agregar('        <a class="active" href="circuito.html" title="Circuito del mundial">Circuito</a>')
    html.agregar('        <a href="../meteorologia.html" title="Datos meteorologicos">Meteorología</a>')
    html.agregar('        <a href="../clasificaciones.html" title="Resultados y posiciones">Clasificaciones</a>')
    html.agregar('        <a href="../juegos.html" title="Juegos y actividades">Juegos</a>')
    html.agregar('        <a href="../ayuda.html" title="Ayuda del proyecto">Ayuda</a>')
    html.agregar('      </nav>')
    html.agregar('    </header>')
    html.agregar('    <p>')
    html.agregar('      <a href="../index.html" title="Volver a la página de inicio">Inicio</a>')
    html.agregar('      > <strong>Circuito</strong>')
    html.agregar('    </p>')
    html.agregar('    <main>')
    html.agregar('      <section>')
    html.agregar(f'        <h2>{nombre}</h2>')
    html.agregar('        <section>')
    html.agregar(f'          <h3>Presentación de {nombre}</h3>')
    
    # Párrafo descriptivo
    html.agregar('          <p>')
    html.agregar(f'            El circuito de {nombre} está situado en {localidad}, {pais}.')
    html.agregar(f'            Patrocinador principal: {patrocinador}. Fecha del evento: {fecha},')
    html.agregar(f'            total de vueltas: {vueltas}.')
    html.agregar('          </p>')
    
    # Galería de fotos usando XPath
    galeria_fotos = raiz.find(f".//{NAMESPACE}galeria_fotos")
    if galeria_fotos is not None:
        foto = galeria_fotos.find(f"{NAMESPACE}foto")
        if foto is not None:
            url_foto = foto.attrib.get("url", "")
            html.agregar('          <picture>')
            html.agregar(f'            <source srcset="{url_foto}" media="(max-width: 799px)" />')
            html.agregar(f'            <img src="{url_foto}" alt="Foto del circuito {nombre}" />')
            html.agregar('          </picture>')
    
    # Lista de características usando XPath
    html.agregar('          <ul>')
    
    longitud_elem = raiz.find(f".//{NAMESPACE}longitud")
    if longitud_elem is not None:
        longitud_texto = longitud_elem.text
        longitud_unidad = longitud_elem.attrib.get("unidad", "")
        html.agregar(f'            <li>Longitud: {longitud_texto} {longitud_unidad}</li>')
    
    anchura_elem = raiz.find(f".//{NAMESPACE}anchura_media")
    if anchura_elem is not None:
        anchura_texto = anchura_elem.text
        anchura_unidad = anchura_elem.attrib.get("unidad", "")
        html.agregar(f'            <li>Anchura media: {anchura_texto} {anchura_unidad}</li>')
    
    hora_elem = raiz.find(f".//{NAMESPACE}hora_inicio")
    if hora_elem is not None:
        hora_texto = hora_elem.text
        hora_unidad = hora_elem.attrib.get("unidad", "")
        html.agregar(f'            <li>Hora inicio: {hora_texto} {hora_unidad}</li>')
    
    html.agregar('          </ul>')
    
    # Galería de videos usando XPath
    galeria_videos = raiz.find(f".//{NAMESPACE}galeria_videos")
    if galeria_videos is not None:
        video = galeria_videos.find(f"{NAMESPACE}video")
        if video is not None:
            url_video = video.attrib.get("url", "")
            html.agregar('          <video controls>')
            html.agregar(f'            <source src="{url_video}" type="video/mp4" />')
            html.agregar('            Resumen circuito. Tu navegador no soporta el vídeo.')
            html.agregar('          </video>')
    
    html.agregar('        </section>')
    
    # Referencias externas usando XPath
    referencias = raiz.find(f".//{NAMESPACE}referencias")
    if referencias is not None:
        refs_lista = referencias.findall(f"{NAMESPACE}referencia")
        if refs_lista:
            html.agregar('        <aside>')
            html.agregar('          <h3>Enlaces externos</h3>')
            html.agregar('          <ul>')
            for ref in refs_lista:
                url = ref.text.strip()
                html.agregar('            <li>')
                html.agregar(f'              <a href="{url}" title="{nombre} referencia" target="_blank">{url}</a>')
                html.agregar('            </li>')
            html.agregar('          </ul>')
            html.agregar('        </aside>')
    
    # Clasificación y vencedor usando XPath
    clasificados_elem = raiz.find(f".//{NAMESPACE}clasificados")
    vencedor_elem = raiz.find(f".//{NAMESPACE}vencedor")
    
    if clasificados_elem is not None and vencedor_elem is not None:
        html.agregar('        <section>')
        html.agregar('          <h3>Resultados</h3>')
        html.agregar('          <table>')
        html.agregar('            <caption>')
        html.agregar('              Clasificación MotoGP')
        html.agregar('            </caption>')
        html.agregar('            <thead>')
        html.agregar('              <tr>')
        html.agregar('                <th id="nom" scope="col">Nombre</th>')
        html.agregar('                <th id="pts" scope="col">Puntos</th>')
        html.agregar('              </tr>')
        html.agregar('            </thead>')
        html.agregar('            <tbody>')
        
        # Participantes usando XPath
        participantes = clasificados_elem.findall(f"{NAMESPACE}clasificacion_participante")
        for participante in participantes:
            nom = participante.find(f"{NAMESPACE}nombre").text
            pts = participante.find(f"{NAMESPACE}puntos").text
            html.agregar('              <tr>')
            html.agregar(f'                <td headers="nom">{nom}</td>')
            html.agregar(f'                <td headers="pts">{pts}</td>')
            html.agregar('              </tr>')
        
        html.agregar('            </tbody>')
        html.agregar('          </table>')
        
        # Información del vencedor usando XPath
        nombre_venc = vencedor_elem.find(f"{NAMESPACE}nombre").text
        tiempo_venc = vencedor_elem.find(f"{NAMESPACE}tiempo_carrera").text
        html.agregar(f'          <p>Ganador del evento: <strong>{nombre_venc} ({tiempo_venc})</strong></p>')
        
        html.agregar('        </section>')
    
    # Cerrar estructura HTML
    html.agregar('      </section>')
    html.agregar('    </main>')
    html.agregar('  </body>')
    html.agregar('</html>')
    
    # Escribir archivo
    html.escribir("InfoCircuito.html")
    print("Archivo InfoCircuito.html creado exitosamente")


if __name__ == "__main__":
    main()
