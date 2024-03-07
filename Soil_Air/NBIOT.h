#include "Config.h"
#include <M5Atom.h>

extern bool isListen;
extern bool getResponse;

void IRAM_ATTR resetModule();
void sendATCommand(const char* command);
void waitAndReadResponse();
void NBIOT_Init();
void NBIOT_CheckConnection();
void NBIOT_ConnectMQTT();
void NBIOT_SubTopic(const String& topic);
void NBIOT_listenCallback();
void NBIOT_publishData(const String& topic,const String& str);