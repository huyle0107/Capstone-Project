#include"StateMachine.h"

// ClassJson Data
SENSOR_DATA data;
// Class Data for read value
SENSOR_RS485 data485;
String publishData; 

State state =  INIT;
State pre_state = state;

float Water_EC = 0, Water_PH = 0, Water_ORP = 0, Water_TEMP = 0, Water_SALINITY = 0;
void WaterStateMachine(){
  switch(state){
    case INIT:
              SerialMon.begin(Monitor_baudrate, SERIAL_8N1, Monitor_RX, Monitor_TX);
              SerialNBIOT.begin(NBIOT_baudrate, SERIAL_8N1, NBIOT_RX,NBIOT_TX);
              Serial485.begin(RS485_baudrate, SERIAL_8N1, RS485_RX, RS485_TX);
              setTimer1(timeRead);
              state = ReadEC;    
              break;

    case ReadEC:
              Serial1.println("Writing to WaterStation - EC with data...");
              Serial2.write(data485.getDataWATER_EC(), 8);
              pre_state = state;
              state = WaitSensor;
              setTimer(timeWaitSensor);
              break;

    case ReadSALINITY:
              Serial1.println("Writing to WaterStation - SALINITY with data...");
              Serial2.write(data485.getDataWATER_SALINITY(), 8);
              pre_state = state;
              state = WaitSensor;
              setTimer(timeWaitSensor);
              break;
   
    case ReadORP:
              Serial1.println("Writing to WaterStation - ORP with data...");
              Serial2.write(data485.getDataWATER_ORP(), 8);
              pre_state = state;
              state = WaitSensor;
              setTimer(timeWaitSensor);
              break;    
    
    case ReadPH:
              Serial1.println("Writing to WaterStation - PH with data...");
              Serial2.write(data485.getDataWATER_PH(), 8);
              pre_state = state;
              state = WaitSensor;
              setTimer(timeWaitSensor);
              break;
    
    case ReadTEMP:
              Serial1.println("Writing to WaterStation - TEMP with data...");
              Serial2.write(data485.getDataWATER_TEMP(), 8);
              pre_state = state;
              state = WaitSensor;
              setTimer(timeWaitSensor);
              break;
    
    case WaitSensor:
              if(timer_flag == 1){
                state = pre_state;
              }
              if (Serial2.available()) {    // If the serial port receives a message.
                 uint8_t receivedData[9];
                 Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                 for (int i = 0; i <9 ; i++) {
                   Serial1.print("0x");
                   Serial1.print(receivedData[i], HEX);
                   Serial1.print(", ");
                 }
                 Serial1.println();
                 if(pre_state == ReadEC){
                    Serial1.print("EC =");
                    Water_EC = decode_32bit(receivedData);
                    Serial1.println(data.floatToString(Water_EC));
                    state = ReadSALINITY;
                 }
                 if(pre_state == ReadSALINITY){
                    Serial1.print("SALINITY =");
                    Water_SALINITY = decode_32bit(receivedData);
                    Serial1.println(data.floatToString(Water_SALINITY));
                    state = ReadORP;
                 }
                 if(pre_state == ReadORP){
                    Serial1.print("ORP =");
                    Water_ORP = decode_32bit(receivedData);
                    Serial1.println(data.floatToString(Water_ORP));
                    state = ReadPH;
                 }                 
                 if(pre_state == ReadPH){
                    Serial1.print("PH =");
                    Water_PH = decode_32bit(receivedData);
                    Serial1.println(data.floatToString(Water_PH));
                    state = ReadTEMP;
                 }
                 if(pre_state == ReadTEMP){
                    Serial1.print("TEMP =");
                    Water_TEMP = decode_32bit(receivedData);
                    Serial1.println(data.floatToString(Water_TEMP));
                    state = WAIT_SEND;
                 }   
              }                           
              break; 

    case WAIT_SEND:
              if(timer1_flag){
                   state = NBIOT_RECONNECTION; 
              }
              break;

    case NBIOT_RECONNECTION:
              NBIOT_CheckConnection();
              NBIOT_ConnectMQTT();
              setTimer(timeClearBuffer);
              state = CLEAR_BUFFER_PRE;
              break;

    case  CLEAR_BUFFER_PRE:
              NBIOT_clearBuffer();
              if(timer_flag){
                state = NBIOT_SEND;
              }
              break;

    case  CLEAR_BUFFER_POST:
              NBIOT_clearBuffer();
              if(timer_flag){
                SerialMon.println("SYSTEM OFF");
                setTimer(timeSleep);
                state = SYSTEMOFF;
              }
              break; 

    case NBIOT_SEND:
              isListen = true;
              publishData = data.createWaterStationJSON(Water_EC, Water_PH, Water_ORP, Water_TEMP, Water_SALINITY);
              SerialMon.println(publishData);
              NBIOT_publishData(WaterStation,publishData);
              state = WAIT_RESPONSE;
              setTimer(timeWaitResponse);
              //setTimer1(timeExecuteResponse);
              // state = SYSTEMOFF;
              // setTimer(timeSleep);             
              break;

    case WAIT_RESPONSE:
              if(getResponse == true){
                isListen = false;
                SerialMon.println("Receive callback");
                setTimer(timeClearBuffer);
                state = CLEAR_BUFFER_POST;
              }
              if(timer_flag){
                 resetModule();
              }
              break;

    case SYSTEMOFF:
              if(timer_flag == 1){
                state = ReadEC;
                setTimer1(timeRead);
              }
              break;

    default:
            break;
  }
}
