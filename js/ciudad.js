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

document.addEventListener("DOMContentLoaded", function () {
  const ciudad = new Ciudad("Alcañiz", "España", "alcañizano/a");

  ciudad.setPoblacion(16241);
  ciudad.setCoordenadas("41.0500, -0.1333");

  // Seccion principal
  const main = document.querySelector("main");

  // Creación de la seccion de info ciudad y sus componentes
  const infoCiudad = document.createElement("section");

  // Componentes
  const headerCiudad = document.createElement("h3");
  const pPais = document.createElement("p");

  const seccionInformacionSecundaria = document.createElement("section");
  const headerInformacionSecundaria = document.createElement("h4");

  // Añanadir información a los componentes
  headerCiudad.textContent = `Información de ${ciudad.getNombre()}`;
  pPais.textContent = `País: ${ciudad.getPais()}`;
  headerInformacionSecundaria.textContent = "Información secundaria";

  seccionInformacionSecundaria.appendChild(headerInformacionSecundaria);
  seccionInformacionSecundaria.innerHTML += ciudad.getInformacionSecundaria();

  // Mostrar componentes
  infoCiudad.appendChild(headerCiudad);
  infoCiudad.appendChild(pPais);
  infoCiudad.appendChild(seccionInformacionSecundaria);

  main.appendChild(infoCiudad);

  ciudad.escribirCoordenadas();
});
