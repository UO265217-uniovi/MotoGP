// La ciudad es: Alcañiz

class Ciudad {
    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre;
        this.pais = pais;
        this.gentilicio = gentilicio;
        this.poblacion = null;
        this.coordenadas = null;
    }

    setPoblacion(poblacion) {
        this.poblacion = poblacion;
    }

    setCoordenadas(coordenadas) {
        this.coordenadas = coordenadas;
    }

    getNombre() {
        return this.nombre;
    }

    getPais() {
        return this.pais;
    }

    getInformacionSecundaria() {
        return (
        `<ul>
            <li>${this.gentilicio}</li>
            <li>${this.poblacion}</li>
        </ul>`
        );
    }

    escribirCoordenadas() {
    document.write(`<p>Coordenadas: ${this.coordenadas}</p>`);
  }
}