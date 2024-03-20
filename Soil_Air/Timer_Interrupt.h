#include "M5Atom.h"
#define timeRead                60000
#define timeWaitSensor          1000
#define timeWaitResponse        5000
#define timeWaitRelay           5000
#define timeSleep               540000
//#define timeSleep               60000  

extern int timer_flag;
extern int timer1_flag;
void setTimer(int duration);
void setTimer1(int duration);
void timerRun();
