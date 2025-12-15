<?php
    require_once("configuracion.php");
    $mensaje = "";

    if (isset($_POST["crear"])) {
        $gestor = new Configuracion();
        $mensaje = $gestor->inicializar();
    }

    if (isset($_POST["borrar"])) {
        $gestor = new Configuracion();
        $mensaje = $gestor->borrar();
    }

    if (isset($_POST["exportar"])) {
        $gestor = new Configuracion();
        $mensaje = $gestor->exportar();
    }
?>
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>MotoGP - Configuración BD</title>

    <meta name="author" content="Iván Roque Álvarez Lamas" />
    <meta name="description" content="Configuración Base de Datos MotoGP Desktop" />
    <meta name="keywords" content="MotoGP, Desktop, Configuración, SQL, PHP" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <link rel="stylesheet" type="text/css" href="../estilo/estilo.css" />
    <link rel="stylesheet" type="text/css" href="../estilo/layout.css" />

    <link rel="icon" href="../multimedia/favicon.ico" type="image/x-icon" />
  </head>

  <body>
    <header>
      <h1><a href="../index.html">MotoGP Desktop</a></h1>
    </header>

    <p>
      <a href="../index.html" title="Volver a la página de inicio">Inicio</a>
      > <a href="../juegos.html" title="Volver a juegos">Juegos</a>
      > <strong>Configuración BD</strong>
    </p>

    <main>
      <h2>Configuración de Base de Datos</h2>

      <?php if (!empty($mensaje)) { ?>
          <section>
             <h3>Estado de la operación</h3>
             <p><strong><?php echo $mensaje; ?></strong></p>
          </section>
      <?php } ?>

      <section>
        <h3>Operaciones Disponibles</h3>
        <p>Seleccione una opción para gestionar la base de datos del proyecto:</p>

        <form action="#" method="post">
            <article>
                <h4>Inicialización</h4>
                <p>Crea las tablas necesarias y carga los datos iniciales (Dispositivos).</p>
                <input type="submit" name="crear" value="Crear / Reiniciar Base de Datos" />
            </article>

            <article>
                <h4>Exportación de Datos</h4>
                <p>Descarga un archivo CSV con todos los resultados de las pruebas de usabilidad.</p>
                <input type="submit" name="exportar" value="Exportar Datos a CSV" />
            </article>

            <article>
                <h4>Borrado Completo</h4>
                <p>Elimina la base de datos y todos los registros almacenados.</p>
                <input type="submit" name="borrar" value="Eliminar Base de Datos" />
            </article>
        </form>
      </section>
    </main>
  </body>
</html>