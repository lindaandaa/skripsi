// Deklarasi pin yang akan digunakan
const int emgPin = A0;  // Pin analog untuk sensor EMG

// Variabel untuk menyimpan nilai sensor EMG
int emgValue = 0;

void setup() {
  // Mulai koneksi serial
  Serial.begin(9600);
}

void loop() {
  // Baca nilai dari sensor EMG
  emgValue = analogRead(emgPin);
  
  // Kirim nilai sensor EMG ke komputer melalui koneksi serial
  Serial.println(emgValue);
  
  // Tunggu sebentar sebelum membaca sensor lagi
  delay(10);
}
