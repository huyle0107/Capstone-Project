#include <tuple>
#include "NBIOT.h"

bool isListen = false;
bool getResponse = false;


void IRAM_ATTR resetModule() 
{
  ets_printf("reboot\n");
  esp_restart();
}


void NBIOT_listenCallback(){
  if(isListen){
    while (!SerialNBIOT.available()) {}
    String receivedData = "";
    while (SerialNBIOT.available()) {
      char c = SerialNBIOT.read();
      receivedData += c;
    }
    if(receivedData.indexOf("+CMQPUB: 0") != -1)  getResponse = true;
  }
}


void sendATCommand(const char* command) {
  SerialMon.println(command);
  //sendATCommand(command);

  //Serial1.println(command);
  SerialNBIOT.write(command);
  SerialNBIOT.write("\r"); // Gửi ký tự CR (Enter)

  waitAndReadResponse(); 
}

void waitAndReadResponse() {
  while (!SerialNBIOT.available()) {}
  //delay(2000);
  while (SerialNBIOT.available()) {
    char c = SerialNBIOT.read();
    SerialMon.print(c);
  }
}

void NBIOT_Init(){
 // Init NBIOT
  sendATCommand("AT");
  sendATCommand("ATZ");
  sendATCommand("AT+CPIN?");
  sendATCommand("AT+CCID");
  sendATCommand("AT+COPS?");
  sendATCommand("AT+CEREG?");
  
  //Attach network
  sendATCommand("AT+CBAND=3");
  sendATCommand("AT+CGDCONT=1,\"IP\",\"nbiot\"");
  sendATCommand("AT+COPS=0");
  sendATCommand("AT+CGCONTRDP");
}

void NBIOT_CheckConnection(){
  sendATCommand("AT+CGREG=0");
  sendATCommand("AT+COPS?");
  sendATCommand("AT+CSQ");
  sendATCommand("AT+CENG?");
  sendATCommand("AT+CMQDISCON=0");
  sendATCommand("ATE0");
}

void  NBIOT_ConnectMQTT(){
  // sendATCommand("AT+CMQTSYNC=1");
  // delay(100);
  // readResponse();   
  sendATCommand("AT+CMQTSYNC=1");
  sendATCommand("AT+CMQNEW=\"mqttserver.tk\",\"1883\",12000,1024");\
  sendATCommand("AT+CMQCON=0,3,\"SoilAir\",600,1,0,\"innovation\",\"Innovation_RgPQAZoA5N\"");
}

void NBIOT_SubTopic(const String& topic){
  String SubString = "AT+CMQSUB=0,\"" + topic + "\",1";
  sendATCommand(SubString.c_str());
}

String sendPublish(const char* command){
  SerialMon.println(command);
  SerialNBIOT.write(command);
  SerialNBIOT.write("\r"); // Gửi ký tự CR (Enter)

  String response = "";
  delay(2000);
  while (SerialNBIOT.available()) {
    char c = SerialNBIOT.read();
    SerialMon.print(c);
    response += c;
  }
  return response;
}


void NBIOT_publishData(const String& topic,const String& str){
  String newStr = "";
  for (char c : str) {
    newStr += (c == '"') ? '\'' : c;
  }
  //Create MQTT string
  String mqttString = "AT+CMQPUB=0,\"" + topic + "\",1,1,0," + String(newStr.length()) + ",\"" + newStr + "\"";
 
 sendATCommand(mqttString.c_str());
 isListen = true;
}