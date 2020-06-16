// defines

#define VERSION "0.1"
#define SEPARADOR ";"
#define PERIODO_SENSORES 5000
#define CMD_DATA2SERIE "*"
#define CMD_PIN2STATE "S"

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

#define NReles  4
int reles[] = {2, 3, 4, 5};

float presion, temperatura, humedad;

long tiempoUltimoDato;

void setup() {

  // Configuracion lcd
  lcd.init();
  lcd.backlight();

  // Configuracion Serie
  Serial.begin(115200);

  
  mostrarMensaje(F(VERSION));

  // Configuracion Sensor BME280
  Wire.begin();
  if (!bme.begin()) {
    mostrarMensaje(F("Sensor BME no detectado"));
  }

  for( int i = 0; i < NReles; i++){
    pinMode(reles[i], OUTPUT);
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
    char lectura = Serial.read();

  }

  
}



void leerSensores(){
   BME280::TempUnit tempUnit(BME280::TempUnit_Celsius);
   BME280::PresUnit presUnit(BME280::PresUnit_Pa);
   bme.read(presion, temperatura, humedad, tempUnit, presUnit);   
}

void mostrarDatosSerie(){ 
  Serial.print(temperatura);
  Serial.print(F(SEPARADOR));
  Serial.print(int(round(humedad)));
  Serial.print(F(SEPARADOR));
  Serial.print(long(presion));
  for(int i = 0; i < NReles; i++){
    if (digitalRead(reles[i]))
        Serial.print("On;");
    else
        Serial.print("Off;");
  }  
}

void mostrarDatosLCD(){
  lcd.clear();
  
  /* FORMATEO de datos y ENVIO al puerto SERIE */
  lcd.setCursor(0,0);
  lcd.print(F("T:"));
  lcd.print(temperatura);
  lcd.print(F(" H:"));
  lcd.print(int(round(humedad)));
  lcd.print(F(" P:"));
  lcd.print(long(presion));
  //lcd.print(F("atm"));
  lcd.setCursor(0,1);
  for( int i = 0; i < NReles; i++){
    if (digitalRead(reles[i]))
        lcd.print("On  ");
    else
        lcd.print("Off ");
  }

}

void execCommand(String command) {
  if (command == "*" ) mostrarDatosSerie();
  
}
