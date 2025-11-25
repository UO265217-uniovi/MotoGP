class Memoria {
  #tablero_bloqueado;
  #primera_carta;
  #segunda_carta;
  #cronometro;

  constructor() {
    this.#tablero_bloqueado = true;
    this.#primera_carta = null;
    this.#segunda_carta = null;

    this.#cronometro = new Cronometro();

    this.barajarCartas();
    this.reiniciarAtributos();

    this.#cronometro.arrancar();
  }

  voltearCarta(carta) {
    if (this.#tablero_bloqueado) return;

    if (carta === this.#primera_carta) return;

    carta.setAttribute("data-estado", "volteada");

    if (this.#primera_carta === null) this.#primera_carta = carta;
    else {
      this.#segunda_carta = carta;
      this.comprobarPareja();
    }
  }

  barajarCartas() {
    const cartasNodeList = document.querySelectorAll("main article");

    const cartasArray = Array.from(cartasNodeList);

    for (let i = cartasArray.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));

      [cartasArray[i], cartasArray[j]] = [cartasArray[j], cartasArray[i]];
    }

    const main = document.querySelector("main");

    cartasArray.forEach((carta) => {
      main.appendChild(carta);
    });
  }

  reiniciarAtributos() {
    this.#tablero_bloqueado = false;

    this.#primera_carta = null;
    this.#segunda_carta = null;
  }

  deshabilitarCartas() {
    this.#primera_carta.setAttribute("data-estado", "revelada");
    this.#segunda_carta.setAttribute("data-estado", "revelada");

    this.comprobarJuego();
    this.reiniciarAtributos();
  }

  comprobarJuego() {
    const cartasReveladas = document.querySelectorAll(
      'main article[data-estado="revelada"]'
    );

    const totalCartas = document.querySelectorAll("main article");

    if (cartasReveladas.length === totalCartas.length) {
      this.#cronometro.parar();
    }
  }

  cubrirCartas() {
    this.#tablero_bloqueado = true;

    setTimeout(() => {
      if (this.#primera_carta && this.#segunda_carta) {
        this.#primera_carta.removeAttribute("data-estado");
        this.#segunda_carta.removeAttribute("data-estado");
      }

      this.reiniciarAtributos();
    }, 1000);
  }

  comprobarPareja() {
    const primera = this.#primera_carta.querySelector("img").src;
    const segunda = this.#segunda_carta.querySelector("img").src;

    primera === segunda ? this.deshabilitarCartas() : this.cubrirCartas();
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const memoria = new Memoria();

  const cartas = document.querySelectorAll("main article");

  cartas.forEach((carta) => {
    carta.addEventListener("click", function () {
      memoria.voltearCarta(carta);
    });
  });
});
