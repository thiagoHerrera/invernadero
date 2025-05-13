#include <WiFi.h>
#include <HTTPClient.h>

// Reemplazar con tu red Wi-Fi
const char* ssid = "Cereza";
const char* password = "robotica";

// URL de tu API en el servidor Django
const char* serverUrl = "http://192.168.1.60:8000/api/sensors";

void setup() {
  Serial.begin(115200);
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

    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Simulando lectura de sensores (podés cambiarlo por lectura real)
    float temperatura = 25.5;
    float humedad = 60.0;
    float humedad_suelo = 70.3;

    // Cuerpo del POST en formato JSON (corregido)
    String jsonData = "{\"temperatura\": " + String(temperatura, 1) +
                      ", \"humedad\": " + String(humedad, 1) +
                      ", \"humedad_suelo\": " + String(humedad_suelo, 1) + "}";

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

  delay(10000); // Espera 10 segundos antes del próximo envío
}
