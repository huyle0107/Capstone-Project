#include "NBIOT.h"

bool isListen = false;
bool getResponse = false;


void IRAM_ATTR resetModule() 
{
  ets_printf("reboot\n");
  esp_restart();
}



void sendATCommand(const char* command) {
  SerialMon.println(command);
  //sendATCommand(command);

  //Serial1.println(command);
  SerialNBIOT.write(command);
  SerialNBIOT.write("\r"); // Gửi ký tự CR (Enter)

  String result = waitAndReadResponse(); 
  if(result.indexOf("OK") != -1 && isListen){
    getResponse = true;
  }
  if(!(result.indexOf("OK") != -1 || result.indexOf("ER") != -1)){
    result = waitAndReadResponse();
  }
}
void NBIOT_ListenCallback(){
  String receivedData = "";
  while (SerialNBIOT.available()) {
      char c = SerialNBIOT.read();
      receivedData += c;
  }
  if(receivedData.indexOf("+CMQPUB: 0,") != -1) getResponse = true;
}

String waitAndReadResponse() {
  while (!SerialNBIOT.available()) {}
  //delay(2000);

  String receivedData = "";
  while (SerialNBIOT.available()) {
      char c = SerialNBIOT.read();
      receivedData += c;
  }
  SerialMon.println(receivedData);
  return receivedData;
}


void NBIOT_Init(){
 // Init NBIOT
  SerialMon.begin(Monitor_baudrate, SERIAL_8N1, Monitor_RX, Monitor_TX);
  SerialNBIOT.begin(NBIOT_baudrate, SERIAL_8N1, NBIOT_RX,NBIOT_TX);
  Serial485.begin(RS485_baudrate, SERIAL_8N1, RS485_RX, RS485_TX);
  sendATCommand("AT");
  sendATCommand("ATZ");
  sendATCommand("AT+CPIN?");
  sendATCommand("AT+CCID");
  sendATCommand("AT+COPS?");
  sendATCommand("AT+CEREG?");
  
  //Attach network
  sendATCommand("AT+CBAND=3");
  //sendATCommand("AT+CGDCONT=1,\"IP\",\"nbiot\"");
  sendATCommand("AT+COPS=0");
  sendATCommand("AT+CGCONTRDP");
}

void NBIOT_CheckConnection(){
  sendATCommand("AT+CGREG=0");
  sendATCommand("AT+COPS?");
  sendATCommand("AT+CSQ");
  sendATCommand("AT+CENG?");
  //sendATCommand("AT+CMQDISCON=0");
  sendATCommand("ATE0");
}

void  NBIOT_ConnectMQTT(){
  sendATCommand("AT+CMQTSYNC=1");
  sendATCommand("AT+CMQNEW=\"mqttserver.tk\",\"1883\",12000,1024");\
  sendATCommand("AT+CMQCON=0,3,\"WaterStation\",600,1,0,\"innovation\",\"Innovation_RgPQAZoA5N\"");
}

void NBIOT_SubTopic(const String& topic){
  String SubString = "AT+CMQSUB=0,\"" + topic + "\",1";
  sendATCommand(SubString.c_str());
}

void NBIOT_publishData(const String& topic,const String& str){
  getResponse = false;
  String newStr = "";
  for (char c : str) {
    newStr += (c == '"') ? '\'' : c;
  }
  //Create MQTT string
  String mqttString = "AT+CMQPUB=0,\"" + topic + "\",1,1,0," + String(newStr.length()) + ",\"" + newStr + "\"";
 
  sendATCommand(mqttString.c_str());
}

void NBIOT_clearBuffer(void){
  String receivedData = "";
  while (SerialNBIOT.available()) {
      char c = SerialNBIOT.read();
      receivedData += c;
  }
  if(!receivedData.isEmpty()) SerialMon.println(receivedData);

}
