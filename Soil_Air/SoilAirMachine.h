#include"Timer_Interrupt.h"
#include "sensor_data.h"
#include <string>
#include "Config.h"
#include "NBIOT.h"

enum State {
    INIT = 0,
    RELAYON = 1,
    RELAYOFF = 2,
    WAIT_RELAY = 3,

    READ_AIR_TEMP_HUMID = 4,
    READ_AIR_NOISE = 5,
    READ_AIR_PM25_PM10 = 6,
    READ_AIR_ATMOSPHERE = 7,
    READ_AIR_ILLUMINANCE = 8,
    READ_AIR_CO = 9,
    READ_AIR_CO2 = 10,
    READ_AIR_SO2 = 11,
    READ_AIR_NO2 = 12,
    READ_AIR_O3 = 13,

    READ_SOIL_TEMP_HUMID = 14,
    READ_SOIL_EC = 15,
    READ_SOIL_PH = 16,
    READ_SOIL_NPK = 17,
    
    WAIT_SENSOR = 18,
    WAIT_SEND = 19,
    NBIOT_SEND = 20,
    WAIT_RESPONSE = 21,
    SYSTEMOFF = 22
};


extern State pre_state;
extern State state;
extern String publishData;


// Class Data for read value
extern SENSOR_RS485 air_data485;
void SoilAirStateMachine();
