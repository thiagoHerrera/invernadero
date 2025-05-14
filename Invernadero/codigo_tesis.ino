#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "DHT.h"

// Wi-Fi
const char* ssid = "Cereza";
const char* password = "robotica";

// API del servidor
const char* serverUrl = "http://192.168.0.12:8000/api/sensors/";

// Pines sensores
#define DHTPIN 15
#define DHTTYPE DHT11
#define SOIL_PIN 34
#define LIGHT_PIN 35

// Pines actuadores
#define PIN_BOMBA 26
#define PIN_VENTILADOR 27

// Instancia sensor DHT
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Configurar pines de salida
  pinMode(PIN_BOMBA, OUTPUT);
  pinMode(PIN_VENTILADOR, OUTPUT);
  digitalWrite(PIN_BOMBA, LOW);
  digitalWrite(PIN_VENTILADOR, LOW);

  // Conexión Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado a Wi-Fi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Lectura de sensores
    float temperatura = dht.readTemperature();
    float humedad = dht.readHumidity();
    int humedad_suelo_raw = analogRead(SOIL_PIN);
    int luz_raw = analogRead(LIGHT_PIN);

    if (isnan(temperatura) || isnan(humedad)) {
      Serial.println("Error al leer DHT11");
      delay(5000);
      return;
    }

    // Conversión de valores
    float humedad_suelo = map(humedad_suelo_raw, 4095, 1500, 0, 100);
    humedad_suelo = constrain(humedad_suelo, 0, 100);

    float luminosidad = map(luz_raw, 0, 4095, 100, 0);

    // Mostrar en consola
    Serial.println("Temperatura: " + String(temperatura, 1));
    Serial.println("Humedad: " + String(humedad, 1));
    Serial.println("Humedad suelo: " + String(humedad_suelo, 1));
    Serial.println("Luminosidad: " + String(luminosidad, 1));

    // Crear JSON
    String jsonData = "{\"temperatura\": " + String(temperatura, 1) +
                      ", \"humedad\": " + String(humedad, 1) +
                      ", \"humedad_suelo\": " + String(humedad_suelo, 1) +
                      ", \"luz\": " + String(luminosidad, 1) + "}";

    // Enviar HTTP POST
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Código de respuesta: " + String(httpResponseCode));
      Serial.println("Respuesta del servidor: " + response);

      // Deserializar JSON
      StaticJsonDocument<200> doc;
      DeserializationError error = deserializeJson(doc, response);

      if (error) {
        Serial.print("Error al deserializar JSON: ");
        Serial.println(error.f_str());
      } else {
        bool bomba = doc["bomba"];
        bool ventilador = doc["ventilador"];

        Serial.println("Bomba: " + String(bomba ? "ON" : "OFF"));
        Serial.println("Ventilador: " + String(ventilador ? "ON" : "OFF"));

        digitalWrite(PIN_BOMBA, bomba ? HIGH : LOW);
        digitalWrite(PIN_VENTILADOR, ventilador ? HIGH : LOW);
      }

    } else {
      Serial.print("Error en POST: ");
      Serial.println(http.errorToString(httpResponseCode));
    }

    http.end();
  } else {
    Serial.println("WiFi no conectado");
  }

  delay(10000); // Espera 10 segundos antes del próximo ciclo
}
