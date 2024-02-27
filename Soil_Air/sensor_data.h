#ifndef INC_SENSOR_DATA_H_
#define INC_SENSOR_DATA_H_

#include <ArduinoJson.h>

class SENSOR_DATA{
  public:
    SENSOR_DATA(){};
    String floatToString(float value);
    String createAirJSON(float value, String ID);
    String createAirStationJSON(float temp, float humid, float illuminance, float atmosphere, 
                                        float noise, float pm10, float pm25, float co,float co2, float so2, float no2, float o3);
    String createAirSoilStationJSON(float temp, float humid, float illuminance, float atmosphere, 
                                        float noise, float pm10, float pm25, float co,float co2, float so2, float no2, float o3,float tempSoil, float humidSoil, float ph, float ec, float nito, float photpho, float kali);
    String createSoilStationJSON(float tempSoil, float humidSoil, float ph, float ec, float nito, float photpho, float kali);
};


class SENSOR_RS485{
  private:
  uint8_t* data_air_HUMID_TEMP;
  uint8_t* data_air_NOISE;
  uint8_t* data_air_PM25_PM10;
  uint8_t* data_air_ATMOSPHERE;
  uint8_t* data_air_LUX;

  uint8_t* data_air_TEMP;
  uint8_t* data_air_HUMID;
  uint8_t* data_air_CO;
  uint8_t* data_air_CO2;
  uint8_t* data_air_SO2;
  uint8_t* data_air_NO2;
  uint8_t* data_air_O3;
  uint8_t* data_air_PM25;
  uint8_t* data_air_PM10;

  
  uint8_t* data_soil_HUMID_TEMP;
  uint8_t* data_soil_EC;
  uint8_t* data_soil_NPK;
  uint8_t* data_soil_PH;

  public:
  SENSOR_RS485();
  ~SENSOR_RS485();
  uint8_t* getDataAIR_HUMID_TEMP();
  uint8_t* getDataAIR_NOISE();
  uint8_t* getDataAIR_PM25_PM10();
  uint8_t* getDataAIR_ATMOSPHERE();
  uint8_t* getDataAIR_LUX();

  uint8_t* getDataAIR_TEMP();
  uint8_t* getDataAIR_HUMID();
  uint8_t* getDataAIR_CO();
  uint8_t* getDataAIR_CO2();
  uint8_t* getDataAIR_SO2();
  uint8_t* getDataAIR_NO2();
  uint8_t* getDataAIR_O3();
  uint8_t* getDataAIR_PM25();
  uint8_t* getDataAIR_PM10();
  

  uint8_t* getDataSOIL_PH();
  uint8_t* getDataSOIL_HUMID_TEMP();
  uint8_t* getDataSOIL_NPK();
  uint8_t* getDataSOIL_EC();
};

#endif
