#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h> // version 6
#include <TimeLib.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <Wire.h>
#include <Adafruit_ADS1X15.h>


//Wifi and MQTT information
const char* ssid = "Yasmeenetwork";
const char* password =  "plantsforlyfe";

//const char* ssid = "VIRGIN418";  // home
//const char* password =  "9A4C6744"; //home
///const char* mqtt_server = "192.168.2.140"; //home

//const char* ssid = "Makerspace-2.4G";  // home
//const char* password =  "makeymakey"; //home
//const char* mqtt_server = "192.168.0.107"; //home
const char* mqtt_server = "192.168.0.162"; 
//const int nid = 1;  // this is node ID
const int mqtt_port = 1883;
WiFiClient espClient;
PubSubClient client(mqtt_server, mqtt_port, espClient);

//Sensor variables initialization
//String volts [10] = { };
//ADC_MODE(ADC_VCC);
Adafruit_ADS1115 ads1115;

const byte ELECTRODE1=0; // PIN D3 = GPIO 0

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
  Serial.begin(115200);
  pinMode(ELECTRODE1, OUTPUT);
  digitalWrite(ELECTRODE1, LOW);

  Serial.println("Getting single-ended readings from AIN0..3");
  Serial.println("ADC Range: +/- 6.144V (1 bit = 3mV)");
  ads1115.begin();

 // because max voltage is 3.3V
 //ads1115.setGain(GAIN_ONE);     // 1x gain   +/- 4.096V  1 bit = 2mV
 //ads1115.setGain(GAIN_TWO);     // 2x gain   +/- 2.048V  1 bit = 1mV
 ads1115.setGain(GAIN_FOUR);    // 4x gain   +/- 1.024V  1 bit = 0.5mV
 //ads1115.setGain(GAIN_EIGHT);   // 8x gain   +/- 0.512V  1 bit = 0.25mV
 //ads1115.setGain(GAIN_SIXTEEN); // 16x gain  +/- 0.256V  1 bit = 0.125mV

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
    if (client.connect("ESP8266_1"))
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
  int16_t adc0, adc1, adc2, adc3;
  float volts0;
  int16_t results;
  //making json document
  StaticJsonDocument<400> doc;
  JsonArray timestamp = doc.createNestedArray("timestamp");
  timestamp.add(getTime());
  JsonArray nodeid = doc.createNestedArray("nodeid");  //node ID to change for every nodemcu
  nodeid.add(2);
  
  JsonArray data = doc.createNestedArray("data");
  
  for (int n = 0; n < 10; ++n) {
    // turning on voltage on probe
    digitalWrite(ELECTRODE1, HIGH);
    // waiting 10ms for power to come on
    delay(10);
    // reading analog sensor
    adc0 = ads1115.readADC_SingleEnded(0);
    // waiting another 10ms, just in case
    delay(10);
    // turning voltage off again
    digitalWrite(ELECTRODE1, LOW);
    //write data to json
    volts0 = ads1115.computeVolts(adc0);

    data.add(adc0);
    Serial.print("AIN0: "); Serial.print(adc0), Serial.print(" Volts: "), Serial.println(volts0), Serial.print("NODEID: "),Serial.print(nodeid);
    delay(80); // should be 10 hz, if we want 20hz reduce to 30 delay
  }
  //Publish DATA to MQTT
  char out[256];
  int b =serializeJson(doc, out);
  //Serial.print("publishing bytes = ");
  //Serial.println(b,DEC);
  client.publish("test", out);
}
