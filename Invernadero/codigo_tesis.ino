#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// Wi-Fi
const char* ssid = "Cereza";
const char* password = "robotica25";

// API del servidor
const char* serverUrl = "https://floracore.onrender.com/api/parameters/";

// Pines sensores
#define DHTPIN 4
#define DHTTYPE DHT11
#define SOIL_PIN 34
#define LIGHT_PIN 35

// Pines reles
#define PIN_RIEGO 26
#define PIN_VENTILADORES 27
#define PIN_FOCO 25   // Relé para el foco

// Instancia sensor DHT
DHT dht(DHTPIN, DHTTYPE);

// Estructura para datos de sensores
struct SensorData {
  float temperatura;
  float humedad;
  float humedad_suelo;
  float luz;
};

// Variables para optimización (últimos valores enviados)
SensorData lastSentData = {0, 0, 0, 0};

// Umbrales para cambio significativo
const float TEMP_THRESHOLD = 0.5;
const float HUM_THRESHOLD = 2.0;
const float SOIL_HUM_THRESHOLD = 2.0;
const float LIGHT_THRESHOLD = 5.0;

// Variables para reconexión WiFi
unsigned long lastWiFiCheck = 0;
const unsigned long WIFI_CHECK_INTERVAL = 10000;

// Variables para el parpadeo del foco
unsigned long lastFocoToggle = 0;
const unsigned long FOCO_INTERVAL = 2000; // 2 segundos
bool focoState = false;

// Variables para el control automático del riego
unsigned long lastRiegoToggle = 0;
const unsigned long RIEGO_INTERVAL = 5000; // cada 5 segundos
const unsigned long RIEGO_ON_TIME = 1000;  // encendido durante 1 segundo
bool riegoState = false;

// ---------------- FUNCIONES ----------------

void connectWiFi() {
  if (WiFi.status() != WL_CONNECTED) {
    if (millis() - lastWiFiCheck > WIFI_CHECK_INTERVAL) {
      Serial.println("Intentando reconectar WiFi...");
      WiFi.begin(ssid, password);
      lastWiFiCheck = millis();
    }
  }
}

SensorData leerSensores() {
  SensorData data;
  data.temperatura = dht.readTemperature();
  data.humedad = dht.readHumidity();
  int humedad_suelo_raw = analogRead(SOIL_PIN);
  int luz_raw = analogRead(LIGHT_PIN);

  if (isnan(data.temperatura) || isnan(data.humedad)) {
    Serial.println("Error: No se pudo leer el sensor DHT11");
    data.temperatura = -999;
    data.humedad = -999;
    return data;
  }

  data.humedad_suelo = map(humedad_suelo_raw, 4095, 1500, 0, 100);
  data.humedad_suelo = constrain(data.humedad_suelo, 0, 100);
  data.luz = map(luz_raw, 0, 4095, 100, 0);

  return data;
}

bool datosCambiaron(SensorData current, SensorData last) {
  return (abs(current.temperatura - last.temperatura) >= TEMP_THRESHOLD) ||
         (abs(current.humedad - last.humedad) >= HUM_THRESHOLD) ||
         (abs(current.humedad_suelo - last.humedad_suelo) >= SOIL_HUM_THRESHOLD) ||
         (abs(current.luz - last.luz) >= LIGHT_THRESHOLD);
}

bool enviarDatos(SensorData data) {
  WiFiClientSecure client;
  client.setInsecure();
  HTTPClient http;
  
  // Configurar timeout
  http.setTimeout(10000);
  http.begin(client, serverUrl);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Accept", "application/json");
  http.addHeader("User-Agent", "ESP32-Invernadero/1.0");

  // Validar datos antes de enviar
  if (isnan(data.temperatura) || isnan(data.humedad)) {
    Serial.println("Error: Datos inválidos, no se puede enviar");
    http.end();
    return false;
  }

  // Crear JSON usando ArduinoJson para mayor confiabilidad
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["temperatura"] = round(data.temperatura * 10) / 10.0;
  jsonDoc["humedad"] = round(data.humedad * 10) / 10.0;
  jsonDoc["humedad_suelo"] = round(data.humedad_suelo * 10) / 10.0;
  jsonDoc["luz"] = round(data.luz * 10) / 10.0;
  
  String jsonData;
  serializeJson(jsonDoc, jsonData);

  Serial.println("Enviando datos: " + jsonData);

  int httpResponseCode = http.POST(jsonData);
  bool success = false;

  Serial.println("Código de respuesta: " + String(httpResponseCode));
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Respuesta del servidor (primeros 200 chars): " + response.substring(0, min(200, (int)response.length())));

    if (httpResponseCode == 201 || httpResponseCode == 200) {
      // Verificar si la respuesta parece ser JSON
      if (response.startsWith("{") && response.endsWith("}")) {
        StaticJsonDocument<1024> doc;
        DeserializationError error = deserializeJson(doc, response);

        if (error) {
          Serial.print("Error al deserializar JSON: ");
          Serial.println(error.f_str());
          Serial.println("Respuesta completa: " + response);
          // Consideramos exitoso si el HTTP es correcto
          success = true;
        } else {
          Serial.println("JSON parseado correctamente");
          // Verificar estructura de respuesta
          if (doc.containsKey("acciones")) {
            int riego = doc["acciones"]["riego"];
            int ventiladores = doc["acciones"]["ventiladores"];

            Serial.println("Riego: " + String(riego ? "ON" : "OFF"));
            Serial.println("Ventiladores: " + String(ventiladores ? "ON" : "OFF"));

            aplicarAcciones(riego, ventiladores);
          } else {
            Serial.println("Advertencia: Respuesta sin campo 'acciones'");
          }
          success = true;
        }
      } else {
        Serial.println("Error: Respuesta no es JSON válido");
        Serial.println("Respuesta completa: " + response);
        // Si recibimos HTML, probablemente hay un error del servidor
        if (response.indexOf("<html>") >= 0 || response.indexOf("<HTML>") >= 0) {
          Serial.println("El servidor devolvió HTML en lugar de JSON - posible error 500");
        }
      }
    } else if (httpResponseCode >= 400) {
      Serial.println("Error HTTP " + String(httpResponseCode) + ": " + response);
    }
  } else {
    Serial.print("Error de conexión: ");
    Serial.println(http.errorToString(httpResponseCode));
  }

  http.end();
  return success;
}

void aplicarAcciones(int riego, int ventiladores) {
  digitalWrite(PIN_RIEGO, riego ? HIGH : LOW);
  digitalWrite(PIN_VENTILADORES, ventiladores ? HIGH : LOW);
}

// Función para manejar el parpadeo del foco
void manejarFoco() {
  unsigned long currentMillis = millis();
  if (currentMillis - lastFocoToggle >= FOCO_INTERVAL) {
    focoState = !focoState;
    digitalWrite(PIN_FOCO, focoState ? HIGH : LOW);
    Serial.println(focoState ? " Foco ENCENDIDO" : " Foco APAGADO");
    lastFocoToggle = currentMillis;
  }
}

// Función para manejar la bomba de agua automáticamente
void manejarRiegoAutomatico() {
  unsigned long currentMillis = millis();

  if (!riegoState && (currentMillis - lastRiegoToggle >= RIEGO_INTERVAL)) {
    riegoState = true;
    digitalWrite(PIN_RIEGO, HIGH);
    Serial.println(" Bomba de agua ENCENDIDA");
    lastRiegoToggle = currentMillis;
  }

  // Apagar después de 1 segundo
  if (riegoState && (currentMillis - lastRiegoToggle >= RIEGO_ON_TIME)) {
    riegoState = false;
    digitalWrite(PIN_RIEGO, LOW);
    Serial.println(" Bomba de agua APAGADA");
  }
}

// ---------------- SETUP ----------------
void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(PIN_RIEGO, OUTPUT);
  pinMode(PIN_VENTILADORES, OUTPUT);
  pinMode(PIN_FOCO, OUTPUT);
  digitalWrite(PIN_RIEGO, LOW);
  digitalWrite(PIN_VENTILADORES, LOW);
  digitalWrite(PIN_FOCO, LOW);

  WiFi.begin(ssid, password);
  Serial.print("Conectando a Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado a Wi-Fi");
}

// ---------------- LOOP ----------------
void loop() {
  connectWiFi();

  manejarFoco();              // Parpadeo del foco
  manejarRiegoAutomatico();   // Control automático de la bomba

  if (WiFi.status() == WL_CONNECTED) {
    SensorData currentData = leerSensores();
    if (currentData.temperatura == -999) {
      delay(5000);
      return;
    }

    Serial.println("Temperatura: " + String(currentData.temperatura, 1) + " °C");
    Serial.println("Humedad: " + String(currentData.humedad, 1) + " %");
    Serial.println("Humedad suelo: " + String(currentData.humedad_suelo, 1) + " %");
    Serial.println("Luminosidad: " + String(currentData.luz, 1) + " %");

    if (datosCambiaron(currentData, lastSentData)) {
      Serial.println("Datos cambiaron significativamente, enviando...");
      bool sent = false;
      for (int attempt = 1; attempt <= 3 && !sent; attempt++) {
        Serial.println("Intento " + String(attempt) + " de envío");
        sent = enviarDatos(currentData);
        if (!sent && attempt < 3) delay(2000);
      }

      if (sent) {
        lastSentData = currentData;
        Serial.println("Datos enviados exitosamente");
      } else {
        Serial.println("Falló el envío después de 3 intentos");
      }
    } else {
      Serial.println("Datos no cambiaron significativamente, omitiendo envío");
    }
  } else {
    Serial.println("WiFi no conectado, intentando reconectar...");
  }

  delay(100); // pequeño delay para evitar saturar el loop
}
