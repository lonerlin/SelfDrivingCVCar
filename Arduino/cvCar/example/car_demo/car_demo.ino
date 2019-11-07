#include<PID.h>
#include<MotorControl.h>
#define LeftDIRPin 4
#define LeftPWMPin 5
#define RightDIRPin 7
#define RightPWMPin 6
#define Switch 2
#define BASE_SPEED 40
#define FAST_SPEED 80
int SPEED=0;
int cur=0;
int left,right;
String inStr="";
PID pid(1500,0,0);
MotorControl mc(LeftDIRPin,LeftPWMPin,RightDIRPin,RightPWMPin);

void setup() {
  Serial.begin(115200);
  while(!Serial){;}
  left=0;
  right=0;
}

void loop() {
 inStr="";
 while (Serial.available()>0){
    int inChar = Serial.read();
    //Serial.println(inChar);
    if(inStr=="" && (char)inChar=='-')inStr="-";
    if (isDigit(inChar)) {
      // convert the incoming byte to a char and add it to the string:
    inStr += (char)inChar;
    delay(1);
    }
    // if you get a newline, print the string, then the string's value:
    if (inChar == '\n') {
        break;
    }
 }
   
    if(inStr!="")cur=inStr.toInt();
    //Serial.println(cur);
    if(cur==200)
    {
      mc.Motor(0,0);
    }
    else{
      if(abs(cur)<25)SPEED=FAST_SPEED;
      else if(abs(cur)>60 )SPEED=20;
      else SPEED=BASE_SPEED;
      pid.update(cur);
     
      left=pid.m_command + SPEED;
      right=-pid.m_command + SPEED;
      //left=BASE_SPEED+cur;
      //Serial.print("left:");
      //Serial.println(left);
      //right=BASE_SPEED-cur;
      //Serial.print("right:");
      //Serial.println(right);
      //if (left>150)left=240;
      //if(right>150)right=240;
      //if(left<-150)left=-240;
      //if(right<-150)right=-240;
      
      mc.Motor(left,right);
      delay(5);
      }
  
}
