/*
 * Script de diagnóstico para el ESP32 - Invernadero
 * Este script ayuda a diagnosticar problemas de conectividad y API
 */

#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configuración WiFi
const char* ssid = "Cereza";
const char* password = "robotica25";

// URL del servidor
const char* serverUrl = "https://floracore.onrender.com/api/parameters/";

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("=== DIAGNÓSTICO ESP32 - INVERNADERO ===");
  Serial.println();
  
  // Test 1: Conectividad WiFi
  testWiFiConnection();
  
  // Test 2: Resolución DNS
  testDNSResolution();
  
  // Test 3: Conectividad HTTPS
  testHTTPSConnection();
  
  // Test 4: Envío de datos de prueba
  testAPICall();
  
  Serial.println("=== DIAGNÓSTICO COMPLETADO ===");
}

void loop() {
  // No hacer nada en el loop
  delay(10000);
}

void testWiFiConnection() {
  Serial.println("Test 1: Conectividad WiFi");
  Serial.println("-------------------------");
  
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println(" ✓ CONECTADO");
    Serial.println("IP: " + WiFi.localIP().toString());
    Serial.println("Gateway: " + WiFi.gatewayIP().toString());
    Serial.println("DNS: " + WiFi.dnsIP().toString());
    Serial.println("RSSI: " + String(WiFi.RSSI()) + " dBm");
  } else {
    Serial.println(" ✗ FALLÓ");
    Serial.println("Estado WiFi: " + String(WiFi.status()));
  }
  Serial.println();
}

void testDNSResolution() {
  Serial.println("Test 2: Resolución DNS");
  Serial.println("----------------------");
  
  IPAddress ip;
  if (WiFi.hostByName("floracore.onrender.com", ip)) {
    Serial.println("✓ DNS resuelto correctamente");
    Serial.println("IP de floracore.onrender.com: " + ip.toString());
  } else {
    Serial.println("✗ Error en resolución DNS");
  }
  Serial.println();
}

void testHTTPSConnection() {
  Serial.println("Test 3: Conectividad HTTPS");
  Serial.println("---------------------------");
  
  WiFiClientSecure client;
  client.setInsecure(); // Para pruebas, no verificar certificado
  
  if (client.connect("floracore.onrender.com", 443)) {
    Serial.println("✓ Conexión HTTPS establecida");
    client.stop();
  } else {
    Serial.println("✗ Error en conexión HTTPS");
  }
  Serial.println();
}

void testAPICall() {
  Serial.println("Test 4: Llamada a la API");
  Serial.println("-------------------------");
  
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("✗ WiFi no conectado, saltando test");
    return;
  }
  
  WiFiClientSecure client;
  client.setInsecure();
  HTTPClient http;
  
  http.setTimeout(15000); // 15 segundos timeout
  http.begin(client, serverUrl);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Accept", "application/json");
  http.addHeader("User-Agent", "ESP32-Diagnostico/1.0");
  
  // Datos de prueba
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["temperatura"] = 25.5;
  jsonDoc["humedad"] = 60.0;
  jsonDoc["humedad_suelo"] = 45.0;
  jsonDoc["luz"] = 80.0;
  
  String jsonData;
  serializeJson(jsonDoc, jsonData);
  
  Serial.println("Enviando: " + jsonData);
  
  int httpResponseCode = http.POST(jsonData);
  
  Serial.println("Código de respuesta: " + String(httpResponseCode));
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Longitud de respuesta: " + String(response.length()));
    
    if (httpResponseCode == 200 || httpResponseCode == 201) {
      Serial.println("✓ API respondió correctamente");
      
      // Mostrar primeros 300 caracteres de la respuesta
      Serial.println("Respuesta (primeros 300 chars):");
      Serial.println(response.substring(0, min(300, (int)response.length())));
      
      // Intentar parsear JSON
      StaticJsonDocument<1024> doc;
      DeserializationError error = deserializeJson(doc, response);
      
      if (error) {
        Serial.println("✗ Error parseando JSON: " + String(error.f_str()));
      } else {
        Serial.println("✓ JSON parseado correctamente");
        if (doc.containsKey("acciones")) {
          Serial.println("✓ Campo 'acciones' encontrado");
        } else {
          Serial.println("⚠ Campo 'acciones' no encontrado");
        }
      }
    } else {
      Serial.println("✗ Error HTTP: " + String(httpResponseCode));
      Serial.println("Respuesta: " + response.substring(0, min(200, (int)response.length())));
    }
  } else {
    Serial.println("✗ Error de conexión: " + http.errorToString(httpResponseCode));
  }
  
  http.end();
  Serial.println();
}