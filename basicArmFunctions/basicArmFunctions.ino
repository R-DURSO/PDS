/*
  testBraccio90.ino
 testBraccio90 is a setup sketch to check the alignment of all the servo motors
 This is the first sketch you need to run on Braccio
 When you start this sketch Braccio will be positioned perpendicular to the base
 If you can't see the Braccio in this exact position you need to reallign the servo motors position
 Created on 18 Nov 2015
 by Andrea Martino
 This example is in the public domain.
 */

#include <Braccio.h>
#include <Servo.h>

void waitAtSafetyPos(int signal, bool isClosed, bool isWaiting);
int getSignal();
void putObjectAsideGood();
void putObjectAsideBad();
void pickObjectAtHisLeft();
void pickObjectAtHisRight();
void pickGoodObject(bool isWaiting);
void pickBadObject(bool isWaiting);


Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

bool isClosed = true;
bool isWaiting = false;
int mySignal;


void setup() {  
  //Initialization functions and set up the initial position for Braccio
  //All the servo motors will be positioned in the "safety" position:
  //Base (M1):90 degrees
  //Shoulder (M2): 45 degrees
  //Elbow (M3): 180 degrees
  //Wrist vertical (M4): 180 degrees
  //Wrist rotation (M5): 90 degrees
  //gripper (M6): 10 degrees
  Braccio.begin();
  Serial.begin(9600);
}





void loop() {
  if (Serial.available() > 0) {
  mySignal = getSignal();

  // the arm is aligned upwards  and the gripper is closed
                     //(step delay, M1, M2, M3, M4, M5, M6);
  if(mySignal == '1'){
    waitAtSafetyPos(mySignal, false, isWaiting);
  }else if(mySignal == '2'){
    pickGoodObject(isWaiting);
  }else if(mySignal == '3'){
    pickBadObject(isWaiting);
  }
  mySignal = 0;
  }
}

void pickGoodObject(bool isWaiting){
  isWaiting = false;
  pickObjectAtHisLeft();
  putObjectAsideGood();
  Serial.write("end\n");
}

void pickBadObject(bool isWaiting){
  isWaiting = false;
  pickObjectAtHisRight();
  putObjectAsideBad();
  Serial.write("end\n");
}

void pickObjectAtHisLeft(){
  /*
   Step Delay: a milliseconds delay between the movement of each servo.  Allowed values from 10 to 30 msec.
   M1=base degrees. Allowed values from 0 to 180 degrees
   M2=shoulder degrees. Allowed values from 15 to 165 degrees
   M3=elbow degrees. Allowed values from 0 to 180 degrees
   M4=wrist vertical degrees. Allowed values from 0 to 180 degrees
   M5=wrist rotation degrees. Allowed values from 0 to 180 degrees
   M6=gripper degrees. Allowed values from 10 to 73 degrees. 10: the toungue is open, 73: the gripper is closed.
  */
                       //(step delay, M1, M2, M3, M4, M5, M6);
    Braccio.ServoMovement(20,         90, 90, 45, 25, 85, 10);
    
    Serial.write("stop\n");
    Braccio.ServoMovement(20,         90, 70, 20, 25, 85, 10);
    //Braccio.ServoMovement(20, 90, 39, 190, 188, 90, 10);
    //Braccio.ServoMovement(20, 90, 39, 190, 188, 90, 73);
    Braccio.ServoMovement(20,         90, 70, 20, 25, 85, 73);
    Braccio.ServoMovement(20,         90, 90, 45, 25, 85, 73);
  //delay for testing purpose
}

void pickObjectAtHisRight(){
    Braccio.ServoMovement(20,         110, 90, 45, 25, 85, 10);
    Serial.write("stop\n");
    Braccio.ServoMovement(20,         110, 70, 20, 25, 85, 10);
    Braccio.ServoMovement(20,         110, 70, 20, 25, 85, 10);
    Braccio.ServoMovement(20,         110, 90, 45, 25, 85, 10);
}


void putObjectAsideGood(){
                       //(step delay, M1, M2, M3, M4, M5, M6);
    Braccio.ServoMovement(20,         0, 90, 45, 25, 85, 73);
    Braccio.ServoMovement(20,         0, 70, 20, 25, 85, 73);
    Braccio.ServoMovement(20,         0, 70, 20, 25, 85, 10);
    Braccio.ServoMovement(20,         0, 90, 45, 25, 85, 10);

}

void putObjectAsideBad(){
                       //(step delay, M1, M2, M3, M4, M5, M6);
    Braccio.ServoMovement(20,         180, 90, 45, 25, 85, 73);
    Braccio.ServoMovement(20,         180, 70, 20, 25, 85, 73);
    Braccio.ServoMovement(20,         180, 70, 20, 25, 85, 10);
    Braccio.ServoMovement(20,         180, 90, 45, 25, 85, 10);

}

/*
 * function to wait on the safety position.
 * Intended use: receive a signal in a while loop, 
 * while this signal is 1, wait. if the arm has taken
 * an object in the griper, @param isClosed has to be true,
 * otherwise the griper will be open
 */

void waitAtSafetyPos(int signal, bool isClosed, bool isWaiting){
  if(!isWaiting){
    isClosed ? Braccio.ServoMovement(20, 90, 135, 0, 0, 90, 10):Braccio.ServoMovement(20, 90, 135, 0, 0, 90, 73);
    delay(1000);
    Serial.write("Waiting at safety pos \n");
    isWaiting = true;
  }else{
    Serial.write("Still waiting at safety pos \n");
  }
    
}


//testing purpose
int getSignal(){
  int incomingByte = 0;
   
  // read the incoming byte:
  incomingByte = Serial.read();

  // say what you got:
  Serial.write("Arduino received: ");
  Serial.write(incomingByte);
  Serial.write("\n");
  return incomingByte;        
}
