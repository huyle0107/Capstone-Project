#include"Timer_Interrupt.h"
#include "sensor_data.h"
#include "espnow.h"
#include <string>
#include "Config.h"
#include "NBIOT.h"

enum State {
  INIT         = 0,
  ReadEC       = 1,
  ReadSALINITY = 2,
  ReadORP      = 3,
  ReadPH       = 4,
  ReadTEMP     = 5,
  WAIT_SEND = 6,
  WaitSensor   = 7,
  WAIT_RESPONSE = 8,
  SYSTEMOFF     = 9,

  NBIOT_RECONNECTION = 10,
  CLEAR_BUFFER_PRE = 11,
  CLEAR_BUFFER_POST = 12,
  NBIOT_SEND = 13
};

extern State pre_state;
extern State state;
extern String publishData;
// Class Data for read value
extern SENSOR_RS485 data485;
void WaterStateMachine();
