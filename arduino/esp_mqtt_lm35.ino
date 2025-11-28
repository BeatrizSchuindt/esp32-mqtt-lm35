#include <WiFi.h>
#include <PubSubClient.h>

// ======= CONFIG WIFI =======
const char* ssid     = "Galaxy S25 Ultra D43D";   
const char* password = "87654321";      

// ======= CONFIG MQTT =======
const char* mqtt_server = "10.68.17.102";
const int   mqtt_port   = 1883;
const char* mqtt_topic  = "sensores/temperatura/lm35";

WiFiClient espClient;
PubSubClient client(espClient);

// ======= LM35 =======
const int lm35Pin = 1;
unsigned long lastMsg = 0;
const long intervalo = 2000;

// Conexão WIFI - ESP32
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando em ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado!");
  Serial.print("IP do ESP32: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Tentando conectar ao MQTT... ");

    String clientId = "ESP32-LM35-";
    clientId += String(random(0xffff), HEX);

    if (client.connect(clientId.c_str())) {
      Serial.println("conectado!");
    } else {
      Serial.print("falhou, rc=");
      Serial.print(client.state());
      Serial.println(" — tentando de novo em 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200); //frequência
  delay(1000);

  analogReadResolution(12); 
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > intervalo) {
    lastMsg = now;

    // cálculo da temperatura via mV
    int leitura = analogRead(lm35Pin);
    float tensao = (leitura * 3.3) / 4095.0;
    float tempC  = tensao * 100.0;

    Serial.print("Temp: ");
    Serial.print(tempC, 2);
    Serial.println(" °C (enviando via MQTT)");

    char payload[16];
    dtostrf(tempC, 4, 2, payload); 
    client.publish(mqtt_topic, payload);
  }
}
