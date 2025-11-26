// La ciudad es: Alcañiz

class Ciudad {
  #nombre;
  #pais;
  #gentilicio;
  #poblacion;
  #latitud;
  #longitud;

  constructor(nombre, pais, gentilicio) {
    this.#nombre = nombre;
    this.#pais = pais;
    this.#gentilicio = gentilicio;
    this.#poblacion = null;
    this.#longitud = null;
    this.#latitud = null;
  }

  setPoblacion(poblacion) {
    this.#poblacion = poblacion;
  }

  setCoordenadas(latitud, longitud) {
    this.#latitud = latitud;
    this.#longitud = longitud;
  }

  getNombre() {
    return this.#nombre;
  }

  getPais() {
    return this.#pais;
  }

  getInformacionSecundaria() {
    return `<ul>
            <li>${this.#gentilicio}</li>
            <li>${this.#poblacion}</li>
        </ul>`;
  }

  escribirCoordenadas() {
    $("main section section").append(
      `<p>Coordenadas: ${this.#latitud}, ${this.#longitud}</p>`
    );
  }

  getMeteorologiaCarrera() {
    const fechaCarrera = "2025-06-08";

    const url = `https://archive-api.open-meteo.com/v1/archive?latitude=${
      this.#latitud
    }&longitude=${
      this.#longitud
    }&start_date=${fechaCarrera}&end_date=${fechaCarrera}&hourly=temperature_2m,relative_humidity_2m,apparent_temperature,rain,wind_speed_10m,wind_direction_10m&daily=sunrise,sunset&timezone=auto`;

    $.ajax({
      dataType: "json",
      url: url,
      method: "GET",
      success: (data) => {
        this.#procesarJSONCarrera(data);
      },
      error: (jqXHR, textStatus, errorThrown) => {
        console.error("Error API Carrera:", textStatus, errorThrown);
        $("main").append(
          "<p>No se pudieron cargar los datos de la carrera.</p>"
        );
      },
    });
  }

  #procesarJSONCarrera(data) {
    const $seccion = $("<section></section>");
    $seccion.append("<h3>Meteorología: Día de la Carrera (8 Junio 2025)</h3>");

    // Datos diarios (Sol)
    const daily = data.daily;
    // La API devuelve fechas tipo "2025-06-08T06:30", hacemos split para sacar la hora
    const salidaSol = daily.sunrise[0].split("T")[1];
    const puestaSol = daily.sunset[0].split("T")[1];

    $seccion.append(
      `<p><strong>Salida del sol:</strong> ${salidaSol} | <strong>Puesta del sol:</strong> ${puestaSol}</p>`
    );

    const hourly = data.hourly;
    const $contenedorHorario = $("<article></article>");
    $contenedorHorario.append("<h4>Previsión por horas (09:00 - 16:00)</h4>");

    const $listaHoras = $("<ul></ul>");

    hourly.time.forEach((timeStr, i) => {
      const horaCompleta = timeStr.split("T")[1];
      const horaNum = parseInt(horaCompleta.split(":")[0]);

      if (horaNum >= 9 && horaNum <= 16) {
        let temp = hourly.temperature_2m[i];
        let sensacion = hourly.apparent_temperature[i];
        let humedad = hourly.relative_humidity_2m[i];
        let lluvia = hourly.rain[i];
        let vientoVel = hourly.wind_speed_10m[i];
        let vientoDir = hourly.wind_direction_10m[i];

        let itemLista = `
            <li>
              <strong>${horaCompleta}:</strong> 
                <ul>
                  <li>Temp: ${temp}°C (Sens: ${sensacion}°C)</li> 
                  <li>Lluvia: ${lluvia} mm</li>
                  <li>Humedad: ${humedad}%</li>
                  <li>Viento: ${vientoVel} km/h (${vientoDir}°)</li>
                </ul>
            </li>
        `;
        $listaHoras.append(itemLista);
      }
    });

    $contenedorHorario.append($listaHoras);
    $seccion.append($contenedorHorario);
    $("main").append($seccion);
  }

  getMeteorologiaEntrenos() {
    const fechaInicio = "2025-06-05"; // Jueves
    const fechaFin = "2025-06-07"; // Sábado

    const url = `https://archive-api.open-meteo.com/v1/archive?latitude=${
      this.#latitud
    }&longitude=${
      this.#longitud
    }&start_date=${fechaInicio}&end_date=${fechaFin}&hourly=temperature_2m,relative_humidity_2m,rain,wind_speed_10m&timezone=auto`;

    $.ajax({
      dataType: "json",
      url: url,
      method: "GET",
      success: (data) => {
        this.#procesarJSONEntrenos(data);
      },
      error: (jqXHR, textStatus, errorThrown) => {
        console.error("Error API Entrenos:", textStatus, errorThrown);
      },
    });
  }

  #procesarJSONEntrenos(data) {
    const hourly = data.hourly;

    let resumenDias = {};

    // Recorremos todas las horas devueltas (72 horas aprox)
    hourly.time.forEach((fechaHora, i) => {
      let dia = fechaHora.split("T")[0];

      if (!resumenDias[dia]) {
        resumenDias[dia] = {
          sumaTemp: 0,
          sumaHum: 0,
          sumaLluvia: 0,
          sumaViento: 0,
          conteo: 0,
        };
      }

      resumenDias[dia].sumaTemp += hourly.temperature_2m[i];
      resumenDias[dia].sumaHum += hourly.relative_humidity_2m[i];
      resumenDias[dia].sumaLluvia += hourly.rain[i];
      resumenDias[dia].sumaViento += hourly.wind_speed_10m[i];
      resumenDias[dia].conteo++;
    });

    const $seccion = $("<section></section>");
    $seccion.append("<h3>Meteorología: Medias Entrenamientos (5-7 Junio)</h3>");

    for (let dia in resumenDias) {
      let datos = resumenDias[dia];
      let n = datos.conteo;

      let mediaTemp = (datos.sumaTemp / n).toFixed(2);
      let mediaHum = (datos.sumaHum / n).toFixed(2);
      let mediaLluvia = (datos.sumaLluvia / n).toFixed(2);
      let mediaViento = (datos.sumaViento / n).toFixed(2);

      let htmlDia = `
                <article>
                    <h4>Resumen del día ${dia}</h4>
                    <ul>
                      <li>Temp. Media: ${mediaTemp} °C</li>
                      <li>Humedad Media: ${mediaHum} %</li>
                      <li>Lluvia Media: ${mediaLluvia} mm</li>
                      <li>Viento Medio: ${mediaViento} km/h</li>
                    </ul>
                </article>
            `;
      $seccion.append(htmlDia);
    }

    $seccion.append($seccion);
    $("main").append($seccion);
  }
}

$(function () {
  const ciudad = new Ciudad("Alcañiz", "España", "alcañizano/a");

  ciudad.setPoblacion(16241);

  ciudad.setCoordenadas(41.05, -0.1333);

  const $main = $("main");
  const $infoCiudad = $("<section></section>");

  // Header Ciudad
  $infoCiudad.append(`<h3>Información de ${ciudad.getNombre()}</h3>`);
  $infoCiudad.append(`<p>País: ${ciudad.getPais()}</p>`);

  // Info Secundaria
  const $secundaria = $("<section></section>");
  $secundaria.append("<h4>Información secundaria</h4>");
  $secundaria.append(ciudad.getInformacionSecundaria()); // Inserta el string HTML devuelto

  $infoCiudad.append($secundaria);
  $main.append($infoCiudad);

  // Escribir coordenadas
  ciudad.escribirCoordenadas();

  ciudad.getMeteorologiaCarrera();
  ciudad.getMeteorologiaEntrenos();
});
