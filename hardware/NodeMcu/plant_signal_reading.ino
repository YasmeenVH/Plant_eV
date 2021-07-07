#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h> // version 6
#include <TimeLib.h>
#include <NTPClient.h>
#include <WiFiUdp.h>


//Wifi and MQTT information
const char* ssid = "Yasmeenetwork";
const char* password =  "plantsforlyfe";
const char* mqtt_server = "192.168.0.106";
const int mqtt_port = 1883;
WiFiClient espClient;
PubSubClient client(mqtt_server, mqtt_port, espClient);

//Sensor variables initialization
String volts [10] = { };
ADC_MODE(ADC_VCC);

// Initialize variable for timestamp
// Define NTP Client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "ca.pool.ntp.org");
unsigned long epochTime; 

// Function that gets current epoch time
unsigned long getTime() {
  timeClient.update();
  unsigned long now = timeClient.getEpochTime();
  return now;
}


void setup() 
{
  Serial.begin(9600);

  //Connecting to WIFI
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) 
  {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.print("Connected to WiFi :");
  Serial.println(WiFi.SSID());

  //Connecting to MQTT broker
  while (!client.connected()) 
  {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP8266"))
    {
      Serial.println("connected");
    }
    else
    {
      Serial.print("failed with state ");
      Serial.println(client.state());
      delay(2000);
    }
  }
  client.subscribe("test");
  
  //Time
  timeClient.begin();
}

void loop() 
{ 
  //Collect DATA
  StaticJsonDocument<400> doc;
  JsonArray timestamp = doc.createNestedArray("timestamp");
  timestamp.add(getTime());
  JsonArray data = doc.createNestedArray("data");
  for (int n = 0; n < 10; ++n) {
    data.add(ESP.getVcc());
    delay(200);
  }
  //Publish DATA to MQTT
  char out[256];
  int b =serializeJson(doc, out);
  //Serial.print("publishing bytes = ");
  //Serial.println(b,DEC);
  client.publish("test", out);
}
