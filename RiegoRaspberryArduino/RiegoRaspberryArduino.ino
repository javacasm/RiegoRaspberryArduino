/*
     Sistema de control de riego

     *  Control de rel'es de electrov'alvulas y rel'e bomba de riego
     *  Medida de condiciones atmosf'ericas: Temperatura, humedad y presi'on usando un sensor BME280
     *  Se muestra el estado en un lcd 20x4
     *  Se env'ia el estado (rel'es y sensores) bajo petici'on por el puerto serie
     *  Se define el array de los pines a los que est'an conectados los N rel'es
     *  Se controla si los rel'es son de conexi'on directa o invertida (estado Low los activa)


     Pensado para que lo controle una Rapsberry Pi


     TODO:

     * Establecer hora desde serie V1.8
     * Mostrar hora en el LCD      V1.8
     * Programaci'on  de activaci'on a horarios   V2.0

     Licencia CC by SA by @javacasm

     Junio de 2020

*/


// defines

#define VERSION "V:1.6.1"
#define SEPARADOR_SERIE ";"

#define PERIODO_LECTURA_SENSORES 5000

#define CMD_RETURN_ERROR -1
#define CMD_RETURN_OK     0
#define CMD_RETURN_UNKOWN 1

#define END_OF_COMMAND '\n'
#define CMD_HELP       'h'
#define CMD_DATA2SERIE '#'
#define CMD_PIN2STATE  'S'
#define CMD_WILCARD    '*'
#define CMD_PIN_HIGH   'H'
#define CMD_PIN_LOW    'L'
#define CMD_SET_SENSOR_PERIOD 'T'

#define CMD_PINSTATE2TEXT(x) x == CMD_PIN_HIGH ? "High" : "Low"
#define CMD_PINSTATE2BOOL(x) x == CMD_PIN_HIGH ?  HIGH  :  LOW

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
int reles[] = {2, 3, 4, 5, 6};
bool relesInverted[] = {true, true, true, true, false};

float presion, temperatura, humedad;

long periodoLecturaSensores = PERIODO_LECTURA_SENSORES;
long tiempoUltimoDato;

void setup() {

  // Configuracion lcd
  lcd.init();
  lcd.backlight();

  // Configuracion Serie
  Serial.begin(115200);


  mostrarMensaje(String(VERSION));
  lcd.setCursor(0, 2);
  mostrarMensaje(" @javacasm CC by SA");

  // Configuracion Sensor BME280
  Wire.begin();
  if (!bme.begin()) {
    mostrarMensaje(F("Sensor BME no detectado"));
  }

  for ( int i = 0; i < NReles; i++) {
    pinMode(reles[i], OUTPUT);
    setReleState(i,LOW);
  }

  tiempoUltimoDato = millis();
}


void loop() {
  long tiempoActual = millis();

  leerPuertoSerie();

  if (tiempoActual - tiempoUltimoDato > periodoLecturaSensores ) {
    leerSensores();
    mostrarDatosLCD();
    tiempoUltimoDato = tiempoActual;
  }
}


int leerPuertoSerie() {
  int returnValue = CMD_RETURN_ERROR;

  if (Serial.available() > 0) {
    char data;
    String command = "";
    while ( (data = Serial.read() ) != END_OF_COMMAND) {
      if (data != -1 && data != '\r' && data != '\n') // -1 no hay datos, No queremos incluir los finales de linea
        command += data;
    }
    returnValue = execCommand(command);
  }

  return returnValue;
}



int setReleState(int indexPin,bool newState){
   if (relesInverted[indexPin]) newState = !newState;
     digitalWrite(reles[indexPin], newState);   
}

int  changePin2State(String command) {

  int returnValue = CMD_RETURN_ERROR;
  bool newState = CMD_PINSTATE2BOOL(command[2]);
  if (command[1] == CMD_WILCARD){
    for (int i = 0; i < NReles ; i++){
      setReleState(i,newState);
    }
    Serial.print(">> Set all reles ");
    Serial.println(CMD_PINSTATE2TEXT(command[2]));
    returnValue = CMD_RETURN_OK;
  } else {
  
    int indexPin = command[1] - '1';
    if ( (indexPin < NReles) && (indexPin >= 0) ) {
      setReleState(indexPin,newState);
      Serial.print(">> Set rele ");
      Serial.print(command[1]);
      Serial.print(" ");
      Serial.println(CMD_PINSTATE2TEXT(command[2]));
      returnValue = CMD_RETURN_OK;
    }
    else {
      Serial.print("ERROR: no hay datos conexion del rele ");
      Serial.println(indexPin);
    }
  }
  return returnValue;
}

int  showHelp() {
  Serial.println("=============================");
  Serial.println("Comandos:");
  Serial.print("  ");
  Serial.print(CMD_DATA2SERIE);
  Serial.println(" envia los datos actuales via serie");
  Serial.print("  ");
  Serial.print(CMD_PIN2STATE);
  Serial.print("Xs X:pinID (1-"); Serial.print(NReles); Serial.print(") "); Serial.print(CMD_WILCARD); Serial.println(" para todos s: H para HIGH, L para LOW");
  Serial.print("  ");
  Serial.print(CMD_SET_SENSOR_PERIOD);
  Serial.println("N N:0-9 segundos entre medidas de datos. 0 Medida continua");
  Serial.print("  ");
  Serial.print(CMD_HELP);
  Serial.println(" muestra ayuda");
  Serial.println("  \\n para enviar y ejecutar el comando");
  Serial.println("=============================");
  return CMD_RETURN_OK;
}

void dumpStringChars(String command) {
  for (int  i = 0; i < command.length(); i++) {
    Serial.print(int(command[i]));
    Serial.print("-");
    Serial.println(command[i]);
  }
}



int execCommand(String command) {
  int returnValue = CMD_RETURN_ERROR;
  Serial.print("<< ");
  Serial.println(command);
  switch (command[0]) {
    case CMD_DATA2SERIE:
      returnValue = mostrarDatosSerie();
      break;
    case CMD_PIN2STATE:
      returnValue = changePin2State(command);
      if (returnValue == CMD_RETURN_OK) {
        mostrarDatosSerie();
        mostrarDatosLCD();
      }
      break;
    case CMD_HELP:
      returnValue = showHelp();
      break;
    case CMD_SET_SENSOR_PERIOD:
      returnValue = changePeriodSensor(command);
      break;
    default:
      mostrarMensaje(command);
      returnValue = CMD_RETURN_UNKOWN;
      break;

  }
  return returnValue;
}

int changePeriodSensor(String command) {
  int returnValue = CMD_RETURN_ERROR;
  periodoLecturaSensores = (command[1] - '0') * 1000;
  if (periodoLecturaSensores < 0) periodoLecturaSensores = 0;
  Serial.print(">> Tsensors = ");
  Serial.print(periodoLecturaSensores);
  Serial.print("ms");
  returnValue = CMD_RETURN_OK;
  return returnValue;

}

int  leerSensores() {
  BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
  BME280::PresUnit presUnit(BME280::PresUnit_Pa);
  bme.read(presion, temperatura, humedad, tempUnit, presUnit);
  return CMD_RETURN_OK;
}

int mostrarDatosSerie() {
  Serial.print(temperatura);
  Serial.print(F(SEPARADOR_SERIE));
  Serial.print(int(round(humedad)));
  Serial.print(F(SEPARADOR_SERIE));
  Serial.print(long(presion));
  Serial.print(F(SEPARADOR_SERIE));
  for (int i = 0; i < NReles; i++) {
     Serial.print(getReleStrState(i));
     Serial.print(F(SEPARADOR_SERIE));
  }
  Serial.println();
  return CMD_RETURN_OK;
}

int mostrarDatosLCD() {
  //  lcd.clear();

  /* FORMATEO de datos y ENVIO al puerto SERIE */
  lcd.setCursor(0, 0);
  lcd.print(F("T:"));
  lcd.print(temperatura);
  lcd.print(F("C H:"));
  lcd.print(int(round(humedad)));
  lcd.print(F("%"));
  lcd.setCursor(0, 1);
  lcd.print(F("P:"));
  lcd.print(long(presion));
  lcd.print(F(" atm"));
  
  for ( int i = 0; i < NReles; i++) {
    lcd.setCursor(i * 4, 3);
    lcd.print(getReleStrState(i));
    lcd.print(" ");
  }
  return CMD_RETURN_OK;
}

String getReleStrState(int idRele){
  String strState = "";
  int releState = getReleState(idRele);
  if (releState)
      strState = "On";
  else
      strState = "Off";
  return strState;
}

int getReleState(int idRele){
   int pinState = digitalRead(reles[idRele]);
   if (relesInverted[idRele]) pinState = !pinState;
   return pinState;
}
