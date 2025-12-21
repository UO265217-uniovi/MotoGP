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

            // Obtener todas las tablas
            $tablasResult = $conn->query("SHOW TABLES");
            if (!$tablasResult) {
                return "Error al obtener tablas: " . $conn->error;
            }

            if ($tablasResult->num_rows > 0) {
                header('Content-Type: text/csv; charset=utf-8');
                header('Content-Disposition: attachment; filename=base_de_datos.csv');

                $output = fopen('php://output', 'w');

                while ($tablaRow = $tablasResult->fetch_array()) {
                    $nombreTabla = $tablaRow[0];

                    // Cabecera de la sección de la tabla
                    fputcsv($output, array("Tabla: " . $nombreTabla));

                    $datosResult = $conn->query("SELECT * FROM " . $nombreTabla);
                    
                    if ($datosResult) {
                        // Obtener nombres de columnas
                        $columnas = array();
                        $fields = $datosResult->fetch_fields();
                        foreach ($fields as $field) {
                            $columnas[] = $field->name;
                        }
                        fputcsv($output, $columnas);

                        // Escribir datos
                        while ($fila = $datosResult->fetch_assoc()) {
                            fputcsv($output, $fila);
                        }
                        
                        // Separador entre tablas
                        fputcsv($output, array("")); 
                    }
                }

                fclose($output);
                exit();
            } else {
                return "No hay tablas en la base de datos.";
            }
        }
    }
?>