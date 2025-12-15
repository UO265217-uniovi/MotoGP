<?php
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

    public function getSeconds() {
        $tiempoTotal = $this->tiempo;
        if ($this->inicio != 0) {
            $tiempoTotal += microtime(true) - $this->inicio;
        }
        return $tiempoTotal;
    }
}
?>