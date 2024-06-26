#include "Config.h"
#include <M5Atom.h>
#include "Timer_Interrupt.h"

extern bool isListen;
extern bool getResponse;


void sendATCommand(const char* command);
String waitAndReadResponse();
void NBIOT_Init();
void NBIOT_CheckConnection();
void NBIOT_ConnectMQTT();
void NBIOT_SubTopic(const String& topic);
void NBIOT_publishData(const String& topic,const String& str);
void NBIOT_ListenCallback();
void NBIOT_clearBuffer(void);