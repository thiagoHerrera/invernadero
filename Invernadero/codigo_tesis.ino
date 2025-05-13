#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h"

// Wi-Fi
const char* ssid = "Telecentro-eaa3";
const char* password = "M3NNCHMGHM6P";

// API URL
const char* serverUrl = "http://192.168.0.12:8000/api/sensors/";

// Pines
#define DHTPIN 15
#define DHTTYPE DHT11
#define SOIL_PIN 34     // Sensor de humedad de suelo
#define LIGHT_PIN 35    // Sensor de luminosidad (LDR)

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

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

    // Leer sensores
    float temperatura = dht.readTemperature();
    float humedad = dht.readHumidity();
    int humedad_suelo_raw = analogRead(SOIL_PIN);      // 0 a 4095
    int luz_raw = analogRead(LIGHT_PIN);               // 0 a 4095

    // Verificar que no falle el DHT11
    if (isnan(temperatura) || isnan(humedad)) {
      Serial.println("Error al leer DHT11");
      delay(5000);
      return;
    }

    // Convertir humedad de suelo a porcentaje (opcional, depende del sensor)
    float humedad_suelo = map(humedad_suelo_raw, 4095, 1500, 0, 100);
    humedad_suelo = constrain(humedad_suelo, 0, 100);

    // Convertir luz (opcional)
    float luminosidad = map(luz_raw, 0, 4095, 100, 0); // 100% = luz fuerte, 0% = oscuridad

    // Mostrar en consola
    Serial.println("Temperatura: " + String(temperatura));
    Serial.println("Humedad: " + String(humedad));
    Serial.println("Humedad suelo: " + String(humedad_suelo));
    Serial.println("Luminosidad: " + String(luminosidad));

    // JSON para POST
    String jsonData = "{\"temperatura\": " + String(temperatura, 1) +
                      ", \"humedad\": " + String(humedad, 1) +
                      ", \"humedad_suelo\": " + String(humedad_suelo, 1) +
                      ", \"luz\": " + String(luminosidad, 1) + "}";

    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(jsonData);

    if (httpResponseCode > 0) {
      Serial.print("Código de respuesta: ");
      Serial.println(httpResponseCode);
      String response = http.getString();
      Serial.println("Respuesta del servidor: " + response);
    } else {
      Serial.print("Error en POST: ");
      Serial.println(http.errorToString(httpResponseCode));
    }

    http.end();
  } else {
    Serial.println("WiFi no conectado");
  }

  delay(10000); // 10 segundos
}
