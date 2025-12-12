<?php
    session_start();

    class Cronometro {
        private $inicio;
        private $tiempo;

        public function __construct() {
            $this->inicio = 0;
            $this->tiempo = 0;
        }

        public function arrancar() {
            if ($this->inicio == 0) {
                $this->inicio = microtime(true);
            }
        }

        public function parar() {
            if ($this->inicio != 0) {
                $parada = microtime(true);
                $this->tiempo += ($parada - $this->inicio);
                $this->inicio = 0;
            }
        }

        public function mostrar() {
            $tiempoTotal = $this->tiempo;
            if ($this->inicio != 0) {
                $tiempoTotal += microtime(true) - $this->inicio;
            }

            $segundosTotales = floor($tiempoTotal);
            $minutos = floor($segundosTotales / 60);
            $segundos = $segundosTotales % 60;

            $decimas = floor(($tiempoTotal - $segundosTotales) * 10);

            return sprintf("%02d:%02d.%d", $minutos, $segundos, $decimas);
        }

        public function reiniciar() {
            $this->inicio = 0;
            $this->tiempo = 0;
        }
    }

    if (!isset($_SESSION["cronometro"])) {
        $_SESSION["cronometro"] = new Cronometro();
    }

    $cronometro = $_SESSION["cronometro"];

    if (isset($_POST["arrancar"])) {
        $cronometro->arrancar();
    }

    if (isset($_POST["parar"])) {
        $cronometro->parar();
    }

    if (isset($_POST["reiniciar"])) {
        $cronometro->reiniciar();
    }

    $_SESSION["cronometro"] = $cronometro;
?>

<!DOCTYPE HTML>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>MotoGP Desktop - Cronómetro</title>
    <link rel="stylesheet" type="text/css" href="estilo/estilo.css" />
    <link rel="stylesheet" type="text/css" href="estilo/layout.css" />
</head>
<body>
    <header>
        <h1>MotoGP Desktop</h1>
        <nav>
            <a href="index.html">Inicio</a>
            <a href="piloto.html">Piloto</a>
            <a href="circuito.html">Circuito</a>
            <a href="meteorologia.html">Meteorología</a>
            <a href="clasificaciones.php">Clasificaciones</a>
            <a href="juegos.html" class="active">Juegos</a>
            <a href="cronometro.php">Cronómetro</a>
        </nav>
    </header>
    
    <p>
      <a href="index.html" title="Volver a la página de inicio">Inicio</a>
      >
      <a href="juegos.html" title="Volver a la página de juegos">Juegos</a>
      >
      <strong>Cronómetro PHP</strong>
    </p>
    
    <main>
        <section>
            <h2>Cronómetro PHP</h2>
            
            <article>
                <h3>Tiempo Transcurrido</h3>
                <p>
                    <?php echo $cronometro->mostrar(); ?>
                </p>
            </article>

            <article>
                <h3>Controles</h3>
                <form action="cronometro.php" method="post">
                    <p>
                        <input type="submit" name="arrancar" value="Arrancar" />
                        <input type="submit" name="parar" value="Parar" />
                        <input type="submit" name="mostrar" value="Mostrar / Actualizar" />
                        <input type="submit" name="reiniciar" value="Reiniciar" />
                    </p>
                </form>
            </article>
        </section>
    </main>
</body>
</html>