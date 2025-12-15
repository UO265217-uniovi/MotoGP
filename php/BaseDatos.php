<?php
    class BaseDatos {
        private $servername = "localhost";
        private $username = "DBUSER2025";
        private $password = "DBPSWD2025";
        private $dbname = "uo265217_db";
        private $conn;

        public function __construct() {
            $this->conn = new mysqli($this->servername, $this->username, $this->password);

            if ($this->conn->connect_error) {
                die("Error de conexión: " . $this->conn->connect_error);
            }
        }

        public function seleccionarBD() {
            return $this->conn->select_db($this->dbname);
        }

        public function getConexion() {
            return $this->conn;
        }

        public function cerrar() {
            $this->conn->close();
        }
    }
?>