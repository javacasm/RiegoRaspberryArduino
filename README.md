v# Sistema de Riego con Raspberry y Arduino

Sistema de control de riego

*  Control de relés de electroválvulas y relé bomba de riego
*  Medida de condiciones atmosféricas: Temperatura, humedad y presión usando un sensor BME280
*  Se muestra el estado en un lcd 20x4
*  Se envía el estado (relés y sensores) bajo petición por el puerto serie
*  Se define el array de los pines a los que están conectados los N relés
*  Se controla si los relés son de conexión directa o invertida (estado Low los activa)

*  Una Rapsberry Pi 3 controla el sistema
*  Control vía Telegram 



[Código Arduino V1.6.1 (C++)](./RiegoRaspberryArduino/RiegoRaspberryArduino.ino)

[Código python para Raspberry Pi V0.9](./Riego-RA-Raspberry)

TODO:

Módulo Arduino

* Establecer la hora de Arduino desde serie     -       V1.8
* Mostrar hora en el LCD                       -       V1.8
* Programación de horarios de activación       -       V2.0
* Medida de humedad del suelo                   -      V3.5 


Módulo Raspberry

Programa de control en python:
    * Encendido según horario - V1.0
    * Captura de imágenes - V1.5
    * MQTT - V2.5
    * Visualización de estadísticas - V3.0
    * Control de Humedad del suelo - V3.5

Licencia CC by SA by @javacasm

Junio de 2020