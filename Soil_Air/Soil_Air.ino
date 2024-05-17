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
  //NBIOT_SubTopic(AirStation);
  //sendATCommand("AT+CMQPUB=0,\"/innovation/airmonitoring/WSNs\",1,1,0,39,\"{'temperature': 25.5, 'humidity': 60.2}\"");
 }

void loop(){
  SoilAirStateMachine();
  // sendATCommand("AT+CMQPUB=0,\"/innovation/soilmonitoring/WSNs\",1,1,0,39,\"{'temperature': 25.5, 'humidity': 60.2}\"");
  // delay(60000);
}

// void loop() {
//   SerialMon.println("Turn On relay");
//   Serial485.write(data485.relay_turnON(), 8);
//   delay(1000);

//   if (Serial485.available()) {    
//     uint8_t receivedData[8];
//     Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//     for (int i = 0; i <8 ; i++) {
//       SerialMon.print("0x");
//       SerialMon.print(receivedData[i], HEX);
//       SerialMon.print(", ");
//     }
//     SerialMon.println();
//   }
//   delay(5000);
  

  



//   // SerialMon.println("Writing to AirStation - TEMP with data...");
//   // Serial485.write(data485.getDataAIR_TEMP(), 8);
//   // delay(1000);
//   // if (Serial485.available()) {    // If the serial port receives a message.
//   //   uint8_t request[8] = data485.getDataAIR_TEMP();
//   //   SerialMon.print("Request: ");
//   //   for (int i = 0; i < 8; i++) {
//   //     SerialMon.print("0x");
//   //     if (request[i] < 0x10) {
//   //       Serial1.print("0");
//   //     }
//   //     SerialMon.print(request[i], HEX);
//   //     if (i < 8 - 1) {
//   //       SerialMon.print(", ");
//   //     }
//   //   }
//   //   SerialMon.println();
//   //   uint8_t receivedData[7];
//   //   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <7 ; i++) {
//   //     SerialMon.print("0x");
//   //     SerialMon.print(receivedData[i], HEX);
//   //     SerialMon.print(", ");
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("AIR TEMP =");
//   //   air_TEMP = int16_t((receivedData[3] << 8 | receivedData[4])) / 10;
//   //   SerialMon.println(data.floatToString(air_TEMP));
//   // }


//   // SerialMon.println("Writing to AirStation - HUMID with data...");
//   // Serial485.write(data485.getDataAIR_HUMID(), 8);
//   // delay(1000);
//   // if (Serial485.available()) {    // If the serial port receives a message.
//   //   uint8_t receivedData[7];
//   //   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <7 ; i++) {
//   //     SerialMon.print("0x");
//   //     SerialMon.print(receivedData[i], HEX);
//   //     SerialMon.print(", ");
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("AIR HUMID =");
//   //   air_HUMID = int16_t((receivedData[3] << 8 | receivedData[4])) / 10;
//   //   SerialMon.println(data.floatToString(air_HUMID));
//   // }


//   SerialMon.println("Writing to AirStation - TEMP/HUMID with data...");
//   Serial485.write(data485.getDataAIR_HUMID_TEMP(), 8);
//   if(Serial485.available())  {
//     uint8_t* request = data485.getDataAIR_HUMID_TEMP();
//     SerialMon.print("Request: ");
//     for (int i = 0; i < 8; i++) {
//       SerialMon.print("0x");
//       if (request[i] < 0x10) {
//         SerialMon.print("0");
//       }
//       SerialMon.print(request[i], HEX);
//       if (i < 8 - 1) {
//         SerialMon.print(", ");
//       }
//     }
//     SerialMon.println();
//     SerialMon.print("Response: ");
//     uint8_t receivedData[9];
//                   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//                   for (int i = 0; i <9 ; i++) {
//                     SerialMon.print("0x");
//                     SerialMon.print(receivedData[i], HEX);
//                     SerialMon.print(", ");
//                   }
//                   SerialMon.println();
//                   SerialMon.print("AIR TEMP =");
//                   air_TEMP = int16_t((receivedData[5] << 8 | receivedData[6])) / 10.0;
//                   SerialMon.println(data.floatToString(air_TEMP));
                  
//                   SerialMon.print("AIR HUMIDITY =");
//                   air_HUMID = int16_t((receivedData[3] << 8 | receivedData[4])) / 10.0;
//                   SerialMon.println(data.floatToString(air_HUMID));
//   }
//   delay(1000);

//   SerialMon.println("Writing to AirStation - PM2.5/PM10 with data...");
//   Serial485.write(data485.getDataAIR_PM25_PM10(), 8);
//   if(Serial485.available())  {
//     uint8_t* request = data485.getDataAIR_PM25_PM10();
//     SerialMon.print("Request: ");
//     for (int i = 0; i < 8; i++) {
//       SerialMon.print("0x");
//       if (request[i] < 0x10) {
//         Serial1.print("0");
//       }
//       SerialMon.print(request[i], HEX);
//       if (i < 8 - 1) {
//         SerialMon.print(", ");
//       }
//     }
//     SerialMon.println();
//     SerialMon.print("Response: ");
//     uint8_t receivedData[9];
//                   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//                   for (int i = 0; i <9 ; i++) {
//                     SerialMon.print("0x");
//                     SerialMon.print(receivedData[i], HEX);
//                     SerialMon.print(", ");
//                   }
//                   SerialMon.println();
//                   SerialMon.print("AIR PM10 =");
//                   air_PM10 = int16_t((receivedData[5] << 8 | receivedData[6]));
//                   SerialMon.println(data.floatToString(air_PM10));
                  
//                   SerialMon.print("AIR PM2.5 =");
//                   air_PM25 = int16_t((receivedData[3] << 8 | receivedData[4]));
//                   SerialMon.println(data.floatToString(air_PM25));
//   }
//   delay(1000);

//   // SerialMon.println("Writing to AirStation - CO with data...");
//   // Serial485.write(data485.getDataAIR_CO(), 8);
//   // delay(1000);
//   // if (Serial485.available()) {    // If the serial port receives a message.
//   //   uint8_t request[8] = data485.getDataAIR_CO();
//   //   SerialMon.print("Request: ");
//   //   for (int i = 0; i < 8; i++) {
//   //     SerialMon.print("0x");
//   //     if (request[i] < 0x10) {
//   //       Serial1.print("0");
//   //     }
//   //     SerialMon.print(request[i], HEX);
//   //     if (i < 8 - 1) {
//   //       SerialMon.print(", ");
//   //     }
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("Response: ");
//   //   uint8_t receivedData[7];
//   //   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <7 ; i++) {
//   //     SerialMon.print("0x");
//   //     SerialMon.print(receivedData[i], HEX);
//   //     SerialMon.print(", ");
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("AIR CO =");
//   //   air_CO = int16_t((receivedData[3] << 8 | receivedData[4]));
//   //   SerialMon.println(data.floatToString(air_CO));
//   // }
  

//   // SerialMon.println("Writing to AirStation - CO2 with data...");
//   // Serial485.write(data485.getDataAIR_CO2(), 8);
//   // delay(1000);
//   // if (Serial485.available()) {    // If the serial port receives a message.
//   //   uint8_t request[8] = data485.getDataAIR_CO2();
//   //   SerialMon.print("Request: ");
//   //   for (int i = 0; i < 8; i++) {
//   //     SerialMon.print("0x");
//   //     if (request[i] < 0x10) {
//   //       Serial1.print("0");
//   //     }
//   //     SerialMon.print(request[i], HEX);
//   //     if (i < 8 - 1) {
//   //       SerialMon.print(", ");
//   //     }
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("Response: ");
//   //   uint8_t receivedData[7];
//   //   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <7 ; i++) {
//   //     SerialMon.print("0x");
//   //     SerialMon.print(receivedData[i], HEX);
//   //     SerialMon.print(", ");
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("AIR CO2 =");
//   //   air_CO2 = int16_t((receivedData[3] << 8 | receivedData[4]));
//   //   SerialMon.println(data.floatToString(air_CO2));
//   // }

  
//   // SerialMon.println("Writing to AirStation - SO2 with data...");
//   // Serial485.write(data485.getDataAIR_SO2(), 8);
//   // delay(1000);
//   // if (Serial485.available()) {    // If the serial port receives a message.
//   //   uint8_t request[8] = data485.getDataAIR_SO2();
//   //   SerialMon.print("Request: ");
//   //   for (int i = 0; i < 8; i++) {
//   //     SerialMon.print("0x");
//   //     if (request[i] < 0x10) {
//   //       Serial1.print("0");
//   //     }
//   //     SerialMon.print(request[i], HEX);
//   //     if (i < 8 - 1) {
//   //       SerialMon.print(", ");
//   //     }
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("Response: ");
//   //   uint8_t receivedData[7];
//   //   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <7 ; i++) {
//   //     SerialMon.print("0x");
//   //     SerialMon.print(receivedData[i], HEX);
//   //     SerialMon.print(", ");
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("AIR SO2 =");
//   //   air_SO2 = int16_t((receivedData[3] << 8 | receivedData[4]));
//   //   SerialMon.println(data.floatToString(air_SO2));
//   // }  


//   // SerialMon.println("Writing to AirStation - NO2 with data...");
//   // Serial485.write(data485.getDataAIR_NO2(), 8);
//   // delay(1000);
//   // if (Serial485.available()) {    // If the serial port receives a message.
//   //   uint8_t request[8] = data485.getDataAIR_NO2();
//   //   SerialMon.print("Request: ");
//   //   for (int i = 0; i < 8; i++) {
//   //     SerialMon.print("0x");
//   //     if (request[i] < 0x10) {
//   //       Serial1.print("0");
//   //     }
//   //     SerialMon.print(request[i], HEX);
//   //     if (i < 8 - 1) {
//   //       SerialMon.print(", ");
//   //     }
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("Response: ");
//   //   uint8_t receivedData[7];
//   //   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <7 ; i++) {
//   //     SerialMon.print("0x");
//   //     SerialMon.print(receivedData[i], HEX);
//   //     SerialMon.print(", ");
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("AIR NO2 =");
//   //   air_NO2 = int16_t((receivedData[3] << 8 | receivedData[4]));
//   //   SerialMon.println(data.floatToString(air_NO2));
//   // }

//   // SerialMon.println("Writing to AirStation - O3 with data...");
//   // Serial485.write(data485.getDataAIR_O3(), 8);
//   // delay(1000);
//   // if (Serial485.available()) {    // If the serial port receives a message.
//   //   uint8_t request[8] = data485.getDataAIR_O3();
//   //   SerialMon.print("Request: ");
//   //   for (int i = 0; i < 8; i++) {
//   //     SerialMon.print("0x");
//   //     if (request[i] < 0x10) {
//   //       Serial1.print("0");
//   //     }
//   //     SerialMon.print(request[i], HEX);
//   //     if (i < 8 - 1) {
//   //       SerialMon.print(", ");
//   //     }
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("Response: ");
//   //   uint8_t receivedData[7];
//   //   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <7 ; i++) {
//   //     SerialMon.print("0x");
//   //     SerialMon.print(receivedData[i], HEX);
//   //     SerialMon.print(", ");
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("AIR O3 =");
//   //   air_O3 = int16_t((receivedData[3] << 8 | receivedData[4]));
//   //   SerialMon.println(data.floatToString(air_O3));
//   // }


//   SerialMon.println("Writing to AirStation - NOISE with data...");
//   Serial485.write(data485.getDataAIR_NOISE(), 8);
//   delay(1000);
//   if (Serial485.available()) {    // If the serial port receives a message.
//     uint8_t* request = data485.getDataAIR_NOISE();
//     SerialMon.print("Request: ");
//     for (int i = 0; i < 8; i++) {
//       SerialMon.print("0x");
//       if (request[i] < 0x10) {
//         SerialMon.print("0");
//       }
//       SerialMon.print(request[i], HEX);
//       if (i < 8 - 1) {
//         SerialMon.print(", ");
//       }
//     }
//     SerialMon.println();
//     SerialMon.print("Response: ");
//     uint8_t receivedData[7];
//                   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//                   for (int i = 0; i <7 ; i++) {
//                     SerialMon.print("0x");
//                     SerialMon.print(receivedData[i], HEX);
//                     SerialMon.print(", ");
//                   }
//                   SerialMon.println();
//                   SerialMon.print("AIR NOISE =");
//                   air_NOISE = int16_t((receivedData[3] << 8 | receivedData[4])) / 10.0;
//                   SerialMon.println(data.floatToString(air_NOISE));
//   }
//   // Serial1.println("Writing to AirStation - PM2.5 and PM10 with data...");
//   // Serial2.write(data485.getDataAIR_PM25_PM10(), 8);
//   // delay(1000);
//   // if (Serial2.available()) {    // If the serial port receives a message.
//   //   uint8_t receivedData[9];
//   //   Serial2.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <9 ; i++) {
//   //     Serial1.print("0x");
//   //     Serial1.print(receivedData[i], HEX);
//   //     Serial1.print(", ");
//   //   }
//   //   Serial1.println();
//   //   Serial1.print("AIR PM10 =");
//   //   air_PM10 = int16_t((receivedData[5] << 8 | receivedData[6]));
//   //   Serial1.println(data.floatToString(air_PM10));
    
//   //   Serial1.print("AIR PM2.5 =");
//   //   air_PM25 = int16_t((receivedData[3] << 8 | receivedData[4]));
//   //   Serial1.println(data.floatToString(air_PM25));
//   // }
//   // delay(2000);
  
//   SerialMon.println("Writing to AirStation - ATMOSPHERE with data...");
//   Serial485.write(data485.getDataAIR_ATMOSPHERE(), 8);
//   delay(1000);
//   if (Serial485.available()) {    // If the serial port receives a message.
//     uint8_t* request = data485.getDataAIR_ATMOSPHERE();
//     SerialMon.print("Request: ");
//     for (int i = 0; i < 8; i++) {
//       SerialMon.print("0x");
//       if (request[i] < 0x10) {
//         Serial1.print("0");
//       }
//       SerialMon.print(request[i], HEX);
//       if (i < 8 - 1) {
//         SerialMon.print(", ");
//       }
//     }
//     SerialMon.println();
//     SerialMon.print("Response: ");
//     uint8_t receivedData[7];
//                   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//                   for (int i = 0; i <7 ; i++) {
//                     SerialMon.print("0x");
//                     SerialMon.print(receivedData[i], HEX);
//                     SerialMon.print(", ");
//                   }
//                   SerialMon.println();
//                   SerialMon.print("AIR ATMOSPHERE =");
//                   air_ATMOSPHERE = int16_t((receivedData[3] << 8 | receivedData[4])) / 10.0;
//                   SerialMon.println(data.floatToString(air_ATMOSPHERE));
//   }

 
//   SerialMon.println("Writing to AirStation - LUX with data...");
//   Serial485.write(data485.getDataAIR_LUX(), 8);
//   delay(1000);
//   if (Serial485.available()) {    // If the serial port receives a message.
//    uint8_t* request = data485.getDataAIR_LUX();
//     SerialMon.print("Request: ");
//     for (int i = 0; i < 8; i++) {
//       SerialMon.print("0x");
//       if (request[i] < 0x10) {
//         SerialMon.print("0");
//       }
//       SerialMon.print(request[i], HEX);
//       if (i < 8 - 1) {
//         SerialMon.print(", ");
//       }
//     }
//     SerialMon.println();
//     SerialMon.print("Response: ");
//                   uint8_t receivedData[9];
//                   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//                   for (int i = 0; i <9 ; i++) {
//                     SerialMon.print("0x");
//                     SerialMon.print(receivedData[i], HEX);
//                     SerialMon.print(", ");
//                   }
//                   SerialMon.println();
//                   SerialMon.print("LUX =");
//                   air_LUX = int32_t(receivedData[3] << 24 | receivedData[4] << 16| receivedData[5] << 8 | receivedData[6]);
//                   SerialMon.println(data.floatToString(air_LUX));
//   }
//   // // String publishData = data.createAirStationJSON(air_TEMP,air_HUMID,air_LUX,air_ATMOSPHERE,air_NOISE,air_PM10,air_PM25,air_CO,air_CO2,air_SO2,air_NO2,air_O3);
//   // // Serial.println(publishData);
//   // // NBIOT_publishData(AirStation,publishData);
 
//   // //Sensors for Soil
//   // SerialMon.println("Writing to SoilStation - PH with data...");
//   // Serial485.write(data485.getDataSOIL_PH(), 8);
//   // delay(1000);
//   // if (Serial485.available()) {    // If the serial port receives a message.
//   //   uint8_t receivedData[7];
//   //   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <7 ; i++) {
//   //     SerialMon.print("0x");
//   //     SerialMon.print(receivedData[i], HEX);
//   //     SerialMon.print(", ");
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("SOIL PH =");
//   //   soil_PH = int16_t((receivedData[3] << 8 | receivedData[4])) / 100;
//   //   SerialMon.println(data.floatToString(soil_PH));
//   // }


//   // SerialMon.println("Writing to SoilStation - TEMP and HUMID with data...");
//   // Serial485.write(data485.getDataSOIL_HUMID_TEMP(), 8);
//   // delay(1000);
//   // if (Serial485.available()) {    // If the serial port receives a message.
//   //   uint8_t receivedData[9];
//   //   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <9 ; i++) {
//   //     SerialMon.print("0x");
//   //     SerialMon.print(receivedData[i], HEX);
//   //     SerialMon.print(", ");
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("SOIL TEMP =");
//   //   soil_TEMP = int16_t((receivedData[5] << 8 | receivedData[6])) / 10;
//   //   SerialMon.println(data.floatToString(soil_TEMP));
    
//   //   SerialMon.print("SOIL HUMIDITY =");
//   //   soil_HUMID = int16_t((receivedData[3] << 8 | receivedData[4])) / 10;
//   //   SerialMon.println(data.floatToString(soil_HUMID));
//   // }


//   // SerialMon.println("Writing to SoilStation - NPK with data...");
//   // Serial485.write(data485.getDataSOIL_NPK(), 8);
//   // delay(1000);
//   // if (Serial485.available()) {    // If the serial port receives a message.
//   //   uint8_t receivedData[11];
//   //   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <11 ; i++) {
//   //     SerialMon.print("0x");
//   //     SerialMon.print(receivedData[i], HEX);
//   //     SerialMon.print(", ");
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("Soil_N =");
//   //   soil_N = int16_t((receivedData[3] << 8 | receivedData[4]));
//   //   SerialMon.println(data.floatToString(soil_N));

//   //   SerialMon.print("Soil_P =");
//   //   soil_P = int16_t((receivedData[5] << 8 | receivedData[6]));
//   //   SerialMon.println(data.floatToString(soil_P));

//   //   SerialMon.print("Soil_K =");
//   //   soil_K = int16_t((receivedData[7] << 8 | receivedData[8]));
//   //   SerialMon.println(data.floatToString(soil_K));
//   // }


//   // SerialMon.println("Writing to SoilStation - EC with data...");
//   // Serial485.write(data485.getDataSOIL_EC(), 8);
//   // delay(1000);
//   // if (Serial485.available()) {    // If the serial port receives a message.
//   //   uint8_t receivedData[7];
//   //   Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//   //   for (int i = 0; i <7 ; i++) {
//   //     SerialMon.print("0x");
//   //     SerialMon.print(receivedData[i], HEX);
//   //     SerialMon.print(", ");
//   //   }
//   //   SerialMon.println();
//   //   SerialMon.print("Soil_EC =");
//   //   soil_EC = int16_t((receivedData[3] << 8 | receivedData[4]));
//   //   SerialMon.println(data.floatToString(soil_EC));
//   // }

//   // // publishData = data.createSoilStationJSON(soil_TEMP, soil_HUMID, soil_PH, soil_EC, soil_N, soil_P, soil_K);
//   // // Serial.println(publishData);
//   // // NBIOT_publishData(SoilStation,publishData);
  
//   SerialMon.println("Turn Off relay");
//   Serial485.write(data485.relay_turnOFF(), 8);
//   delay(1000);
//   if (Serial485.available()) {    
//     uint8_t receivedData[8];
//     Serial485.readBytes(receivedData, sizeof(receivedData));  // Read the message.
//     for (int i = 0; i <8 ; i++) {
//       SerialMon.print("0x");
//       SerialMon.print(receivedData[i], HEX);
//       SerialMon.print(", ");
//     }
//     SerialMon.println();
//   }
//    delay(1200000);
//   }


