int x;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
}

void loop() {
  while(!Serial.available());
  x = Serial.readString().toInt();
  resp(x);
}

void resp(int x){
  if(x == 0){
    Serial.print("0");
  }else if(x == 1){
    Serial.print("1");
  }else{
    Serial.print("Erreur");
  }
}
