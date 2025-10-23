#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// Wi-Fi
const char* ssid = "Cereza";
const char* password = "robotica25";

// API del servidor (HTTP para testing local)
const char* serverUrl = "http://localhost:8000/api/parameters/";

// Pines sensores
#define DHTPIN 4
#define DHTTYPE DHT11
#define SOIL_PIN 34
#define LIGHT_PIN 35

// Pines reles
#define PIN_RIEGO 26
#define PIN_VENTILADORES 27
#define PIN_FOCO 25

// Instancia sensor DHT
DHT dht(DHTPIN, DHTTYPE);

// Estructura para datos de sensores
struct SensorData {
  float temperatura;
  float humedad;
  float humedad_suelo;
  float luz;
};

// Variables para optimización
SensorData lastSentData = {0, 0, 0, 0};

// Umbrales para cambio significativo
const float TEMP_THRESHOLD = 0.5;
const float HUM_THRESHOLD = 2.0;
const float SOIL_HUM_THRESHOLD = 2.0;
const float LIGHT_THRESHOLD = 5.0;

// Variables para reconexión WiFi
unsigned long lastWiFiCheck = 0;
const unsigned long WIFI_CHECK_INTERVAL = 10000;

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
  HTTPClient http;
  
  http.setTimeout(10000);
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Accept", "application/json");
  http.addHeader("User-Agent", "ESP32-Invernadero/1.0");

  if (isnan(data.temperatura) || isnan(data.humedad)) {
    Serial.println("Error: Datos inválidos, no se puede enviar");
    http.end();
    return false;
  }

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
    Serial.println("Respuesta completa: " + response);

    if (httpResponseCode == 201 || httpResponseCode == 200) {
      if (response.startsWith("{") && response.endsWith("}")) {
        StaticJsonDocument<1024> doc;
        DeserializationError error = deserializeJson(doc, response);

        if (error) {
          Serial.print("Error al deserializar JSON: ");
          Serial.println(error.f_str());
          success = true;
        } else {
          Serial.println("JSON parseado correctamente");
          if (doc.containsKey("acciones")) {
            int riego = doc["acciones"]["riego"];
            int ventiladores = doc["acciones"]["ventiladores"];
            int foco = doc["acciones"]["foco"];

            Serial.println("Riego: " + String(riego ? "ON" : "OFF"));
            Serial.println("Ventiladores: " + String(ventiladores ? "ON" : "OFF"));
            Serial.println("Foco: " + String(foco ? "ON" : "OFF"));

            aplicarAcciones(riego, ventiladores, foco);
          }
          success = true;
        }
      }
    } else {
      Serial.println("Error HTTP " + String(httpResponseCode) + ": " + response);
    }
  } else {
    Serial.print("Error de conexión: ");
    Serial.println(http.errorToString(httpResponseCode));
  }

  http.end();
  return success;
}

void aplicarAcciones(int riego, int ventiladores, int foco) {
  digitalWrite(PIN_RIEGO, riego ? HIGH : LOW);
  digitalWrite(PIN_VENTILADORES, ventiladores ? HIGH : LOW);
  digitalWrite(PIN_FOCO, foco ? HIGH : LOW);
}

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

void loop() {
  connectWiFi();

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

    static unsigned long lastSend = 0;
    if (millis() - lastSend > 10000 || datosCambiaron(currentData, lastSentData)) {
      Serial.println("Enviando datos al servidor...");
      bool sent = enviarDatos(currentData);
      if (sent) {
        lastSentData = currentData;
        lastSend = millis();
      }
    }
  } else {
    Serial.println("WiFi no conectado, intentando reconectar...");
  }

  delay(1000);
}