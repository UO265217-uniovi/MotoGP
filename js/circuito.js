class Circuito {
  constructor() {
    if (!this.comprobarApiFile()) {
      $("main").append("<p>Este navegador no soporta API File</p>");
    }
  }

  comprobarApiFile() {
    return window.File && window.FileReader && window.FileList && window.Blob;
  }

  leerArchivoHTML(files) {
    const archivo = files[0];

    if (!archivo) return;

    const lector = new FileReader();

    lector.onload = (evento) => {
      this.mostrarContenido(lector.result);
    };

    lector.readAsText(archivo);
  }

  mostrarContenido(contenido) {
    const zonaDestino = document.querySelector(
      "main > section:nth-of-type(1) > section"
    );

    const parser = new DOMParser();
    const doc = parser.parseFromString(contenido, "text/html");

    const contenidoPrincipal = doc.querySelector("main > section");

    zonaDestino.innerHTML = "";

    const titulo = document.createElement("h4");
    titulo.textContent = "Datos del archivo seleccionado:";
    zonaDestino.appendChild(titulo);

    if (contenidoPrincipal) {
      Array.from(contenidoPrincipal.children).forEach((hijo) => {
        zonaDestino.appendChild(hijo);
      });
    } else {
      zonaDestino.innerHTML += contenido;
    }
  }
}

class CargadorSVG {
  constructor() {
    if (!this.comprobarApiFile()) {
      $("main").append("<p>Este navegador no soporta API File</p>");
    }
  }

  comprobarApiFile() {
    return window.File && window.FileReader && window.FileList && window.Blob;
  }

  leerArchivoSVG(files) {
    const archivo = files[0];

    if (!archivo) return;

    if (!archivo.type.includes("image/svg") && !archivo.name.endsWith(".svg")) {
      alert("Por favor, sube un archivo SVG válido.");
      return;
    }

    const lector = new FileReader();

    lector.onload = (evento) => {
      this.mostrarSVG(lector.result);
    };

    lector.readAsText(archivo);
  }

  mostrarSVG(datos) {
    const zonaDestino = $("main > section:nth-of-type(2) > section");

    zonaDestino.empty();

    const titulo = $("<h4>Gráfico de altimetría:</h4>");
    zonaDestino.append(titulo);

    zonaDestino.append(datos);
  }
}

class CargadorKML {
  constructor() {
    this.mapa = null;
    if (!this.comprobarApiFile()) {
      const main = document.querySelector("main");
      const errorP = document.createElement("p");
      errorP.textContent = "Este navegador no soporta API File para KML";
      main.appendChild(errorP);
    }
  }

  comprobarApiFile() {
    return window.File && window.FileReader && window.FileList && window.Blob;
  }

  leerArchivoKML(files) {
    const archivo = files[0];
    if (!archivo) return;

    if (!archivo.name.endsWith(".kml")) {
      alert("Por favor, sube un archivo .kml válido");
      return;
    }

    const lector = new FileReader();
    lector.onload = (evento) => {
      this.procesarKML(lector.result);
    };
    lector.readAsText(archivo);
  }

  procesarKML(xmlContent) {
    // 1. Parsear el KML (XML)
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xmlContent, "text/xml");

    // 2. Extraer coordenadas
    // Tu KML tiene varios Placemarks (Sector 1, Sector 2...), buscamos todas las coordenadas
    const coordenadasRaw = xmlDoc.querySelectorAll("coordinates");

    let puntosRuta = [];
    let centroMapa = null;

    // Recorremos CADA etiqueta <coordinates> (una por cada sector)
    coordenadasRaw.forEach((coordenadaItem) => {
      // Limpiamos saltos de línea y espacios extra que tiene tu KML
      // Tu KML usa saltos de línea para separar coordenadas, los convertimos a espacios
      let texto = coordenadaItem.textContent.trim().replace(/\s+/g, " ");

      const pares = texto.split(" ");

      // Procesamos cada par "lon,lat"
      pares.forEach((par) => {
        const coords = par.split(",");
        if (coords.length >= 2) {
          // MapBox espera [longitud, latitud] numéricos
          const punto = [parseFloat(coords[0]), parseFloat(coords[1])];
          puntosRuta.push(punto);

          // Guardamos el primer punto encontrado como centro del mapa
          if (!centroMapa) {
            centroMapa = punto;
          }
        }
      });
    });

    // Si no se encontraron puntos, salimos
    if (!centroMapa || puntosRuta.length === 0) return;

    this.mostrarMapa(centroMapa, puntosRuta);
  }

  mostrarMapa(centro, ruta) {
    mapboxgl.accessToken =
      "pk.eyJ1IjoiaXZhbnNhbHZhcmVzIiwiYSI6ImNtaWg2b3U0OTAxY3EzZHFxN3NpOHIybzkifQ._2c7ngeltesf0CzsV2FHiA";

    let contenedorMapa = document.querySelector("main > div");

    if (!contenedorMapa) {
      // Se usa div para el mapa dinámico
      contenedorMapa = document.createElement("div");
      document.querySelector("main").appendChild(contenedorMapa);
    }

    contenedorMapa.innerHTML = "";

    this.mapa = new mapboxgl.Map({
      container: contenedorMapa,
      style: "mapbox://styles/mapbox/satellite-streets-v12",
      center: centro,
      zoom: 14,
    });

    this.mapa.addControl(new mapboxgl.NavigationControl());

    this.mapa.on("load", () => {
      new mapboxgl.Marker({ color: "red" }).setLngLat(centro).addTo(this.mapa);

      if (ruta.length > 0) {
        this.mapa.addSource("ruta", {
          type: "geojson",
          data: {
            type: "Feature",
            properties: {},
            geometry: {
              type: "LineString",
              coordinates: ruta,
            },
          },
        });

        this.mapa.addLayer({
          id: "ruta",
          type: "line",
          source: "ruta",
          layout: {
            "line-join": "round",
            "line-cap": "round",
          },
          paint: {
            "line-color": "#ff0000",
            "line-width": 5,
          },
        });

        const bounds = new mapboxgl.LngLatBounds();
        ruta.forEach((coord) => bounds.extend(coord));
        this.mapa.fitBounds(bounds, { padding: 50 });
      }
    });
  }
}

$(function () {
  // Ejercicio 2
  const circuito = new Circuito();
  const inputHTML = document.querySelector(
    "main > section:nth-of-type(1) input"
  );
  if (inputHTML) {
    inputHTML.addEventListener("change", function () {
      circuito.leerArchivoHTML(this.files);
    });
  }

  // Ejercicio 2
  const cargadorSVG = new CargadorSVG();
  const inputSVG = document.querySelector(
    "main > section:nth-of-type(2) input"
  );
  if (inputSVG) {
    inputSVG.addEventListener("change", function () {
      cargadorSVG.leerArchivoSVG(this.files);
    });
  }

  // Ejercicio 3
  const cargadorKML = new CargadorKML();
  const inputKML = document.querySelector(
    "main > section:nth-of-type(3) input"
  );
  if (inputKML) {
    inputKML.addEventListener("change", function () {
      cargadorKML.leerArchivoKML(this.files);
    });
  }
});
