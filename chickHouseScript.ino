//Libraries
#include <FastLED.h>//https://github.com/FastLED/FastLED

//Constants
#define NUM_STRIPS 1
#define NUM_LEDS 15
#define BRIGHTNESS 10
#define LED_TYPE WS2812B
#define COLOR_ORDER BRG//RGB
#define FASTLED_ALLOW_INTERRUPTS 0
#define FASTLED_INTERRUPT_RETRY_COUNT 1
#define FRAMES_PER_SECOND 60
#define COOLING 55
#define SPARKING 120

// Gestionnaire du bandeau LED
CRGB leds[NUM_LEDS];
const int stripPin  = 2;

// Pins de contrôle du pont en H (moteur)
const int pinIN1 = 6;
const int pinIN2 = 5;

// Pins de fin de course (moteur)
const int endH = 8;
const int endL = 9;

// Pin de validation Série
const int INA = 7;

// Pin de détecteur infrarouge
const int pinIR = 10;

// Valeurs constantes
const int timeOut = 10*1000; // 10s

// Valeurs variables
String currentPosition = "CLOSE";
bool gReverseDirection  = false;

const String initString = "START";

void setup() {
  Serial.begin(9600);

  FastLED.addLeds<LED_TYPE, stripPin, COLOR_ORDER>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);

  pinMode(pinIN1, OUTPUT);
  pinMode(pinIN2, OUTPUT);

  pinMode(endH, INPUT);
  pinMode(endL, INPUT);

  pinMode(INA, INPUT);

  pinMode(pinIR, INPUT);

  digitalWrite(pinIN1, LOW);
  digitalWrite(pinIN2, LOW);

  FixColor(255, 0, 0); // Rouge
  FixColor(0, 255, 0); // Vert
  FixColor(0, 0, 255); // Bleu
  delay(500);

  FixColor(0, 0, 0); // Eteint

  CloseDoor();

  // Attente de validation de connexion Série
  /*
  while (digitalRead(INA) == LOW) {
    Serial.println(initString);
    delay(500);
  }*/
}

void FixColor (byte r, byte g, byte b) {
  for (int i = 0; i < NUM_LEDS; i++) {
    //leds[i] = CRGB::Goldenrod;
    leds[i].setRGB(r, g, b);
  }
  FastLED.show();
  delay(500);
}

void AnimOpen () {
  for (int i = 0; i < 2; i++) {
    FixColor(0, 0, 255); // Bleu
    delay(1000);
    FixColor(0, 0, 0); // Eteint
  }

  FixColor(0, 0, 255); // Bleu
  for (int j = 0; j < NUM_LEDS; j++) {
    leds[j].setRGB(0, 0, 0); // Eteint
    FastLED.show();
    delay(50);
  }

  delay(500);
}

void AnimClose () {
  for (int i = 0; i < 2; i++) {
    FixColor(0, 0, 255); // Bleu
    delay(1000);
    FixColor(0, 0, 0); // Eteint
  }
  
  FixColor(0, 0, 0); // Eteint
  for (int j = 0; j < NUM_LEDS; j++) {
    leds[j].setRGB(0, 0, 255); // Eteint
    FastLED.show();
    delay(50);
  }

  delay(500);
}

void AnimError () {
  FixColor(255, 0, 0); // Rouge
  delay(1000);

  for (int i = 0; i < 2; i++) {
    FixColor(0, 0, 0); // Rouge
    delay(100);
    FixColor(255, 0, 0); // Eteint
  }
  
  delay(1000);
}

void AnimDetect () {
  for (int i = 0; i < NUM_LEDS; i+=2) {
    leds[i].setRGB(0, 255, 0); // Vert
  }
  FastLED.show();
}

String ReadMSG() {
  String msg = "";
  int startProcess = millis(); // Temps de début de process

  if (Serial.available()) {
    delay(10);
    while (Serial.available() > 0 && (millis() - startProcess) < timeOut) {
      msg += (char)Serial.read();
    }
    Serial.flush();
  }

  return msg;
}

bool CloseDoor () {
  bool state = false;

  AnimClose();

  int startProcess = millis(); // Temps de début de process

  // Moteur en marche avant
  digitalWrite(pinIN1, HIGH);
  digitalWrite(pinIN2, LOW);
  while (digitalRead(endL) == LOW && (millis() - startProcess) < timeOut) {
    delay(250);    
  }
  digitalWrite(pinIN2, LOW); // Arrêt du moteur

  if ((millis() - startProcess) < timeOut) {
    state = true; // Processus achevé
    currentPosition = "CLOSE";
  }

  delay(500);

  return state;
}

bool OpenDoor () {
  bool state = false;

  AnimOpen();

  int startProcess = millis(); // Temps de début de process

  // Moteur en marche avant
  digitalWrite(pinIN1, LOW);
  digitalWrite(pinIN2, HIGH);
  while (digitalRead(endL) == LOW && (millis() - startProcess) < timeOut) {
    delay(250);    
  }
  digitalWrite(pinIN2, LOW); // Arrêt du moteur

  if ((millis() - startProcess) < timeOut) {
    state = true; // Processus achevé
    currentPosition = "OPEN";
  }

  delay(500);

  return state;
}

void loop() {
  if ((ReadMSG == "OPEN" || analogRead(A0) < 900) && currentPosition == "CLOSE") {
    if (!OpenDoor()) {
      Serial.println("ERROR:OPEN");
      AnimError();
    }
  }
  else if ((ReadMSG == "CLOSE" || analogRead(A0) > 1000) && currentPosition == "OPEN"){
    if (!CloseDoor()) {
      Serial.println("ERROR:CLOSE");
      AnimError();
    }
  }

  if (digitalRead(pinIR) == HIGH && currentPosition == "CLOSE") {
    Serial.println("EVENT:DETECT");
    AnimDetect();
  }

  delay(500);
  //Serial.println(analogRead(A0));
}
