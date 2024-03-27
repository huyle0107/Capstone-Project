#include <M5Atom.h>
#include "sensor_data.h"
#include "Timer_Interrupt.h"
#include "Config.h"
#include "SoilAirMachine.h"
#include "NBIOT.h"


hw_timer_t* timer = NULL; //khơi tạo timer
portMUX_TYPE timerMux = portMUX_INITIALIZER_UNLOCKED;
// hàm xử lý ngắt
void IRAM_ATTR onTimer() {   
  portENTER_CRITICAL_ISR(&timerMux); //vào chế độ tránh xung đột
  timerRun();
  portEXIT_CRITICAL_ISR(&timerMux); // thoát 
}


void setup() {
  M5.begin(true, false, true);
  delay(50);
  M5.dis.fillpix(0x00ff00);

  SerialMon.begin(Monitor_baudrate, SERIAL_8N1, Monitor_RX, Monitor_TX);
  SerialNBIOT.begin(NBIOT_baudrate, SERIAL_8N1, NBIOT_RX,NBIOT_TX);
  Serial485.begin(RS485_baudrate, SERIAL_8N1, RS485_RX, RS485_TX);
  delay(1000);

  
  timer = timerBegin(0, 80, true);
  //khởi tạo hàm xử lý ngắt ngắt cho Timer
  timerAttachInterrupt(timer, &onTimer, true);
  //khởi tạo thời gian ngắt cho timer là 1ms (1000 us)
  timerAlarmWrite(timer, 1000, true);
  //bắt đầu chạy timer  
  timerAlarmEnable(timer);


  NBIOT_Init();
  NBIOT_CheckConnection();
  NBIOT_ConnectMQTT();
  NBIOT_SubTopic(AirStation);
  //sendATCommand("AT+CMQPUB=0,\"/innovation/airmonitoring/WSNs\",1,1,0,39,\"{'temperature': 25.5, 'humidity': 60.2}\"");
 }

void loop(){
  SoilAirStateMachine();
}
// void loop() {
//  
  // while (!SerialNBIOT.available()) {}
  // String receivedData = "";
  // while (SerialNBIOT.available()) {
  //   char c = SerialNBIOT.read();
  //   receivedData += c;
  // }
  // if(receivedData.indexOf("+CMQPUB: 0,\"/innovation/airmonitoring/WSNs\"") != -1)  SerialMon.println("Get data");
  // SerialMon.println(receivedData);
//}

  // Serial.println("Turn On relay");
  // Serial2.write(data485.relay_turnON(), 8);
  // delay(1000);

  // if (Serial2.available()) {    
  //   uint8_t receivedData[8];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <8 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  // }
  // delay(5000);

  // Serial.println("Writing to AirStation - TEMP with data...");
  // Serial2.write(data485.getDataAIR_TEMP(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("AIR TEMP =");
  //   air_TEMP = int16_t((receivedData[3] << 8 | receivedData[4])) / 10;
  //   Serial.println(data.floatToString(air_TEMP));
  // }


  // Serial.println("Writing to AirStation - HUMID with data...");
  // Serial2.write(data485.getDataAIR_HUMID(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("AIR HUMID =");
  //   air_HUMID = int16_t((receivedData[3] << 8 | receivedData[4])) / 10;
  //   Serial.println(data.floatToString(air_HUMID));
  // }


  // Serial.println("Writing to AirStation - CO with data...");
  // Serial2.write(data485.getDataAIR_CO(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("AIR CO =");
  //   air_CO = int16_t((receivedData[3] << 8 | receivedData[4]));
  //   Serial.println(data.floatToString(air_CO));
  // }
  

  // Serial.println("Writing to AirStation - CO2 with data...");
  // Serial2.write(data485.getDataAIR_CO2(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("AIR CO2 =");
  //   air_CO2 = int16_t((receivedData[3] << 8 | receivedData[4]));
  //   Serial.println(data.floatToString(air_CO2));
  // }

  
  // Serial.println("Writing to AirStation - SO2 with data...");
  // Serial2.write(data485.getDataAIR_SO2(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("AIR SO2 =");
  //   air_SO2 = int16_t((receivedData[3] << 8 | receivedData[4]));
  //   Serial.println(data.floatToString(air_SO2));
  // }  


  // Serial.println("Writing to AirStation - NO2 with data...");
  // Serial2.write(data485.getDataAIR_NO2(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("AIR NO2 =");
  //   air_NO2 = int16_t((receivedData[3] << 8 | receivedData[4]));
  //   Serial.println(data.floatToString(air_NO2));
  // }

  // Serial.println("Writing to AirStation - O3 with data...");
  // Serial2.write(data485.getDataAIR_O3(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("AIR O3 =");
  //   air_O3 = int16_t((receivedData[3] << 8 | receivedData[4]));
  //   Serial.println(data.floatToString(air_O3));
  // }


  // Serial.println("Writing to AirStation - PM10 with data...");
  // Serial2.write(data485.getDataAIR_PM10(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("AIR PM10 =");
  //   air_PM10 = int16_t((receivedData[3] << 8 | receivedData[4]));
  //   Serial.println(data.floatToString(air_PM10));
  // }



  // Serial.println("Writing to AirStation - PM25 with data...");
  // Serial2.write(data485.getDataAIR_PM25(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("AIR PM25 =");
  //   air_PM25 = int16_t((receivedData[3] << 8 | receivedData[4]));
  //   Serial.println(data.floatToString(air_PM25)); 
  // }
  // // String Publish_data;
  // // Serial1.println("Writing to AirStation - TEMP and HUMID with data...");
  // // Serial2.write(data485.getDataAIR_HUMID_TEMP(), 8);
  // // delay(1000);
  // // if (Serial2.available()) {    // If the serial port receives a message.
  // //   uint8_t receivedData[9];
  // //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  // //   for (int i = 0; i <9 ; i++) {
  // //     Serial1.print("0x");
  // //     Serial1.print(receivedData[i], HEX);
  // //     Serial1.print(", ");
  // //   }
  // //   Serial1.println();
  // //   Serial1.print("AIR TEMP =");
  // //   air_TEMP = int16_t((receivedData[5] << 8 | receivedData[6])) / 10;
  // //   Serial1.println(data.floatToString(air_TEMP));
    
  // //   Serial1.print("AIR HUMIDITY =");
  // //   air_HUMID = int16_t((receivedData[3] << 8 | receivedData[4])) / 10;
  // //   Serial1.println(data.floatToString(air_HUMID));
  // // }
  // // delay(2000);

  // Serial.println("Writing to AirStation - NOISE with data...");
  // Serial2.write(data485.getDataAIR_NOISE(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("AIR NOISE =");
  //   air_NOISE = int16_t((receivedData[3] << 8 | receivedData[4])) / 10;
  //   Serial.println(data.floatToString(air_NOISE));
  // }
  // // Serial1.println("Writing to AirStation - PM2.5 and PM10 with data...");
  // // Serial2.write(data485.getDataAIR_PM25_PM10(), 8);
  // // delay(1000);
  // // if (Serial2.available()) {    // If the serial port receives a message.
  // //   uint8_t receivedData[9];
  // //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  // //   for (int i = 0; i <9 ; i++) {
  // //     Serial1.print("0x");
  // //     Serial1.print(receivedData[i], HEX);
  // //     Serial1.print(", ");
  // //   }
  // //   Serial1.println();
  // //   Serial1.print("AIR PM10 =");
  // //   air_PM10 = int16_t((receivedData[5] << 8 | receivedData[6]));
  // //   Serial1.println(data.floatToString(air_PM10));
    
  // //   Serial1.print("AIR PM2.5 =");
  // //   air_PM25 = int16_t((receivedData[3] << 8 | receivedData[4]));
  // //   Serial1.println(data.floatToString(air_PM25));
  // // }
  // // delay(2000);
  
  // Serial.println("Writing to AirStation - ATMOSPHERE with data...");
  // Serial2.write(data485.getDataAIR_ATMOSPHERE(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("AIR ATMOSPHERE =");
  //   air_ATMOSPHERE = int16_t((receivedData[3] << 8 | receivedData[4])) / 10;
  //   Serial.println(data.floatToString(air_ATMOSPHERE));
  // }

 
  // Serial.println("Writing to AirStation - LUX with data...");
  // Serial2.write(data485.getDataAIR_LUX(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[9];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <9 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("LUX =");
  //   air_LUX = int32_t(receivedData[3] << 24 | receivedData[4] << 16| receivedData[5] << 8 | receivedData[6]);
  //   Serial.println(data.floatToString(air_LUX));
  // }
  // // String publishData = data.createAirStationJSON(air_TEMP,air_HUMID,air_LUX,air_ATMOSPHERE,air_NOISE,air_PM10,air_PM25,air_CO,air_CO2,air_SO2,air_NO2,air_O3);
  // // Serial.println(publishData);
  // // NBIOT_publishData(AirStation,publishData);
 
  // //Sensors for Soil
  // Serial.println("Writing to SoilStation - PH with data...");
  // Serial2.write(data485.getDataSOIL_PH(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("SOIL PH =");
  //   soil_PH = int16_t((receivedData[3] << 8 | receivedData[4])) / 100;
  //   Serial.println(data.floatToString(soil_PH));
  // }


  // Serial.println("Writing to SoilStation - TEMP and HUMID with data...");
  // Serial2.write(data485.getDataSOIL_HUMID_TEMP(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[9];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <9 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("SOIL TEMP =");
  //   soil_TEMP = int16_t((receivedData[5] << 8 | receivedData[6])) / 10;
  //   Serial.println(data.floatToString(soil_TEMP));
    
  //   Serial.print("SOIL HUMIDITY =");
  //   soil_HUMID = int16_t((receivedData[3] << 8 | receivedData[4])) / 10;
  //   Serial.println(data.floatToString(soil_HUMID));
  // }


  // Serial.println("Writing to SoilStation - NPK with data...");
  // Serial2.write(data485.getDataSOIL_NPK(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[11];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <11 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("Soil_N =");
  //   soil_N = int16_t((receivedData[3] << 8 | receivedData[4]));
  //   Serial.println(data.floatToString(soil_N));

  //   Serial.print("Soil_P =");
  //   soil_P = int16_t((receivedData[5] << 8 | receivedData[6]));
  //   Serial.println(data.floatToString(soil_P));

  //   Serial.print("Soil_K =");
  //   soil_K = int16_t((receivedData[7] << 8 | receivedData[8]));
  //   Serial.println(data.floatToString(soil_K));
  // }


  // Serial.println("Writing to SoilStation - EC with data...");
  // Serial2.write(data485.getDataSOIL_EC(), 8);
  // delay(1000);
  // if (Serial2.available()) {    // If the serial port receives a message.
  //   uint8_t receivedData[7];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <7 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  //   Serial.print("Soil_EC =");
  //   soil_EC = int16_t((receivedData[3] << 8 | receivedData[4]));
  //   Serial.println(data.floatToString(soil_EC));
  // }

  // // publishData = data.createSoilStationJSON(soil_TEMP, soil_HUMID, soil_PH, soil_EC, soil_N, soil_P, soil_K);
  // // Serial.println(publishData);
  // // NBIOT_publishData(SoilStation,publishData);
  
  // Serial.println("Turn Off relay");
  // Serial2.write(data485.relay_turnOFF(), 8);
  // delay(1000);
  // if (Serial2.available()) {    
  //   uint8_t receivedData[8];
  //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
  //   for (int i = 0; i <8 ; i++) {
  //     Serial.print("0x");
  //     Serial.print(receivedData[i], HEX);
  //     Serial.print(", ");
  //   }
  //   Serial.println();
  // }

  // String publishData = data.createAirSoilStationJSON(air_TEMP,air_HUMID,air_LUX,air_ATMOSPHERE,air_NOISE,air_PM10,air_PM25,air_CO,air_CO2,air_SO2,air_NO2,air_O3,soil_TEMP, soil_HUMID, soil_PH, soil_EC, soil_N, soil_P, soil_K);
  // Serial.println(publishData);
  // NBIOT_publishData(AirStation,publishData);
  // // delay(10000);
  // delay(576000);




