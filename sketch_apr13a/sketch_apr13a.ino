const int emgPin = A0; // Pin analog untuk membaca sinyal EMG
const float threshold = 2.5; // Ambang batas tegangan untuk menentukan otot kelelahan (misalnya 2.5 Volt)

void setup() {
  Serial.begin(9600); // Mulai komunikasi serial
}

void loop() {
  float voltage = analogRead(emgPin) * (5.0 / 1023.0); // Baca tegangan dari sinyal EMG
  Serial.print("Tegangan EMG: ");
  Serial.print(voltage);
  Serial.println(" Volt");

  if (voltage > threshold) {
    Serial.println("OTOT kelelahan");
  } else {
    Serial.println("OTOT normal");
  }

  delay(1000); // Jeda 1 detik
}
