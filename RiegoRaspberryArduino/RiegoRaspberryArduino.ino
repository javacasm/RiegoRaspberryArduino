/*
 *   Sistema de control de riego 
 * 
 *   *  Control de rel'es de electrov'alvulas y rel'e bomba de riego
 *   *  Medida de condiciones atmosf'ericas: Temperatura, humedad y presi'on
 *   *  Se muestra el estado en un lcd 
 *   *  Se env'ia el estado bajo petici'on por el puerto serie
 * 
 *   Pensado para que lo controle una Rapsberry Pi
 * 
 *   Licencia CC by SA by @javacasm
 *   
 *   Junio de 2020
 * 
 */


// defines

#define VERSION "V:0.3"
#define SEPARADOR_SERIE ";"

#define PERIODO_SENSORES 5000

#define END_OF_COMMAND '\n'
#define CMD_HELP       'h'
#define CMD_DATA2SERIE '*'
#define CMD_PIN2STATE 'S'
#define CMD_PIN_HIGH  'H'
#define CMD_PIN_LOW   'L'

#define mostrarMensaje(x) Serial.println(x); lcd.print(x);

// Librerias

#include <Wire.h>
// Sensor atmosferico BME280 conectado por I2C
#include <BME280I2C.h>
// LCD conectado por I2C
#include <LiquidCrystal_I2C.h>

// Constantes

BME280I2C bme;

LiquidCrystal_I2C lcd(0x27, 20, 4);

#define NReles  5
int reles[] = {2, 3, 4, 5,6};

float presion, temperatura, humedad;

long tiempoUltimoDato;

void setup() {

  // Configuracion lcd
  lcd.init();
  lcd.backlight();

  // Configuracion Serie
  Serial.begin(115200);

  
  mostrarMensaje(String(VERSION) + "by @javacasm CC by SA");

  // Configuracion Sensor BME280
  Wire.begin();
  if (!bme.begin()) {
    mostrarMensaje(F("Sensor BME no detectado"));
  }

  for( int i = 0; i < NReles; i++){
    pinMode(reles[i], OUTPUT);
    digitalWrite(reles[i], HIGH);
  }

  tiempoUltimoDato = millis();
}


void loop() {
  long tiempoActual = millis();

  leerPuertoSerie();
  
  if (tiempoActual - tiempoUltimoDato > PERIODO_SENSORES ) {
    leerSensores();
    mostrarDatosLCD();
  }
}


void leerPuertoSerie(){
  while (Serial.available() > 0) {
    char data;
    String command = "";
    while ( (data = Serial.read() ) != END_OF_COMMAND){
      command += data;
    }
    Serial.print("<<");
    Serial.println(command);
    execCommand(command);
  }

  
}

void changePin2State(String command){
  int indexPin = command[1] - '1';
  bool newState = command[2] == CMD_PIN_HIGH ? HIGH  : LOW;
  digitalWrite(reles[indexPin],newState);
  Serial.print(">> ");
  Serial.print(reles[indexPin]);
  Serial.println(command[2]);
}

void showHelp(){
  Serial.println("Comandos:");
  Serial.print(CMD_HELP);
  Serial.println(" show help");
  Serial.print(CMD_DATA2SERIE);
  Serial.println(" send data to serial");
  Serial.print(CMD_PIN2STATE);
  Serial.println("Xs X:pinID s: H for HIGH, L for LOW");
  Serial.println("\\n to send command");

}

void execCommand(String command) {
  switch(command[0]){
    case CMD_DATA2SERIE:
      mostrarDatosSerie();
      break;
    case CMD_PIN2STATE:
      changePin2State(command);
      break;
    case CMD_HELP:
      showHelp();
      break;
    default:
      mostrarMensaje(command);
      break;
    
  }

}

void leerSensores(){
   BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
   BME280::PresUnit presUnit(BME280::PresUnit_Pa);
   bme.read(presion, temperatura, humedad, tempUnit, presUnit);   
}

void mostrarDatosSerie(){ 
  Serial.print(temperatura);
  Serial.print(F(SEPARADOR_SERIE));
  Serial.print(int(round(humedad)));
  Serial.print(F(SEPARADOR_SERIE));
  Serial.print(long(presion));
  Serial.print(F(SEPARADOR_SERIE));
  for(int i = 0; i < NReles; i++){
    if (!digitalRead(reles[i]))
        Serial.print("On;");
    else
        Serial.print("Off;");
    Serial.print(F(SEPARADOR_SERIE));
  }  
  Serial.println();
}

void mostrarDatosLCD(){
//  lcd.clear();
  
  /* FORMATEO de datos y ENVIO al puerto SERIE */
  lcd.setCursor(0,0);
  lcd.print(F("T:"));
  lcd.print(temperatura);
  lcd.print(F("C H:"));
  lcd.print(int(round(humedad)));
  lcd.print(F("%"));
  lcd.setCursor(0,1);
  lcd.print(F("P:"));
  lcd.print(long(presion));
  lcd.print(F("atm"));
  lcd.setCursor(0,3);
  for( int i = 0; i < NReles; i++){
    if (!digitalRead(reles[i]))
        lcd.print("On  ");
    else
        lcd.print("Off ");
  }

}
