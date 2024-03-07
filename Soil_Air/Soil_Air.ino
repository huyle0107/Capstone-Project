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
  NBIOT_listenCallback();
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
}


void loop() {
  SoilAirStateMachine();
}



