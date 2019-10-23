#include<PID.h>
#include<MotorControl.h>
#define LeftDIRPin 4
#define LeftPWMPin 5
#define RightDIRPin 7
#define RightPWMPin 6
#define Switch 2
#define BASE_SPEED 70

int cur=0;

PID pid(1200,0,0);
MotorControl mc(LeftDIRPin,LeftPWMPin,RightDIRPin,RightPWMPin);

void setup() {
  Serial.begin(115200);
  pinMode(2,INPUT);

}

void loop() {
   int left,right;
  
   while(digitalRead(Switch))
  {
      mc.Motor(0,0);
  }

 if(Serial.available())
  {
    
    cur=Serial.parseInt();
    
    Serial.println(cur);
    pid.update(cur);
    left=pid.m_command + BASE_SPEED;
    right=-pid.m_command +BASE_SPEED;
    Serial.print("left:");
    Serial.println(left);
    Serial.print("right:");
    Serial.println(right);
    mc.Motor(left,right);
    
  }
}
