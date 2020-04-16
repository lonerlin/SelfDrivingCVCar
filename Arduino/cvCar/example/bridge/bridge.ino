  /*
  Arduino 起到连接jetson nano 主控和电机的作用。
  考虑用Arduino来控制电机，主要是隔断主控板与电机间的联系，保护jetson nano的安全。
  约定通过一个8为数字来传送左右马达的转速：
    每个四位，如果第四位等于1代表马达向后，0代表马达向前（既是1代表负）
    左边四位是左马达，右边四位是右马达
*/
#include <Servo.h>
#include<MotorControl.h>
#define LeftDIRPin 4
#define LeftPWMPin 5
#define RightDIRPin 7
#define RightPWMPin 6
#define Switch 2
#define BASE_SPEED 45
#define FAST_SPEED 70
int SPEED=0;
int angle = 90;
int start_angle=angle;
int left,right;
String inStr="";

Servo servo1;
MotorControl mc(LeftDIRPin,LeftPWMPin,RightDIRPin,RightPWMPin);

void setup() {
 Serial.begin(115200);
  while(!Serial){;}
  left=0;
  right=0;
   servo1.attach( 9, 600, 2400 );
   servo1.write(90);
}

void loop() {
   
    while (Serial.available()>0){
      int inChar = Serial.read();
      //Serial.println(inChar);
      
      if (isDigit(inChar)) {
        // 如果是0-9那么并入字符串中:
      inStr += (char)inChar;
      delay(1);
      }
      // 换行符表示结束
      if (inChar == '\n') {
          break;
      }
      
      
    }
    
    //如果传送出错，立刻停止 
    if(inStr!="" && inStr.length()==8 )
    {
       int tmp;
       Serial.print("string:");
       Serial.println(inStr);
       inStr = inStr + "";

       if(inStr.substring(0,1)=="2")
       {
          angle = inStr.substring(1,4).toInt();
          Serial.print("angle:");
          Serial.print(angle);
          servo_move(servo1,start_angle,angle);
          start_angle=angle;
          
       }
       else
       {
         tmp =inStr.substring(0,4).toInt();
         Serial.println(tmp);
         if(tmp /1000 >0)left=-tmp%1000;
         else left=tmp%1000;
  
         //右边取余
         tmp =inStr.substring(4,8).toInt();
         Serial.println(tmp);
         if(tmp/1000>0)right=-tmp%1000;
         else  right=tmp%1000;
         
         mc.Motor(left,right);
         Serial.print("left:");
         Serial.println(left);
         Serial.print("right:");
         Serial.println(right);
       }
       inStr="";
    }
    
    delay(5);
    
 }


void servo_move(Servo servo,int start_angle,int end_angle){
  if (angle<10)angle=20;
  if(angle>170)angle=160;
  
  if(start_angle<end_angle){
    for(int i=start_angle;i<=end_angle;i=i+2){
      servo.write(i);
      delay(20);
    }
  }else{
    for(int i=start_angle;i>=end_angle;i=i-2){
      servo.write(i);
      delay(20);
    }
  }
}
