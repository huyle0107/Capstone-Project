#include"SoilAirMachine.h"


// ClassJson Data
SENSOR_DATA data;
// Class Data for read value
SENSOR_RS485 data485;
String publishData; 

State state =  INIT;
State pre_state = state;

float Voltage = 0, Voltage1 = 0, Current = 0, Power = 0;
float air_TEMP = 0,air_HUMID = 0, air_NOISE = 0, air_PM25 = 0, air_PM10 = 0, air_ATMOSPHERE = 0, air_LUX = 0, air_CO = 0, air_CO2 = 0, air_SO2 = 0, air_NO2 = 0, air_O3 = 0;
float soil_PH = 0, soil_TEMP = 0, soil_HUMID = 0, soil_N = 0, soil_P = 0, soil_K= 0, soil_EC = 0;

void SoilAirStateMachine(){
  switch(state){
    case INIT:
              SerialMon.begin(Monitor_baudrate, SERIAL_8N1, Monitor_RX, Monitor_TX);
              SerialNBIOT.begin(NBIOT_baudrate, SERIAL_8N1, NBIOT_RX,NBIOT_TX);
              Serial485.begin(RS485_baudrate, SERIAL_8N1, RS485_RX, RS485_TX);
              setTimer1(timeRead);
              state = RELAYON;
              break;
    case RELAYON:
              SerialMon.println("Turn On relay");
              Serial485.write(data485.relay_turnON(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);
              break;

    case WAIT_SENSOR:
              if(timer_flag == 1){
                state = pre_state;
              }
              if (Serial485.available()) {
                // RS485 response turn on relay
                if(pre_state == RELAYON){
                  uint8_t receivedData[8];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <8 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  state = WAIT_RELAY;
                  setTimer(5000);
                }

                //RS485 response turn off relay
                if(pre_state == RELAYOFF){
                  uint8_t receivedData[8];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <8 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  state = WAIT_SEND;
                }

                //RS485 response read VOLTAGE
                if(pre_state == READ_VOLTAGE){
                  uint8_t receivedData[9];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i < 9 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("VOLTAGE LOAD =");
                  Voltage = int16_t((receivedData[3] << 8 | receivedData[4])) / 100.0;
                  SerialMon.println(data.floatToString(Voltage));

                  SerialMon.print("VOLTAGE BATTERY =");
                  Voltage1 = int16_t((receivedData[5] << 8 | receivedData[6])) / 100.0;
                  SerialMon.println(data.floatToString(Voltage1));
                  state = READ_CURRENT;
                }   

                //RS485 response read VOLTAGE
                if(pre_state == READ_CURRENT){
                  uint8_t receivedData[9];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i < 9 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("CURRENT =");
                  float Current = int16_t((receivedData[3] << 8 | receivedData[4]) + 150) / 1000.0;
                  //Current = (temp - 44 - (temp / 10.0)) / 1000.0;
                  SerialMon.println(data.floatToString(Current));
                  
                  Power = Voltage * Current;
                  SerialMon.print("POWER =");
                  SerialMon.println(data.floatToString(Power));

                  state = READ_AIR_TEMP_HUMID;
                }               
                  
                //RS485 response read AIR_TEMP_HUMID
                if(pre_state == READ_AIR_TEMP_HUMID){
                  uint8_t receivedData[9];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <9 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("AIR TEMP =");
                  air_TEMP = int16_t((receivedData[5] << 8 | receivedData[6])) / 10.0;
                  SerialMon.println(data.floatToString(air_TEMP));
                  
                  SerialMon.print("AIR HUMIDITY =");
                  air_HUMID = int16_t((receivedData[3] << 8 | receivedData[4])) / 10.0;
                  SerialMon.println(data.floatToString(air_HUMID));
                  state = READ_AIR_NOISE;
                }


                //RS485 response read AIR_NOISE
                if(pre_state == READ_AIR_NOISE){
                  uint8_t receivedData[7];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <7 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("AIR NOISE =");
                  air_NOISE = int16_t((receivedData[3] << 8 | receivedData[4])) / 10.0;
                  SerialMon.println(data.floatToString(air_NOISE));
                  state = READ_AIR_PM25_PM10;
                }

                //RS485 response read AIR_PM25_PM10
                if(pre_state == READ_AIR_PM25_PM10){
                  uint8_t receivedData[9];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <9 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("AIR PM10 =");
                  air_PM10 = int16_t((receivedData[5] << 8 | receivedData[6]));
                  SerialMon.println(data.floatToString(air_PM10));
                  
                  SerialMon.print("AIR PM2.5 =");
                  air_PM25 = int16_t((receivedData[3] << 8 | receivedData[4]));
                  SerialMon.println(data.floatToString(air_PM25));
                  state = READ_AIR_ATMOSPHERE;
                }

                //RS485 response read AIR_ATMOSPHERE
                if(pre_state == READ_AIR_ATMOSPHERE){
                  uint8_t receivedData[7];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <7 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("AIR ATMOSPHERE =");
                  air_ATMOSPHERE = int16_t((receivedData[3] << 8 | receivedData[4])) / 10.0;
                  SerialMon.println(data.floatToString(air_ATMOSPHERE));
                  state = READ_AIR_ILLUMINANCE;
                }

                
                //RS485 response read AIR_ATMOSPHERE
                if(pre_state == READ_AIR_ILLUMINANCE){
                  uint8_t receivedData[9];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <9 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("LUX =");
                  air_LUX = int32_t(receivedData[3] << 24 | receivedData[4] << 16| receivedData[5] << 8 | receivedData[6]);
                  SerialMon.println(data.floatToString(air_LUX));
                  state = READ_AIR_CO;
                }

                //RS485 response read AIR_CO
                if(pre_state == READ_AIR_CO){
                  uint8_t receivedData[7];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <7 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("AIR CO =");
                  air_CO = int16_t((receivedData[3] << 8 | receivedData[4]));
                  SerialMon.println(data.floatToString(air_CO));
                  state = READ_AIR_CO2;
                }

                //RS485 response read AIR_CO2
                if(pre_state == READ_AIR_CO2){
                  uint8_t receivedData[7];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <7 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("AIR CO2 =");
                  air_CO2 = int16_t((receivedData[3] << 8 | receivedData[4]));
                  SerialMon.println(data.floatToString(air_CO2));
                  state = READ_AIR_SO2;
                }

                //RS485 response read AIR_SO2
                if(pre_state == READ_AIR_SO2){
                  uint8_t receivedData[7];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <7 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("AIR SO2 =");
                  air_SO2 = int16_t((receivedData[3] << 8 | receivedData[4]));
                  SerialMon.println(data.floatToString(air_SO2));
                  state = READ_AIR_NO2;
                }          
               
               //RS485 response read AIR_NO2
                if(pre_state == READ_AIR_NO2){
                  uint8_t receivedData[7];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <7 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("AIR NO2 =");
                  air_NO2 = int16_t((receivedData[3] << 8 | receivedData[4]));
                  SerialMon.println(data.floatToString(air_NO2));
                  state = READ_AIR_O3;
                }

               //RS485 response read AIR_O3
                if(pre_state == READ_AIR_O3){
                  uint8_t receivedData[7];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <7 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("AIR O3 =");
                  air_O3 = int16_t((receivedData[3] << 8 | receivedData[4]));
                  SerialMon.println(data.floatToString(air_O3));
                  state = READ_SOIL_TEMP_HUMID;
                }   

               //RS485 response read SOIL_TEMP_HUMID
                if(pre_state == READ_SOIL_TEMP_HUMID){
                  uint8_t receivedData[9];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <9 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("SOIL TEMP =");
                  soil_TEMP = int16_t((receivedData[5] << 8 | receivedData[6])) / 10.0;
                  SerialMon.println(data.floatToString(soil_TEMP));
                  
                  SerialMon.print("SOIL HUMIDITY =");
                  soil_HUMID = int16_t((receivedData[3] << 8 | receivedData[4])) / 10.0;
                  SerialMon.println(data.floatToString(soil_HUMID));
                  state = READ_SOIL_EC;
                }        

               //RS485 response read SOIL_EC
                if(pre_state == READ_SOIL_EC){
                  uint8_t receivedData[7];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <7 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("Soil_EC =");
                  soil_EC = int16_t((receivedData[3] << 8 | receivedData[4]));
                  SerialMon.println(data.floatToString(soil_EC));
                  state = READ_SOIL_PH;
                }

               //RS485 response read SOIL_PH
                if(pre_state == READ_SOIL_PH){
                  uint8_t receivedData[7];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <7 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("SOIL PH =");
                  soil_PH = int16_t((receivedData[3] << 8 | receivedData[4])) / 100.0;
                  SerialMon.println(data.floatToString(soil_PH));
                  state = READ_SOIL_NPK;
                }  

               //RS485 response read SOIL_NPK
                if(pre_state == READ_SOIL_NPK){
                  uint8_t receivedData[11];
                  Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
                  for (int i = 0; i <11 ; i++) {
                    SerialMon.print("0x");
                    SerialMon.print(receivedData[i], HEX);
                    SerialMon.print(", ");
                  }
                  SerialMon.println();
                  SerialMon.print("Soil_N =");
                  soil_N = int16_t((receivedData[3] << 8 | receivedData[4]));
                  SerialMon.println(data.floatToString(soil_N));

                  SerialMon.print("Soil_P =");
                  soil_P = int16_t((receivedData[5] << 8 | receivedData[6]));
                  SerialMon.println(data.floatToString(soil_P));

                  SerialMon.print("Soil_K =");
                  soil_K = int16_t((receivedData[7] << 8 | receivedData[8]));
                  SerialMon.println(data.floatToString(soil_K));
                  state = RELAYOFF;
                }              
              }
              break;

    case WAIT_RELAY:
              if(timer_flag == 1){
                state = READ_VOLTAGE;
              }
              break;

    case READ_VOLTAGE:
              SerialMon.println("Writing to AirSoilStation - VOLTAGE with data...");
              Serial485.write(data485.read_Vol(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);        
              break;   

    case READ_CURRENT:
              SerialMon.println("Writing to AirSoilStation - CURRENT with data...");
              Serial485.write(data485.read_Cur(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);        
              break; 

    case READ_AIR_TEMP_HUMID:
              SerialMon.println("Writing to AirStation - TEMP and HUMID with data...");
              Serial485.write(data485.getDataAIR_HUMID_TEMP(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);        
              break;    

    case READ_AIR_NOISE:
              SerialMon.println("Writing to AirStation - NOISE with data...");
              Serial485.write(data485.getDataAIR_NOISE(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);        
              break;    
    
    case READ_AIR_PM25_PM10:
              SerialMon.println("Writing to AirStation - PM2.5 and PM10 with data...");
              Serial485.write(data485.getDataAIR_PM25_PM10(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;

    case READ_AIR_ATMOSPHERE:
              SerialMon.println("Writing to AirStation - ATMOSPHERE with data...");
              Serial485.write(data485.getDataAIR_ATMOSPHERE(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;
    
    case READ_AIR_ILLUMINANCE:
              SerialMon.println("Writing to AirStation - LUX with data...");
              Serial485.write(data485.getDataAIR_LUX(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;
    
    case READ_AIR_CO:
              SerialMon.println("Writing to AirStation - CO with data...");
              Serial485.write(data485.getDataAIR_CO(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;

    case READ_AIR_CO2:
              SerialMon.println("Writing to AirStation - CO2 with data...");
              Serial485.write(data485.getDataAIR_CO2(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;
    
    case READ_AIR_SO2:
              SerialMon.println("Writing to AirStation - SO2 with data...");
              Serial485.write(data485.getDataAIR_SO2(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;
    
    case READ_AIR_NO2:
              SerialMon.println("Writing to AirStation - NO2 with data...");
              Serial485.write(data485.getDataAIR_NO2(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;    

    case READ_AIR_O3:
              SerialMon.println("Writing to AirStation - O3 with data...");
              Serial485.write(data485.getDataAIR_O3(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;

    case READ_SOIL_TEMP_HUMID:
              SerialMon.println("Writing to SoilStation - TEMP and HUMID with data...");
              Serial485.write(data485.getDataSOIL_HUMID_TEMP(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;
    
    case READ_SOIL_EC:
              SerialMon.println("Writing to SoilStation - EC with data...");
              Serial485.write(data485.getDataSOIL_EC(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;

    case READ_SOIL_PH:
              SerialMon.println("Writing to SoilStation - PH with data...");
              Serial485.write(data485.getDataSOIL_PH(), 8); 
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;
    
    case READ_SOIL_NPK:
              SerialMon.println("Writing to SoilStation - NPK with data...");
              Serial485.write(data485.getDataSOIL_NPK(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor);   
              break;             

    case RELAYOFF:
              SerialMon.println("Turn Off relay");
              Serial485.write(data485.relay_turnOFF(), 8);
              pre_state = state;
              state = WAIT_SENSOR;
              setTimer(timeWaitSensor); 
              break;

    case WAIT_SEND:
              if(timer1_flag){
                   state = NBIOT_SEND; 
              }
              break;

    case NBIOT_SEND:
              publishData = data.createAirSoilStationJSON(Voltage, Voltage1, Power, air_TEMP,air_HUMID,air_LUX,air_ATMOSPHERE,air_NOISE,air_PM10,air_PM25,air_CO,air_CO2,air_SO2,air_NO2,air_O3,soil_TEMP, soil_HUMID, soil_PH, soil_EC, soil_N, soil_P, soil_K);
              SerialMon.println(publishData);
              NBIOT_publishData(AirStation,publishData);
              state = WAIT_RESPONSE;
              setTimer(timeWaitResponse);
              setTimer1(timeExecuteResponse);
              // state = SYSTEMOFF;
              // setTimer(timeSleep);             
              break;

    case WAIT_RESPONSE:
              if(getResponse == true){
                SerialMon.println("Receive callback");
                state = CLEAR_BUFFER;
              }
              NBIOT_ListenCallback();
              if(timer_flag){
                 resetModule();
              }
              break;

    case  CLEAR_BUFFER:
              NBIOT_clearBuffer();
              if(timer1_flag){
                state = SYSTEMOFF;
                setTimer(timeSleep);
              }
              break;

    case SYSTEMOFF:
              if(timer_flag){
                setTimer1(timeRead);
                // state = READ_VOLTAGE;
                state = RELAYON;
              }
              break;
    default:
            break;
  }
}
