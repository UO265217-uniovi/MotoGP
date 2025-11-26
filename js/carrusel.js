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

  mostrarFotografias() {
    var header = $("<h2></h2>").text("Imágenes de " + this.#busqueda);

    var img = $("<img>")
      .attr("src", this.#fotos[this.#actual])
      .attr("alt", "Imagen de " + this.#busqueda);

    var article = $("<article></article>").append(header).append(img);

    $("main").append(article);

    setInterval(this.cambiarFotografia.bind(this), 3000);
  }

  cambiarFotografia() {
    this.#actual++;

    if (this.#actual >= this.#fotos.length) {
      this.#actual = 0;
    }

    $("article img").attr("src", this.#fotos[this.#actual]);
  }
}
document.addEventListener("DOMContentLoaded", function () {
  let miCarrusel = new Carrusel("MotorLand Aragon");
  miCarrusel.getFotografias();
});
