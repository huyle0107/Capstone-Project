#include "sensor_data.h"

String SENSOR_DATA::floatToString(float value) {
  char buffer[20];  // Đủ lớn để chứa chuỗi
  sprintf(buffer, "%.2f", value);
  return String(buffer);
}

String SENSOR_DATA::createWaterStationJSON(float EC, float PH, float ORP, float TEMP, float SALINITY){

  DynamicJsonDocument doc(1024);

  doc["station_id"] = "water_0001";
  doc["station_name"] = "WATER 0001";

  JsonArray sensors = doc.createNestedArray("sensors");

  //Sensors for Air-Station
  JsonObject TEMP_sensor = sensors.createNestedObject();
  TEMP_sensor["id"] = "TEMP_0001";
  TEMP_sensor["value"] = floatToString(TEMP);

  JsonObject EC_sensor = sensors.createNestedObject();
  EC_sensor["id"] = "EC_0001";
  EC_sensor["value"] = floatToString(EC);

  JsonObject PH_sensor = sensors.createNestedObject();
  PH_sensor["id"] = "PH_0001";
  PH_sensor["value"] = floatToString(PH);

  JsonObject ORP_sensor = sensors.createNestedObject();
  ORP_sensor["id"] = "ORP_0001";
  ORP_sensor["value"] = floatToString(ORP);

  JsonObject SALINITY_sensor = sensors.createNestedObject();
  SALINITY_sensor["id"] = "SALINITY_0001";
  SALINITY_sensor["value"] = floatToString(SALINITY);

  String jsonString;
  serializeJson(doc, jsonString);
  doc.clear();
  return jsonString;
}




SENSOR_RS485::SENSOR_RS485(){
  data_water_ec = new uint8_t[8]{0x04, 0x03, 0x00, 0x00, 0x00, 0x02, 0xC4, 0x5E};
  data_water_salinity = new uint8_t[8]{0x04, 0x03, 0x00, 0x08, 0x00, 0x02, 0x45, 0x9C};
  data_water_ph = new uint8_t[8]{0x02, 0x03, 0x00, 0x01, 0x00, 0x02, 0x95, 0xF8};
  data_water_orp = new uint8_t[8]{0x05, 0x03, 0x00, 0x01, 0x00, 0x02, 0x94, 0x4F};
  data_water_temp = new uint8_t[8]{0x05, 0x03, 0x00, 0x03, 0x00, 0x02, 0x35, 0x8F};
};

SENSOR_RS485::~SENSOR_RS485() {
  delete[] data_water_ec;
  delete[] data_water_salinity;
  delete[] data_water_ph;
  delete[] data_water_orp;
  delete[] data_water_temp;
};

uint8_t* SENSOR_RS485::getDataWATER_EC(){
  return data_water_ec;
};

uint8_t* SENSOR_RS485::getDataWATER_SALINITY(){
  return data_water_salinity;
};

uint8_t* SENSOR_RS485::getDataWATER_PH(){
  return data_water_ph;
};

uint8_t* SENSOR_RS485::getDataWATER_ORP(){
  return data_water_orp;
};

uint8_t* SENSOR_RS485::getDataWATER_TEMP(){
  return data_water_temp;
};

