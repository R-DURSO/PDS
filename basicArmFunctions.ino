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

void waitAtSafetyPos(int signal, bool isClosed);
int getSignal();
void putObjectAsideGood();
void putObjectAsideBad();
void pickObjectAtHisLeft();
void pickObjectAtHisRight();


Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

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
}





void loop() {
  int mySignal = getSignal();

  // the arm is aligned upwards  and the gripper is closed
                     //(step delay, M1, M2, M3, M4, M5, M6);
  pickObjectAtHisLeft();
  putObjectAsideGood();
  pickObjectAtHisRight();
  putObjectAsideBad();
  while(mySignal == 1){
    waitAtSafetyPos(mySignal, false);
    mySignal = getSignal;
  }
  
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
    Braccio.ServoMovement(20,         80, 90, 45, 25, 85, 10);
    Braccio.ServoMovement(20,         80, 70, 20, 25, 85, 10);
    Braccio.ServoMovement(20,         80, 70, 20, 25, 85, 73);
    Braccio.ServoMovement(20,         80, 90, 45, 25, 85, 73);
  //delay for testing purpose
}

void pickObjectAtHisRight(){
    Braccio.ServoMovement(20,         110, 90, 45, 25, 85, 10);
    Braccio.ServoMovement(20,         110, 70, 20, 25, 85, 10);
    Braccio.ServoMovement(20,         110, 70, 20, 25, 85, 73);
    Braccio.ServoMovement(20,         110, 90, 45, 25, 85, 73);
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

void waitAtSafetyPos(int signal, bool isClosed){
  if(signal== '1'){
    isClosed ? Braccio.ServoMovement(20, 90, 15, 180, 150, 90, 10):Braccio.ServoMovement(20, 90, 15, 180, 150, 90, 73);
    delay(1000);
  }

}


//testing purpose
int getSignal(){
  return 1;
}
