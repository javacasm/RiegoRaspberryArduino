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

#define VERSION "V:1.3"
#define SEPARADOR_SERIE ";"

#define PERIODO_LECTURA_SENSORES 5000

#define CMD_RETURN_ERROR -1
#define CMD_RETURN_OK     0
#define CMD_RETURN_UNKOWN 1

#define END_OF_COMMAND '\n'
#define CMD_HELP       'h'
#define CMD_DATA2SERIE '*'
#define CMD_PIN2STATE 'S'
#define CMD_PIN_HIGH  'H'
#define CMD_PIN_LOW   'L'

#define CMD_PINSTATE2TEXT(x) x != CMD_PIN_HIGH ? "High" : "Low"
#define CMD_PINSTATE2BOOL(x) x != CMD_PIN_HIGH ?  HIGH  :  LOW

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

  
  mostrarMensaje(String(VERSION));
  lcd.setCursor(0,2);
  mostrarMensaje(" @javacasm CC by SA");

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
  
  if (tiempoActual - tiempoUltimoDato > PERIODO_LECTURA_SENSORES ) {
    leerSensores();
    mostrarDatosLCD();
    tiempoUltimoDato = tiempoActual;
  }
}


int leerPuertoSerie(){
  int returnValue = CMD_RETURN_ERROR;
  
  if (Serial.available() > 0) {
    char data;
    String command = "";
    while ( (data = Serial.read() ) != END_OF_COMMAND){
      if(data != -1 && data != '\r' && data != '\n') // -1 no hay datos, No queremos incluir los finales de linea
        command += data;
    }
    returnValue = execCommand(command);
  }

  return returnValue;
}



int  changePin2State(String command){
  int returnValue = CMD_RETURN_ERROR;
  int indexPin = command[1] - '1';
  if(indexPin < NReles){
    bool newState = CMD_PINSTATE2BOOL(command[2]);
    digitalWrite(reles[indexPin],newState);
    
    Serial.print(">> Set ");
    Serial.print(reles[indexPin]);
    Serial.print(" ");
    Serial.println(CMD_PINSTATE2TEXT(command[2]));
    returnValue = CMD_RETURN_OK;
  }
  else {
    Serial.print("ERROR: no data for rele ");
    Serial.println(indexPin);
  }
  return returnValue;
}

int  showHelp(){
  Serial.println("Comandos:");
  Serial.print(CMD_HELP);
  Serial.println(" show help");
  Serial.print(CMD_DATA2SERIE);
  Serial.println(" send data to serial");
  Serial.print(CMD_PIN2STATE);
  Serial.println("Xs X:pinID s: H for HIGH, L for LOW");
  Serial.println("\\n to send command");
  return CMD_RETURN_OK;
}

void dumpStringChars(String command) {
  for(int  i=0; i< command.length(); i++){
    Serial.print(int(command[i]));
    Serial.print("-");
    Serial.println(command[i]);
  }
}



int execCommand(String command) {
  int returnValue = CMD_RETURN_ERROR;
  switch(command[0]){
    case CMD_DATA2SERIE:
      returnValue = mostrarDatosSerie();
      break;
    case CMD_PIN2STATE:
      returnValue = changePin2State(command);
      if(returnValue == CMD_RETURN_OK) {
          mostrarDatosSerie();
          mostrarDatosLCD();
      }
      break;
    case CMD_HELP:
      returnValue = showHelp();
      break;
    default:
      mostrarMensaje(command);
      returnValue = CMD_RETURN_UNKOWN;
      break;
    
  }
  return returnValue;
}

int  leerSensores(){
   BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
   BME280::PresUnit presUnit(BME280::PresUnit_Pa);
   bme.read(presion, temperatura, humedad, tempUnit, presUnit);   
   return CMD_RETURN_OK;
}

int mostrarDatosSerie(){ 
  Serial.print(temperatura);
  Serial.print(F(SEPARADOR_SERIE));
  Serial.print(int(round(humedad)));
  Serial.print(F(SEPARADOR_SERIE));
  Serial.print(long(presion));
  Serial.print(F(SEPARADOR_SERIE));
  for(int i = 0; i < NReles; i++){
    if (!digitalRead(reles[i]))
        Serial.print("On");
    else
        Serial.print("Off");
    Serial.print(F(SEPARADOR_SERIE));
  }  
  Serial.println();
  return CMD_RETURN_OK;
}

int mostrarDatosLCD(){
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
  return CMD_RETURN_OK;
}
