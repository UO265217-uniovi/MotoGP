class Noticias {
  #apikey;
  #busqueda;
  #url;

  constructor() {
    this.#apikey = "FPV4XSEPozfnaqmwV0PwfrichDkFTJ3NNnBwOV10";
    this.#busqueda = "MotoGP";
    this.#url = "https://api.thenewsapi.com/v1/news/all";
  }

  buscar() {
    const urlSolicitud = `${this.#url}?api_token=${this.#apikey}&search=${
      this.#busqueda
    }&language=es,en&limit=5`;

    fetch(urlSolicitud)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Error en la respuesta de la red");
        }
        return response.json();
      })
      .then((data) => {
        this.#procesarJSON(data);
      })
      .catch((error) => {
        console.error("Error fetch:", error);
        $("main").append(
          "<aside>Error: No se han podido recuperar las noticias. Compruebe su conexión o la clave API.</aside>"
        );
      });
  }

  #procesarJSON(data) {
    if (!data || !data.data || data.data.length === 0) return;

    const $seccion = $("<section></section>");

    $seccion.append("<h3>Últimas Noticias de MotoGP</h3>");

    data.data.forEach((noticia) => {
      const titulo = noticia.title;
      const descripcion = noticia.description;
      const urlNoticia = noticia.url;
      const fuente = noticia.source;

      const $articulo = $("<article></article>");

      $articulo.append(`<h4>${titulo}</h4>`);

      $articulo.append(`<p><strong>Fuente:</strong> ${fuente}</p>`);
      $articulo.append(`<p>${descripcion}</p>`);

      $articulo.append(
        `<a href="${urlNoticia}" target="_blank">Leer noticia completa</a>`
      );

      $seccion.append($articulo);
    });

    $("main").append($seccion);
  }
}

$(function () {
  const noticias = new Noticias();
  noticias.buscar();
});
