#include <Wire.h>
#include <Adafruit_ADS1X15.h>

Adafruit_ADS1115 ads1115;

const byte ELECTRODE1=0; // PIN D3 = GPIO 0

void setup(void)
{
  Serial.begin(115200);
  Serial.println("Hello!");

  pinMode(ELECTRODE1, OUTPUT);
  digitalWrite(ELECTRODE1, LOW);

  Serial.println("Getting single-ended readings from AIN0..3");
  Serial.println("ADC Range: +/- 6.144V (1 bit = 3mV)");
  ads1115.begin();

 // because max voltage is 3.3V
 ads1115.setGain(GAIN_ONE);     // 1x gain   +/- 4.096V  1 bit = 2mV
// ads1115.setGain(GAIN_TWO);     // 2x gain   +/- 2.048V  1 bit = 1mV
// ads1115.setGain(GAIN_FOUR);    // 4x gain   +/- 1.024V  1 bit = 0.5mV
// ads1115.setGain(GAIN_EIGHT);   // 8x gain   +/- 0.512V  1 bit = 0.25mV
// ads1115.setGain(GAIN_SIXTEEN); // 16x gain  +/- 0.256V  1 bit = 0.125mV
}

void loop(void)
{
  int16_t adc0, adc1, adc2, adc3;
  float volts0;
  int16_t results;

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

  volts0 = ads1115.computeVolts(adc0);
  Serial.print("AIN0: "); Serial.print(adc0), Serial.print(" Volts: "), Serial.println(volts0);

  // waiting 91ms between readings so that the recording frequency is >10Hz to get 5Hz data
  delay(71); // 91 - 10 - 10
}