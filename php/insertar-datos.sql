USE UO265217_DB;

INSERT INTO dispositivos (nombre_dispositivo) VALUES 
('Ordenador'),
('Tableta'),
('Teléfono Móvil');

-- 2. Insertar las 10 preguntas del test sobre MotoGP
INSERT INTO preguntas (enunciado, respuesta_a, respuesta_b, respuesta_c, respuesta_d, correcta) VALUES
('¿Cuál es el dorsal con el que corre Somkiat Chantra en MotoGP 2025?', '93', '35', '46', '12', 'b'),
('¿En qué ciudad nació el piloto Somkiat Chantra?', 'Bangkok', 'Buriram', 'Chonburi', 'Phuket', 'c'),
('¿Qué archivo específico debes cargar en la sección "Circuito" para ver la altimetría?', 'mapa.svg', 'altimetria.xml', 'altimetria.svg', 'circuito.png', 'c'),
('¿Qué marca de motos NO aparece en las cartas del Juego de Memoria?', 'Kawasaki', 'Ducati', 'KTM', 'Aprilia', 'a'),
('Según la biografía, ¿en qué categoría compitió Somkiat Chantra antes de subir a Moto2?', 'Red Bull Rookies Cup', 'Asia Talent Team (Moto3)', 'MotoE', 'Superbikes', 'b'),
('¿Cuál es la altura del piloto Somkiat Chantra según su ficha técnica?', '1,68m', '1,75m', '1,71m', '1,80m', 'c'),
('¿Cuántas noticias aparecen en la pantalla de inicio?', '1', '2', '3', '4', 'c'),
('¿Qué archivo KML se solicita cargar para visualizar el mapa del circuito?', 'mapa.kml', 'track.kml', 'circuito.kml', 'motogp.kml', 'c'),
('¿Con qué fabricante competirá Chantra en el Mundial de Superbikes en 2026?', 'Yamaha', 'Ducati', 'Kawasaki', 'Honda HRC', 'd'),
('¿Qué término se define en la sección de Piloto como "Vuelta de calentamiento"?', 'Pole Position', 'Warm Up Lap', 'Sighting Lap', 'Cooldown Lap', 'b');