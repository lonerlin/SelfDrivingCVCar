class MotorControl
{
    Motor(int leftDIR,int leftPWM,int rightDIR,rightPWM)
    {
        pinMode(leftDIR,OUTPUT);
        pinMode(rightDIR,OUTPUT);
        leftdir=leftDIR;
        leftpwm=leftPWM;
        rightdir=rightdir;
        rightpwm=rightpwm;
    }

    public void Motor(int left,int right)
    {
      setMotor(left,leftdir,Leftpwm);
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
