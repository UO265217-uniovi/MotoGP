USE UO265217_DB;

INSERT INTO dispositivos (nombre_dispositivo) VALUES 
('Ordenador'),
('Tableta'),
('Teléfono Móvil');

-- 2. Insertar las 10 preguntas del test sobre MotoGP
INSERT INTO preguntas (enunciado, respuesta_a, respuesta_b, respuesta_c, respuesta_d, correcta) VALUES
('¿Cuál es el dorsal con el que corre Somkiat Chantra en MotoGP 2025?', '93', '35', '46', '12', 'b'),
('¿Cuál es el gentilico días dura el calentamiento?', '1', '2', '3', '4', 'c'),
('¿Qué archivo específico debes cargar en la sección "Circuito" para ver la altimetría?', 'mapa.svg', 'altimetria.xml', 'altimetria.svg', 'circuito.png', 'c'),
('¿Qué marca de motos NO aparece en las cartas del Juego de Memoria?', 'Kawasaki', 'Ducati', 'KTM', 'Aprilia', 'a'),
('¿Qué % de humedad había el día de la carrera a las 15 de la tarde?', '33%', '39%', '58.46 %', '48%', 'a'),
('¿Cuál es la altura del piloto Somkiat Chantra según su ficha técnica?', '1,68m', '1,75m', '1,71m', '1,80m', 'c'),
('¿Cuántas noticias aparecen en la pantalla de inicio?', '1', '2', '3', '4', 'c'),
('¿Qué archivo KML se solicita cargar para visualizar el mapa del circuito?', 'mapa.kml', 'track.kml', 'circuito.kml', 'motogp.kml', 'c'),
('¿Cuántos clicks tienes que hacer desde la página de inicio para poner el cronómetro en marcha?', '1', '2', '3', '4', 'c'),
('¿Qué término se define en la sección de Piloto como "Vuelta de calentamiento"?', 'Pole Position', 'Warm Up Lap', 'Sighting Lap', 'Cooldown Lap', 'b');