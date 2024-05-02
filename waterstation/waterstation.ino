#include <M5Atom.h>
#include "WiFi.h"
#include "sensor_data.h"
#include "StateMachine.h"
#include "Timer_Interrupt.h"
#include "espnow.h"


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
  M5.dis.fillpix(0x0000ff);
  SerialMon.begin(Monitor_baudrate, SERIAL_8N1, Monitor_RX, Monitor_TX);
  SerialNBIOT.begin(NBIOT_baudrate, SERIAL_8N1, NBIOT_RX,NBIOT_TX);
  Serial485.begin(RS485_baudrate, SERIAL_8N1, RS485_RX, RS485_TX);
  
  // WiFi.mode(WIFI_STA);
  // delay(3000); //delay for set-up M5
  // if (esp_now_init() != ESP_OK) {
  //    Serial1.println("ESPNow initialization failed!");
  //    delay(100);
  //  }
  //  else {
  //    Serial1.println("ESPNow initialization completed!");
  //    delay(100);
  //  }
  //  esp_now_register_send_cb(OnDataSent);
  //  esp_now_register_recv_cb(OnDataRecv);

  //  memcpy(GateWayInfo.peer_addr, GateWayMacAddress, 6);
  //  GateWayInfo.channel = 0;
  //  GateWayInfo.encrypt = false; // No encryption
  //  if(esp_now_add_peer(&GateWayInfo) != ESP_OK){
  //    M5.dis.fillpix(0xff0000);
  //    Serial1.println("Failed to add GateWay!");
  //    delay(10);
  //  } else {
  //    M5.dis.fillpix(0x00ff00);
  //    Serial1.println("Completed to add GateWay!");
  //    delay(10);
  //  }

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
}

void loop() {
  WaterStateMachine();
}
