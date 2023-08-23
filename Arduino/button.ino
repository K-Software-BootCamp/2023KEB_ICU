int push = 6;

void setup() {
  Serial.begin(9600);
  pinMode(push,INPUT_PULLUP);
}
void loop() {
  if(digitalRead(push)==1) {
    int a = digitalRead(push);
    
    Serial.println(a);
    delay(500);
  }
}
