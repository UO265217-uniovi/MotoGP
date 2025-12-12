<!DOCTYPE html>

<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>MotoGP - Clasificaciones</title>

    <meta name="author" content="Iván Roque Álvarez Lamas" />
    <meta name="description" content="Clasificaciones MotoGP Desktop" />
    <meta name="keywords" content="MotoGP, Desktop, Clasificaciones" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <link rel="stylesheet" type="text/css" href="estilo/estilo.css" />
    <link rel="stylesheet" type="text/css" href="estilo/layout.css" />

    <link rel="icon" href="multimedia/favicon.ico" type="image/x-icon" />
  </head>

  <body>
    <header>
      <h1><a href="index.html">MotoGP Desktop</a></h1>
      <nav>
        <a href="index.html" title="Página de inicio">Inicio</a>
        <a href="piloto.html" title="Información del piloto">Piloto</a>
        <a href="circuito.html" title="Circuito del mundial">Circuito</a>
        <a href="meteorologia.html" title="Datos meteorologicos"
          >Meteorología</a
        >
        <a
          class="active"
          href="clasificaciones.php"
          title="Resultados y posiciones"
          >Clasificaciones</a
        >
        <a href="juegos.html" title="Juegos y actividades">Juegos</a>
        <a href="ayuda.html" title="Ayuda del proyecto">Ayuda</a>
      </nav>
    </header>
    <p>
      <a href="index.html" title="Volver a la página de inicio">Inicio</a>
      > <strong>Clasificaciones</strong>
    </p>
    <main>
      <section>
        <h2>Clasificaciones MotoGP Desktop</h2>
        <?php 
          class Clasificacion {
            protected $documento;
            protected $xml;

            public function __construct($ruta) {
              $this->documento = $ruta;
            }

            public function consultar() {
              if (file_exists($this->documento)) {
                $this->xml = simplexml_load_file($this->documento);
              } else {
                echo "<p>Error: No se encuentra el archivo XML</p>";
              }
            }

            public function mostrarGanador() {
              if ($this->xml) {
                $vencedor = $this->xml->vencedor;

                echo "<article>";
                echo "<h3> Ganador de la Carrera </h3>";
                echo "<p><strong>Piloto: </strong>" . $vencedor->nombre . "</p>";
                echo "<p><strong>Tiempo: </strong>" . $vencedor->tiempo_carrera . "</p>";
                echo "</article>";
              }
            }

            public function mostrarClasificacion() {
              if ($this->xml) {
                echo "<article>";
                echo "<h3>Clasificación General</h3>";
                echo "<ul>";

                foreach ($this->xml->clasificados->clasificacion_participante as $participante) {
                  echo "<li>";
                  echo "<strong>" . $participante->nombre . "</strong>: " . $participante->puntos . " puntos";
                  echo "</li>";
                }

                echo "</ul>";
                echo "</article>";
              }
            }
          }

          $clasificacion = new Clasificacion("xml/circuitoEsquema.xml");

          $clasificacion->consultar();

          $clasificacion->mostrarGanador();
          $clasificacion->mostrarClasificacion();
        ?>
      </section>
    </main>
  </body>
</html>
