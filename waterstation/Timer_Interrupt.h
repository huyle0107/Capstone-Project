#include "M5Atom.h"
#define timeRead                60000
#define timeWaitSensor          1000
#define timeWaitResponse        30000
#define timeWaitRelay           5000
#define timeClearBuffer         60000
#define timeExecuteResponse     180000
#define timeSleep               420000
//#define timeSleep               120000  

extern int timer_flag;
extern int timer1_flag;
void setTimer(int duration);
void setTimer1(int duration);
void timerRun();
