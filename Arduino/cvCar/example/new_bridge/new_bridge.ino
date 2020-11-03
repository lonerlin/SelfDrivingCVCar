  /*
  Arduino 起到连接jetson nano 主控和电机的作用。
  考虑用Arduino来控制电机，主要是隔断主控板与电机间的联系，保护jetson nano的安全。
  约定通过一个8为数字来传送左右马达的转速：
    每个四位，如果第四位等于1代表马达向后，0代表马达向前（既是1代表负）
    左边四位是左马达，右边四位是右马达
    另外，如果最左一位是2，代表这是舵机的控制指令，当前小车只有一个测试用的舵机，所有只用到左4位。
    当需要多个舵机时，可以用到右四位，或是最左一位为3，4等等。
  */

#include <Servo.h>
#include<MotorControl.h>
#define LeftDIRPin 4         //左马达方向针脚
#define LeftPWMPin 5         //左马达PWM
#define RightDIRPin 7        //右方向针脚
#define RightPWMPin 6        //右马达PWM
int angle = 0;
int start_angle1=90;
int start_angle2=90;
int left,right;
String inStr="";
bool is_Send=true;

int buttonPin1=2;
int buttonPin2=3;


Servo servo1;
Servo servo2;
MotorControl mc(LeftDIRPin,LeftPWMPin,RightDIRPin,RightPWMPin);

void setup() {
  pinMode(13, OUTPUT);
  left=0;
  right=0;
  mc.Motor(left,right);
  Serial.begin(115200);
  while(!Serial){;}

   servo1.attach( 9, 600, 2400 );
   servo1.write(0);
   servo2.attach( 10, 600, 2400 );
   servo2.write(0);
   pinMode(buttonPin1,INPUT);
   pinMode(buttonPin2,INPUT);
}

void loop() {
    inStr="";
    while (Serial.available()>0){
      int inChar = Serial.read();
      //Serial.println(inChar);
      
      if (isDigit(inChar)) {
      inStr += (char)inChar;        // 如果是0-9那么并入字符串中:

      delay(1);
      }
      // 换行符表示结束
      if (inChar == '\n') {
          break;
      }
      
      
    }
    decode_message();
    delay(5);
    
}
void decode_message()
{
    //如果传送出错，立刻停止 
    if(inStr!="" && inStr.length()==8 )
    {
       int tmp;
       if(is_Send)
       {
            Serial.print("string:");
            Serial.println(inStr);
       }
       inStr = inStr + "";
       if(inStr.substring(0,1)=="9")
       {
            is_Send=true;
            digitalWrite(13,HIGH);
       }
       if(inStr.substring(0,1)=="2")
       {
          angle = inStr.substring(1,4).toInt();

          if(is_Send)
          {
            Serial.print("angle:");
            Serial.println(angle);
          }
          if (inStr.substring(7,8).toInt()==0)
          {
            //servo_move(servo1,start_angle1,angle);
           // start_angle1=angle;
           servo1.write(angle);
          }
          else
          {
            //servo_move(servo2,start_angle2,angle);
            //start_angle2=angle;
            servo2.write(angle);
          }
       }
       else
       {
         tmp =inStr.substring(0,4).toInt();
         //Serial.println(tmp);
         if(tmp /1000 >0)left=-tmp%1000;
         else left=tmp%1000;
  
         //右边取余
         tmp =inStr.substring(4,8).toInt();
         //Serial.println(tmp);
         if(tmp/1000>0)right=-tmp%1000;
         else  right=tmp%1000;
         
         mc.Motor(left,right);
         if (is_Send)
         {
            Serial.print("left:");
            Serial.println(left);
            Serial.print("right:");
            Serial.println(right);
         }
       }

    }
}
//控制舵机的转向
//servo:舵机对象
//start_angle:开始角度
//end_angle:结束角度
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
//检查按钮状态的的函数，有需要时在loop中调用
void checkButton()
{
    if(debounce(buttonPin1,5))Serial.println("30000011");
    if(debounce(buttonPin2,5))Serial.println("30000021");
}
//去抖函数，用于检查引脚状态
bool debounce(int pin,int debounceDelay)
{
    bool state;
    bool previousState;
    pinMode(pin, INPUT);
    previousState=digitalRead(pin);
    for(int counter=0;counter<debounceDelay;counter++)
    {
      delay(1);
      state=digitalRead(pin);
      if(state!=previousState)
        {
           counter=0;
           previousState=state;
        }
     }
    return state;
}
