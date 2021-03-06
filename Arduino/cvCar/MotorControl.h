//马达控制实际类
class MotorControl
{
public:
    MotorControl(int leftDIR,int leftPWM,int rightDIR,int rightPWM)
    {
        pinMode(leftDIR,OUTPUT);
        pinMode(rightDIR,OUTPUT);
        leftdir=leftDIR;
        leftpwm=leftPWM;
        rightdir=rightDIR;
        rightpwm=rightPWM;
    }

    void Motor(int left,int right)
    {
      setMotor(-left,leftdir,leftpwm);
      setMotor(right,rightdir,rightpwm);
    }
    void setMotor(int mSpeed,int DIR,int PWM)
    {
        if(mSpeed>255) mSpeed=255;
        if(mSpeed<-255)mSpeed=-255;


        if(mSpeed>=0)
        {
            digitalWrite(DIR,HIGH);
            analogWrite(PWM,mSpeed);
        }
        else
        {
            digitalWrite(DIR,LOW);
            analogWrite(PWM,abs(mSpeed));
        }
    }

private:
        int leftdir;
        int leftpwm;
        int rightdir;
        int rightpwm;
};
