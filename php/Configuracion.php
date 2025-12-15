<?php
    require_once("BaseDatos.php");

    class Configuracion {
        private $db;

        public function __construct() {
            $this->db = new BaseDatos();
        }

        public function inicializar() {
            $conn = $this->db->getConexion();
        
            $sqlStructure = file_get_contents("crear-db-tablas.sql");

            $conn->query("DROP DATABASE IF EXISTS UO265217_DB");

            if ($conn->multi_query($sqlStructure)) {
                while ($conn->next_result()) {;}

                $this->db->seleccionarBD();

                $sqlData = file_get_contents("insertar-datos.sql");
                if ($conn->multi_query($sqlData)) {
                    while ($conn->next_result()) {;}
                    return "Base de datos reiniciada y dispositivos cargados correctamente";
                } else {
                    return "Tablas creadas, pero error cargando datos: " . $conn->error;
                }
            } else {
                return "Error creando la estructura: " . $conn->error;
            }
        }

        public function borrar() {
            $conn = $this->db->getConexion();

            $sql = "DROP DATABASE IF EXISTS UO265217_DB";

            if ($conn->query($sql) === TRUE) {
                return "Base de datos eliminada.";
            } else {
                return "Error al eliminar: " . $conn->error;
            }
        }

        public function exportar() {
            
        try {
            $this->db->seleccionarBD();
        } catch (Exception $e) {
            return "Error: La base de datos no existe. Inicialícela primero.";
        }

        $conn = $this->db->getConexion();
        
        if ($conn->connect_error) {
            return "Error de conexión: " . $conn->connect_error;
        }

        $sql = "SELECT p.id_prueba, 
                       u.profesion, u.edad, u.genero, u.pericia, 
                       d.nombre_dispositivo, 
                       p.tiempo_total, p.valoracion, p.puntuacion, p.completado, 
                       p.comentarios_usuario, p.propuestas_mejora,
                       o.comentario AS observacion_facilitador
                FROM pruebas_usabilidad p
                JOIN usuarios u ON p.id_usuario = u.id_usuario
                JOIN dispositivos d ON p.id_dispositivo = d.id_dispositivo
                LEFT JOIN observaciones o ON p.id_prueba = o.id_prueba";

        try {
            $resultado = $conn->query($sql);
        } catch (Exception $e) {
             return "Error al consultar: " . $e->getMessage();
        }

        if ($resultado && $resultado->num_rows > 0) {
            header('Content-Type: text/csv; charset=utf-8');
            header('Content-Disposition: attachment; filename=informe_usabilidad.csv');

            $output = fopen('php://output', 'w');
            
            fputcsv($output, array(
                'ID Prueba', 
                'Profesion', 
                'Edad', 
                'Genero', 
                'Pericia', 
                'Dispositivo', 
                'Tiempo (s)', 
                'Valoracion', 
                'Puntuacion',     
                'Completado', 
                'Comentarios Usuario', 
                'Propuestas Mejora',
                'Observaciones Facilitador'
            ));
            
            while ($fila = $resultado->fetch_assoc()) {
                fputcsv($output, $fila);
            }
            fclose($output);
            exit();
        } else {
            return "No hay datos para exportar.";
        }
    }
    }
?>