#define PID_MAX_INTEGRAL         2000
#define ZUMO_BASE_DEADBAND       10
public class PID
{
    public PID(int32_t pgain, int32_t igain, int32_t dgain)
    {
        m_pgain = pgain;
        m_igain = igain;
        m_dgain = dgain;
        reset();
    }

    void reset()
    {
        m_command = 0;
        m_integral = 0;
        m_prevError = 0x80000000L;
    }

    public void update(int32_t error)
    {
        int32_t pid;

        if (m_prevError!=0x80000000L)
        {
            // integrate integral
            m_integral += error;
            // bound the integral
            if (m_integral>PID_MAX_INTEGRAL)
                m_integral = PID_MAX_INTEGRAL;
            else if (m_integral<-PID_MAX_INTEGRAL)
                m_integral = -PID_MAX_INTEGRAL;

            // calculate PID term
            pid = (error*m_pgain + ((m_integral*m_igain)>>4) + (error - m_prevError)*m_dgain)>>10;


            // Deal with Zumo base deadband
            if (pid>0)
                pid += ZUMO_BASE_DEADBAND;
            else if (pid<0)
                pid -= ZUMO_BASE_DEADBAND;
         m_command = pid; // Zumo base is velocity device, use the pid term directly

        }

        // retain the previous error val so we can calc the derivative
        m_prevError = error;
    }

    public int32_t m_command;

    private:
        int32_t m_pgain;
        int32_t m_igain;
        int32_t m_dgain;

        int32_t m_prevError;
        int32_t m_integral;

};
