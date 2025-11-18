class Memoria {
  constructor() {
    this.tablero_bloqueado = true;
    this.primera_carta = null;
    this.segunda_carta = null;
  }

  voltearCarta(carta) {
    carta.setAttribute("data-estado", "volteada");
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
    this.tablero_bloqueado = false;

    this.primera_carta = null;
    this.segunda_carta = null;
  }

  deshabilitarCartas() {
    this.primera_carta.setAttribute("data-estado", "revelada");
    this.segunda_carta.setAttribute("data-estado", "revelada");

    this.comprobarJuego();
    this.reiniciarAtributos();
  }

  comprobarJuego() {
    const cartasReveladas = document.querySelectorAll(
      'main article[data-estado="revelada"]'
    );

    const totalCartas = document.querySelectorAll("main article");

    if (cartasReveladas.length === totalCartas.length) {
      alert("HAS GANADO!");
    }
  }
}
