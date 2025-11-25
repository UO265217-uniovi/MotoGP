class Carrusel {
  #busqueda;
  #actual;
  #maximo;
  #fotos;

  constructor(circuito) {
    this.#busqueda = circuito;
    this.#actual = 0;
    this.#maximo = 4;
    this.#fotos = [];
  }

  getFotografias() {
    const flickrAPI =
      "https://api.flickr.com/services/feeds/photos_public.gne?jsoncallback=?";

    $.getJSON(flickrAPI, {
      tags: this.#busqueda,
      tagmode: "any",
      format: "json",
    }).done(this.procesarJSONFotografias.bind(this));
  }

  procesarJSONFotografias(data) {
    let items = data.items;

    this.#fotos = [];

    if (!items || items.length === 0) return;

    let nFotos = Math.min(5, items.length);

    for (let i = 0; i < nFotos; i++) {
      let item = items[i];

      let url640 = item.media.m.replace("_m.jpg", "_z.jpg");

      this.#fotos.push(url640);
    }

    if (this.#fotos.length > 0) this.mostrarFotografias();
  }

  // Tarea 7: Añadir la información al index.html
  mostrarFotografias() {
    // Creamos el contenedor y los elementos
    // Usamos un selector específico para que no se duplique si llamamos varias veces
    // (aunque en este ejercicio solo se llama una vez)

    var header = $("<h2></h2>").text("Imágenes de " + this.#busqueda);

    var img = $("<img>")
      .attr("src", this.#fotos[this.#actual])
      .attr("alt", "Imagen de " + this.#busqueda);

    var article = $("<article></article>").append(header).append(img);

    // Añadimos después del h1 o donde indique tu diseño, el guion dice en el documento.
    // Una buena práctica es añadirlo a un contenedor main o section existente.
    // Si no, al final del body:
    $("main").append(article);

    // Tarea 8: Iniciar el temporizador (3 segundos)
    setInterval(this.cambiarFotografia.bind(this), 3000);
  }

  // Tarea 8: Cambio de imagen cíclico
  cambiarFotografia() {
    // Avanzamos el índice
    this.#actual++;

    // Si superamos el número de fotos disponibles, volvemos a 0
    if (this.#actual >= this.#fotos.length) {
      this.#actual = 0;
    }

    // Actualizamos el atributo src de la imagen ya existente en el DOM
    // Selector: busca la imagen que está dentro de un article
    $("article img").attr("src", this.#fotos[this.#actual]);
  }
}

// Instanciación
document.addEventListener("DOMContentLoaded", function () {
  let miCarrusel = new Carrusel("MotorLand Aragon"); // Usa tu circuito asignado
  miCarrusel.getFotografias();
});
