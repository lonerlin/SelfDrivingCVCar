/*
  Arduino 起到连接jetson nano 主控和电机的作用。
  考虑用Arduino来控制电机，主要是隔断主控板与电机间的联系，保护jetson nano的安全。
  约定通过一个8为数字来传送左右马达的转速：
    每个四位，如果第四位等于1代表马达向后，0代表马达向前（既是1代表负）
    左边四位是左马达，右边四位是右马达
*/

#include<MotorControl.h>
#define LeftDIRPin 4
#define LeftPWMPin 5
#define RightDIRPin 7
#define RightPWMPin 6
#define Switch 2
#define BASE_SPEED 45
#define FAST_SPEED 70
int SPEED=0;
int cur=0;
int left,right;
String inStr="";

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
    if(inStr!="" && inStr.length()== 8 )
    {
       int tmp;
       cur=inStr.toInt();
       
       //左边整除
       tmp =cur/10000;
       if(tmp /1000 >0)left=-tmp%1000;
       else left=tmp%1000;

       //右边取余
       tmp =cur %10000;
       if(tmp/1000>0)right=-tmp%1000;
       else  right=tmp%1000;
       
       mc.Motor(left,right);
       
    }
    else
    {
      mc.Motor(0,0);  
    }
    delay(5);
    
 }
