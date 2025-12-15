<?php
// 1. IMPORTANTE: Cargar clases antes de iniciar la sesión
require_once('BaseDatos.php');
require_once('Cronometro.php');

session_start();

$paso = isset($_POST['paso']) ? $_POST['paso'] : 'inicio';
$mensaje = "";

// --- LÓGICA DE CONTROL ---

if ($paso == 'cuestionario') {
    // FASE 1 -> 2: Guardamos datos del usuario (Sin ID, es anónimo)
    $_SESSION['datos_usuario'] = [
        'profesion' => $_POST['profesion'],
        'edad' => $_POST['edad'],
        'genero' => $_POST['genero'],
        'pericia' => $_POST['pericia'],
        'dispositivo' => $_POST['dispositivo']
    ];
    
    // Arrancamos el cronómetro
    if (!isset($_SESSION['crono_test'])) {
        $_SESSION['crono_test'] = new Cronometro();
    }
    $_SESSION['crono_test']->arrancar();
}

elseif ($paso == 'finalizar') {
    // FASE 2 -> 3: El usuario contestó. Calculamos nota y paramos tiempo.
    
    // 1. Parar Cronómetro
    if (isset($_SESSION['crono_test'])) {
        $crono = $_SESSION['crono_test'];
        $crono->parar();
        $_SESSION['tiempo_final'] = $crono->getSeconds();
        unset($_SESSION['crono_test']);
    } else {
        $_SESSION['tiempo_final'] = 0;
    }

    // 2. CORRECCIÓN AUTOMÁTICA
    // Recuperamos las respuestas del formulario
    $respuestasUsuario = isset($_POST['respuestas']) ? $_POST['respuestas'] : [];
    
    try {
        $bd = new BaseDatos();
        $conn = $bd->getConexion();
        $bd->seleccionarBD();

        // Obtenemos las soluciones correctas de la BD
        $sqlSoluciones = "SELECT id, correcta FROM preguntas";
        $result = $conn->query($sqlSoluciones);
        
        $aciertos = 0;
        $detalleRespuestas = []; // Array para guardar cada respuesta individualmente

        if ($result) {
            while ($row = $result->fetch_assoc()) {
                $idPreg = $row['id'];
                $correcta = $row['correcta'];
                
                // ¿Qué contestó el usuario a esta pregunta?
                $respuestaUser = isset($respuestasUsuario[$idPreg]) ? $respuestasUsuario[$idPreg] : null;
                $esCorrecta = ($respuestaUser === $correcta);

                if ($esCorrecta) {
                    $aciertos++;
                }

                // Guardamos el detalle para insertarlo luego en la BD
                if ($respuestaUser) {
                    $detalleRespuestas[] = [
                        'id_pregunta' => $idPreg,
                        'escogida' => $respuestaUser,
                        'es_correcta' => $esCorrecta
                    ];
                }
            }
        }
        
        // Guardamos la nota y el detalle en la sesión para el paso 'guardar'
        $_SESSION['puntuacion_test'] = $aciertos;
        $_SESSION['detalle_respuestas'] = $detalleRespuestas;

    } catch (Exception $e) {
        $_SESSION['puntuacion_test'] = 0;
        $_SESSION['detalle_respuestas'] = [];
    }
}

elseif ($paso == 'guardar') {
    // FASE 3 -> FIN: Guardamos TODO en la Base de Datos
    try {
        $bd = new BaseDatos();
        $conn = $bd->getConexion();
        $bd->seleccionarBD();

        // 1. Insertar Usuario (El ID se genera solo)
        $sqlUser = "INSERT INTO usuarios (profesion, edad, genero, pericia) VALUES (?, ?, ?, ?)";
        $stmt = $conn->prepare($sqlUser);
        $d = $_SESSION['datos_usuario'];
        $stmt->bind_param("sisi", $d['profesion'], $d['edad'], $d['genero'], $d['pericia']);
        
        if ($stmt->execute()) {
            $idUsuario = $conn->insert_id; // Obtenemos el ID generado
            $stmt->close();

            // 2. Insertar Prueba de Usabilidad (Con Puntuación y Tiempo)
            $sqlPrueba = "INSERT INTO pruebas_usabilidad (id_usuario, id_dispositivo, tiempo_total, completado, comentarios_usuario, propuestas_mejora, valoracion, puntuacion) VALUES (?, ?, ?, ?, ?, ?, ?, ?)";
            $stmt2 = $conn->prepare($sqlPrueba);
            
            $tiempo = $_SESSION['tiempo_final'];
            $completado = 1; 
            $comentarios = $_POST['comentarios'];
            $propuestas = $_POST['propuestas'];
            $valoracion = $_POST['valoracion'];
            $puntuacion = $_SESSION['puntuacion_test'];
            $idDisp = $d['dispositivo'];
            
            $stmt2->bind_param("iidissii", $idUsuario, $idDisp, $tiempo, $completado, $comentarios, $propuestas, $valoracion, $puntuacion);
            
            if ($stmt2->execute()) {
                $idPrueba = $conn->insert_id; // Obtenemos el ID de la prueba
                $stmt2->close();

                // 3. Insertar Observaciones del Facilitador
                $obs = $_POST['observaciones'];
                if (!empty($obs)) {
                    $sqlObs = "INSERT INTO observaciones (id_prueba, comentario) VALUES (?, ?)";
                    $stmt3 = $conn->prepare($sqlObs);
                    $stmt3->bind_param("is", $idPrueba, $obs);
                    $stmt3->execute();
                    $stmt3->close();
                }

                // 4. Insertar DETALLE de respuestas (Tabla respuestas_usuario)
                if (isset($_SESSION['detalle_respuestas'])) {
                    $sqlDetalle = "INSERT INTO respuestas_usuario (id_prueba, id_pregunta, respuesta_escogida, es_correcta) VALUES (?, ?, ?, ?)";
                    $stmtDetalle = $conn->prepare($sqlDetalle);
                    
                    foreach ($_SESSION['detalle_respuestas'] as $resp) {
                        $esCorrectaInt = $resp['es_correcta'] ? 1 : 0;
                        $stmtDetalle->bind_param("iisi", $idPrueba, $resp['id_pregunta'], $resp['escogida'], $esCorrectaInt);
                        $stmtDetalle->execute();
                    }
                    $stmtDetalle->close();
                }

                $mensaje = "¡Resultados guardados correctamente!";
                $paso = 'exito';
            } else {
                $mensaje = "Error al guardar prueba: " . $conn->error;
            }
        } else {
            $mensaje = "Error al guardar usuario: " . $conn->error;
        }
        $bd->cerrar();
    } catch (Exception $e) {
        $mensaje = "Excepción: " . $e->getMessage();
    }
}
?>

<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <title>MotoGP - Test de Usabilidad</title>

    <meta name="author" content="Iván Roque Álvarez Lamas" />
    <meta name="description" content="Test de Usabilidad MotoGP Desktop" />
    <meta name="keywords" content="MotoGP, Desktop, Test, Usabilidad" />
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
      > <strong>Test de Usabilidad</strong>
    </p>
    
    <main>
      
      <?php if ($paso == 'inicio') { ?>
      <section>
        <h2>Datos del Participante</h2>
        <p>Por favor, indique sus datos demográficos antes de comenzar (Anónimo).</p>
        <form action="#" method="post">
            <input type="hidden" name="paso" value="cuestionario">
            
            <p>
                <label>Edad: 
                    <input type="number" name="edad" min="12" max="100" required>
                </label>
            </p>
            <p>
                <label>Género: 
                    <select name="genero">
                        <option value="Hombre">Hombre</option>
                        <option value="Mujer">Mujer</option>
                        <option value="Otro">Otro</option>
                    </select>
                </label>
            </p>
            <p>
                <label>Profesión: 
                    <input type="text" name="profesion" required>
                </label>
            </p>
            <p>
                <label>Pericia Informática (0-10): 
                    <input type="number" name="pericia" min="0" max="10" required>
                </label>
            </p>
            <p>
                <label>Dispositivo de la prueba: 
                    <select name="dispositivo">
                        <option value="1">Ordenador</option>
                        <option value="2">Tableta</option>
                        <option value="3">Teléfono Móvil</option>
                    </select>
                </label>
            </p>
            
            <input type="submit" value="Comenzar Prueba">
        </form>
      </section>
      <?php } ?>

      <?php if ($paso == 'cuestionario') { ?>
      <section>
        <h2>Cuestionario</h2>
        <p>Responda a las siguientes preguntas seleccionando la opción correcta.</p>
        <form action="#" method="post">
            <input type="hidden" name="paso" value="finalizar">
            
            <?php
            try {
                $bd = new BaseDatos();
                $conn = $bd->getConexion();
                $bd->seleccionarBD();
                
                // Leemos las preguntas
                $sql = "SELECT * FROM preguntas";
                $result = $conn->query($sql);

                if ($result && $result->num_rows > 0) {
                    $contador = 1;
                    while($row = $result->fetch_assoc()) {
                        echo "<fieldset>";
                        echo "<legend>Pregunta " . $contador . "</legend>";
                        echo "<p><strong>" . $row['enunciado'] . "</strong></p>";
                        
                        // Generamos los radio buttons dinámicamente
                        // name="respuestas[ID]" para luego saber cuál es cuál
                        echo '<label><input type="radio" name="respuestas['.$row['id'].']" value="a" required> a) ' . $row['respuesta_a'] . '</label><br>';
                        echo '<label><input type="radio" name="respuestas['.$row['id'].']" value="b"> b) ' . $row['respuesta_b'] . '</label><br>';
                        echo '<label><input type="radio" name="respuestas['.$row['id'].']" value="c"> c) ' . $row['respuesta_c'] . '</label><br>';
                        echo '<label><input type="radio" name="respuestas['.$row['id'].']" value="d"> d) ' . $row['respuesta_d'] . '</label><br>';
                        
                        echo "</fieldset>";
                        $contador++;
                    }
                } else {
                    echo "<p>No hay preguntas cargadas en la base de datos.</p>";
                }
            } catch (Exception $e) {
                echo "<p>Error cargando preguntas: " . $e->getMessage() . "</p>";
            }
            ?>

            <p><input type="submit" value="Terminar Prueba"></p>
        </form>
      </section>
      <?php } ?>

      <?php if ($paso == 'finalizar') { ?>
      <section>
        <h2>Prueba Finalizada</h2>
        <p>Ha acertado <strong><?php echo $_SESSION['puntuacion_test']; ?></strong> preguntas.</p>
        <p>Por favor, complete la valoración final para guardar los resultados.</p>
        
        <form action="#" method="post">
            <input type="hidden" name="paso" value="guardar">
            
            <fieldset>
                <legend>Opinión del Usuario</legend>
                <p>
                    <label>Valoración de la aplicación (0-10):
                        <input type="number" name="valoracion" min="0" max="10" required>
                    </label>
                </p>
                <p>
                    <label>Comentarios generales:<br>
                        <textarea name="comentarios" rows="3" cols="50"></textarea>
                    </label>
                </p>
                <p>
                    <label>Propuestas de mejora:<br>
                        <textarea name="propuestas" rows="3" cols="50"></textarea>
                    </label>
                </p>
            </fieldset>

            <fieldset>
                <legend>Área del Facilitador</legend>
                <p>
                    <label>Observaciones sobre la prueba:<br>
                        <textarea name="observaciones" rows="3" cols="50"></textarea>
                    </label>
                </p>
            </fieldset>

            <input type="submit" value="Guardar Resultados">
        </form>
      </section>
      <?php } ?>

      <?php if ($paso == 'exito') { ?>
      <section>
        <h2>Operación Completada</h2>
        <p><?php echo $mensaje; ?></p>
        <p>Gracias por su colaboración.</p>
        <p><button onclick="window.close()">Cerrar Ventana</button></p>
      </section>
      <?php } ?>

    </main>
  </body>
</html>