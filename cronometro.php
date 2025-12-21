<?php
    require_once("php/Cronometro.php");
    
    session_start();

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

<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>MotoGP Desktop - Cronómetro</title>

    <meta name="author" content="Iván Roque Álvarez Lamas" />
    <meta name="description" content="Cronómetro PHP MotoGP Desktop" />
    <meta name="keywords" content="MotoGP, Desktop, Cronómetro, PHP" />
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
        <a href="meteorologia.html" title="Datos meteorologicos">Meteorología</a>
        <a href="clasificaciones.php" title="Resultados y posiciones">Clasificaciones</a>
        <a class="active" href="juegos.html" title="Juegos y actividades">Juegos</a>
        <a href="ayuda.html" title="Ayuda del proyecto">Ayuda</a>
      </nav>
    </header>

    <p>
      <a href="index.html" title="Volver a la página de inicio">Inicio</a>
      > <a href="juegos.html" title="Volver a juegos">Juegos</a>
      > <strong>Cronómetro PHP</strong>
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
                    <input type="submit" name="mostrar" value="Mostrar" />
                    <input type="submit" name="reiniciar" value="Reiniciar" />
                </p>
            </form>
        </article>
      </section>
    </main>
  </body>
</html>