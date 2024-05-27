#include <Wire.h>
#include "MAX30100_PulseOximeter.h"

#define REPORTING_PERIOD_MS     1000

PulseOximeter pox;

uint32_t lastBeat = 0;
float beatsPerMinute;
int32_t beatCount = 0;

void onBeatDetected()
{
  Serial.println("Detak jantung terdeteksi!");
  beatCount++;
}

void setup()
{
  Serial.begin(115200);

  // Initialize sensor
  if (!pox.begin())
  {
    Serial.println("Gagal memulai sensor MAX30100");
    for (;;)
      ;
  }
  else
  {
    Serial.println("Sensor MAX30100 berhasil dimulai");
  }

  // Set up callback for beat detection
  pox.setOnBeatDetectedCallback(onBeatDetected);
}

void loop()
{
  pox.update();

  // Calculate heart rate (BPM)
  if (millis() - lastBeat > REPORTING_PERIOD_MS)
  {
    beatsPerMinute = (beatCount / ((millis() - lastBeat) / 60000.0));
    lastBeat = millis();

    Serial.print("Detak jantung (BPM): ");
    Serial.println(beatsPerMinute);

    // Output oxygen saturation
    Serial.print("Kadar oksigen dalam darah (%): ");
    Serial.println(pox.getSpO2());

    // Reset beat count
    beatCount = 0;
  }
}
