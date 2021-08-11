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
const char* mqtt_server = "192.168.0.125";
//const char* mqtt_server = "10.0.0.66";
const int mqtt_port = 1883;
WiFiClient espClient;
PubSubClient client(mqtt_server, mqtt_port, espClient);

//Sensor variables initialization
Adafruit_ADS1115 ads1115;
String volts [10] = { };
float val = 0; //value for storing moisture value 
//int soilPin = A0;//Declare a variable for the soil moisture sensor 
//int soilPower = 2;//Variable for Soil moisture Power
int16_t adc0; // adc1, adc2, adc3;
//float volts0;


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

//Funciton to read plant signal
int readeV()
{
  //digitalWrite(soilPower, HIGH);
  //delay(10);//wait 10 milliseconds 
  //val = analogRead(soilPin); 
  //digitalWrite(soilPower, LOW);
  adc0 = ads1115.readADC_SingleEnded(0);
  val = ads1115.computeVolts(adc0);
  return adc0;//send current moisture value
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
  client.publish("test", "allo");
  
  //Time
  timeClient.begin();

  //Pin setup
  ads1115.begin();
  ads1115.setGain(GAIN_ONE);     // 1x gain   +/- 4.096V  1 bit = 2mV 
  // ads1115.setGain(GAIN_TWO);     // 2x gain   +/- 2.048V  1 bit = 1mV
  // ads1115.setGain(GAIN_FOUR);    // 4x gain   +/- 1.024V  1 bit = 0.5mV
  // ads1115.setGain(GAIN_EIGHT);   // 8x gain   +/- 0.512V  1 bit = 0.25mV
  // ads1115.setGain(GAIN_SIXTEEN); // 16x gain  +/- 0.256V  1 bit = 0.125mV
}

void loop() 
{ 
  //Collect DATA
  StaticJsonDocument<400> doc;
  JsonArray timestamp = doc.createNestedArray("timestamp");
  JsonArray data = doc.createNestedArray("data");
  timestamp.add(getTime());
  for (int n = 0; n < 10; ++n) {
    int eV = readeV();
    data.add(eV);
    delay(200);
  }
  //Publish DATA to MQTT
  char out[256];
  int b =serializeJson(doc, out);
  //Serial.print("publishing bytes = ");
  //Serial.println(b,DEC);
  client.publish("test", out);
  //delay(10000);
}
