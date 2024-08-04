void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0){
    String msg = Serial.readString();

    if (msg == "FAST"){
      for (int i=0; i<10; i++){
        digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
        delay(500);                      // wait for a second
        digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
        delay(500);  
      }
    }
    else if (msg == "SLOW"){
      for (int i=0; i<10; i++){
        digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
        delay(2000);                      // wait for a second
        digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
        delay(2000); 
      }
    }
  }
}