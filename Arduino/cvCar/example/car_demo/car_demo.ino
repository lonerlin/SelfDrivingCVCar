#include<PID.h>
#include<MotorControl.h>
#define LeftDIRPin 4
#define LeftPWMPin 5
#define RightDIRPin 7
#define RightPWMPin 6
#define Switch 2
#define BASE_SPEED 60

int cur=0;
 int left,right;

PID pid(800,0,0);
MotorControl mc(LeftDIRPin,LeftPWMPin,RightDIRPin,RightPWMPin);

void setup() {
  Serial.begin(115200);
  pinMode(2,INPUT);
  left=0;
  right=0;
}

void loop() {
 if(Serial.available())
  {
    
    cur=Serial.parseInt();
    if(cur==200)mc.Motor(0,0);
    //Serial.println(cur);
    else{
      pid.update(cur);
      Serial.println(cur);
      //left=pid.m_command + BASE_SPEED;
      //right=-pid.m_command +BASE_SPEED;
      left=BASE_SPEED+cur;
      right=BASE_SPEED-cur;
      if (left>150)left=150;
      if(right>150)right=150;
      if(left<-150)left=-150;
      if(right<-150)right=-150;
      
      mc.Motor(left,right);
      }
  }
}
