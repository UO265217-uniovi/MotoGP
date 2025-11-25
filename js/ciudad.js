// La ciudad es: Alcañiz

class Ciudad {
  #nombre;
  #pais;
  #gentilicio;
  #poblacion;
  #coordenadas;

  constructor(nombre, pais, gentilicio) {
    this.#nombre = nombre;
    this.#pais = pais;
    this.#gentilicio = gentilicio;
    this.#poblacion = null;
    this.#coordenadas = null;
  }

  setPoblacion(poblacion) {
    this.#poblacion = poblacion;
  }

  setCoordenadas(coordenadas) {
    this.#coordenadas = coordenadas;
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
    let parrafo = document.createElement("p");

    parrafo.textContent = `Coordenadas: ${this.#coordenadas}`;

    let sectionInformacionSecundaria = document.querySelector(
      "main section section"
    );

    sectionInformacionSecundaria.appendChild(parrafo);
  }
}
