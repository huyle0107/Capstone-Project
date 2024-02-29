#include "sensor_data.h"
String SENSOR_DATA::floatToString(float value) {
  char buffer[20];  // Đủ lớn để chứa chuỗi
  sprintf(buffer, "%.2f", value);
  return String(buffer);
}

String SENSOR_DATA::createAirJSON(float value, String ID) {
  DynamicJsonDocument doc(1024);

  doc["station_id"] = "air_0001";
  doc["station_name"] = "AIR 0001";
  doc["id"] = ID;
  doc["value"] = floatToString(value);

  String jsonString;
  serializeJson(doc, jsonString);
  Serial.println("Data to pub:");
  serializeJsonPretty(doc, Serial);
  doc.clear();
  Serial.println();
  return jsonString;
}

String SENSOR_DATA::createAirStationJSON(float temp, float humid, float illuminance, float atmosphere, 
                                        float noise, float pm10, float pm25, float co,float co2, float so2, float no2, float o3) {
  DynamicJsonDocument doc(1024);

  doc["station_id"] = "air_0001";
  doc["station_name"] = "AIR 0001";

  JsonArray sensors = doc.createNestedArray("sensors");

  //Sensors for Air-Station
  JsonObject temp_sensor = sensors.createNestedObject();
  temp_sensor["id"] = "temp_0001";
  temp_sensor["value"] = floatToString(temp);

  JsonObject humid_sensor = sensors.createNestedObject();
  humid_sensor["id"] = "humi_0001";
  humid_sensor["value"] = floatToString(humid);

  JsonObject illuminance_sensor = sensors.createNestedObject();
  illuminance_sensor["id"] = "illuminance_0001";
  illuminance_sensor["value"] = floatToString(illuminance);

  JsonObject atmosphere_sensor = sensors.createNestedObject();
  atmosphere_sensor["id"] = "atmosphere_0001";
  atmosphere_sensor["value"] = floatToString(atmosphere);

  JsonObject noise_sensor = sensors.createNestedObject();
  noise_sensor["id"] = "noise_0001";
  noise_sensor["value"] = floatToString(noise);

  JsonObject pm10_sensor = sensors.createNestedObject();
  pm10_sensor["id"] = "pm10_0001";
  pm10_sensor["value"] = floatToString(pm10);

  JsonObject pm25_sensor = sensors.createNestedObject();
  pm25_sensor["id"] = "pm2.5_0001";
  pm25_sensor["value"] = floatToString(pm25);

  JsonObject co_sensor = sensors.createNestedObject();
  co_sensor["id"] = "CO_0001";
  co_sensor["value"] = floatToString(co);

  JsonObject co2_sensor = sensors.createNestedObject();
  co2_sensor["id"] = "CO2_0001";
  co2_sensor["value"] = floatToString(co2);

  JsonObject so2_sensor = sensors.createNestedObject();
  so2_sensor["id"] = "SO2_0001";
  so2_sensor["value"] = floatToString(so2);  

  JsonObject no2_sensor = sensors.createNestedObject();
  no2_sensor["id"] = "NO2_0001";
  no2_sensor["value"] = floatToString(no2);

  JsonObject o3_sensor = sensors.createNestedObject();
  o3_sensor["id"] = "O3_0001";
  o3_sensor["value"] = floatToString(03);

  String jsonString;
  serializeJson(doc, jsonString);
  doc.clear();
  return jsonString;
}

String SENSOR_DATA::createAirSoilStationJSON(float temp, float humid, float illuminance, float atmosphere, 
                                        float noise, float pm10, float pm25, float co,float co2, float so2, float no2, float o3,float tempSoil, float humidSoil, float ph, float ec, float nito, float photpho, float kali) {
  DynamicJsonDocument doc(1024);

  doc["station_id"] = "air_0001";
  doc["station_name"] = "AIR 0001";

  JsonArray sensors = doc.createNestedArray("sensors");

  //Sensors for Air-Station
  JsonObject temp_sensor = sensors.createNestedObject();
  temp_sensor["id"] = "temp_0001";
  temp_sensor["value"] = floatToString(temp);

  JsonObject humid_sensor = sensors.createNestedObject();
  humid_sensor["id"] = "humi_0001";
  humid_sensor["value"] = floatToString(humid);

  JsonObject illuminance_sensor = sensors.createNestedObject();
  illuminance_sensor["id"] = "illuminance_0001";
  illuminance_sensor["value"] = floatToString(illuminance);

  JsonObject atmosphere_sensor = sensors.createNestedObject();
  atmosphere_sensor["id"] = "atmosphere_0001";
  atmosphere_sensor["value"] = floatToString(atmosphere);

  JsonObject noise_sensor = sensors.createNestedObject();
  noise_sensor["id"] = "noise_0001";
  noise_sensor["value"] = floatToString(noise);

  JsonObject pm10_sensor = sensors.createNestedObject();
  pm10_sensor["id"] = "pm10_0001";
  pm10_sensor["value"] = floatToString(pm10);

  JsonObject pm25_sensor = sensors.createNestedObject();
  pm25_sensor["id"] = "pm2.5_0001";
  pm25_sensor["value"] = floatToString(pm25);

  JsonObject co_sensor = sensors.createNestedObject();
  co_sensor["id"] = "CO_0001";
  co_sensor["value"] = floatToString(co);

  JsonObject co2_sensor = sensors.createNestedObject();
  co2_sensor["id"] = "CO2_0001";
  co2_sensor["value"] = floatToString(co2);

  JsonObject so2_sensor = sensors.createNestedObject();
  so2_sensor["id"] = "SO2_0001";
  so2_sensor["value"] = floatToString(so2);  

  JsonObject no2_sensor = sensors.createNestedObject();
  no2_sensor["id"] = "NO2_0001";
  no2_sensor["value"] = floatToString(no2);

  JsonObject o3_sensor = sensors.createNestedObject();
  o3_sensor["id"] = "O3_0001";
  o3_sensor["value"] = floatToString(03);

  // Sensors for Soil-Station
  JsonObject tempSoil_sensor = sensors.createNestedObject();
  tempSoil_sensor["id"] = "temp_0002";
  tempSoil_sensor["value"] = floatToString(tempSoil);

  JsonObject humidSoil_sensor = sensors.createNestedObject();
  humidSoil_sensor["id"] = "humi_0002";
  humidSoil_sensor["value"] = floatToString(humidSoil);

  JsonObject ph_sensor = sensors.createNestedObject();
  ph_sensor["id"] = "ph_0002";
  ph_sensor["value"] = floatToString(ph);

  JsonObject ec_sensor = sensors.createNestedObject();
  ec_sensor["id"] = "EC_0002";
  ec_sensor["value"] = floatToString(ec);

  JsonObject nito_sensor = sensors.createNestedObject();
  nito_sensor["id"] = "Nito_0002";
  nito_sensor["value"] = floatToString(nito);

  JsonObject photpho_sensor = sensors.createNestedObject();
  photpho_sensor["id"] = "Photpho_0002";
  photpho_sensor["value"] = floatToString(photpho);

  JsonObject kali_sensor = sensors.createNestedObject();
  kali_sensor["id"] = "Kali_0002";
  kali_sensor["value"] = floatToString(kali);

  String jsonString;
  serializeJson(doc, jsonString);
  doc.clear();
  return jsonString;
}
String SENSOR_DATA::createSoilStationJSON(float tempSoil, float humidSoil, float ph, float ec, float nito, float photpho, float kali) {
  DynamicJsonDocument doc(1024);

  doc["station_id"] = "soil_0001";
  doc["station_name"] = "SOIL 0001";
  // doc["gps_longitude"] = 106.89;
  // doc["gps_latitude"] = 10.5;

  JsonArray sensors = doc.createNestedArray("sensors");

  JsonObject temp_sensor = sensors.createNestedObject();
  temp_sensor["id"] = "temp_0001";
  //temp_sensor["sensor_name"] = "Nhiệt Độ";
  temp_sensor["value"] = floatToString(tempSoil);
  //temp_sensor["sensor_unit"] = "°C";

  JsonObject humi_sensor = sensors.createNestedObject();
  humi_sensor["id"] = "humi_0001";
  //humi_sensor["sensor_name"] = "Độ Ẩm";
  humi_sensor["value"] = floatToString(humidSoil);
  //humi_sensor["sensor_unit"] = "%";

  JsonObject ph_sensor = sensors.createNestedObject();
  ph_sensor["id"] = "ph_0001";
  //ph_sensor["sensor_name"] = "PH";
  ph_sensor["value"] = floatToString(ph);
  //ph_sensor["sensor_unit"] = "";

  JsonObject ec_sensor = sensors.createNestedObject();
  ec_sensor["id"] = "EC_0001";
  //ec_sensor["sensor_name"] = "EC";
  ec_sensor["value"] = floatToString(ec);
  //ec_sensor["sensor_unit"] = "ms/cm";

  JsonObject nito_sensor = sensors.createNestedObject();
  nito_sensor["id"] = "Nito_0001";
  //nito_sensor["sensor_name"] = "N";
  nito_sensor["value"] = floatToString(nito);
  //nito_sensor["sensor_unit"] = "ms/cm";

  JsonObject photpho_sensor = sensors.createNestedObject();
  photpho_sensor["id"] = "Photpho_0001";
  //photpho_sensor["sensor_name"] = "P";
  photpho_sensor["value"] = floatToString(photpho);
  //photpho_sensor["sensor_unit"] = "ms/cm";

  JsonObject kali_sensor = sensors.createNestedObject();
  kali_sensor["id"] = "Kali_0001";
  //kali_sensor["sensor_name"] = "K";
  kali_sensor["value"] = floatToString(kali);
  //kali_sensor["sensor_unit"] = "ms/cm";

  String jsonString;
  serializeJson(doc, jsonString);
  doc.clear();
  return jsonString;
}



///////////////////////////////////////

SENSOR_RS485::SENSOR_RS485(){
  relay_ON = new uint8_t[8]{0xFF, 0x05, 0x00, 0x00, 0xFF, 0x00, 0x99, 0xE4};
  relay_OFF = new uint8_t[8]{0xFF, 0x05, 0x00, 0x00, 0x00, 0x00, 0xD8, 0x14};

  data_air_HUMID_TEMP = new uint8_t[8]{0x14, 0x03, 0x01, 0xF4, 0x00, 0x02, 0x86, 0xC0};
  data_air_NOISE = new uint8_t[8]{0x14, 0x03, 0x01, 0xF6, 0x00, 0x01, 0x67, 0x01};
  data_air_PM25_PM10 = new uint8_t[8]{0x14, 0x03, 0x01, 0xF7, 0x00, 0x02, 0x76, 0xC0};
  data_air_ATMOSPHERE = new uint8_t[8]{0x14, 0x03, 0x01, 0xF9, 0x00, 0x01, 0x57, 0x02};
  data_air_LUX = new uint8_t[8]{0x14, 0x03, 0x01, 0xFA, 0x00, 0x02, 0xE7, 0x03};
  
  data_air_TEMP = new uint8_t[8]{0x03, 0x03, 0x00, 0x00, 0x00, 0x01, 0x85, 0xE8}; 
  data_air_HUMID = new uint8_t[8]{0x03, 0x03, 0x00, 0x01, 0x00, 0x01, 0xD4, 0x28};
  data_air_CO = new uint8_t[8]{0x0E, 0x03, 0x00, 0x02, 0x00, 0x01, 0x25, 0x35};
  data_air_CO2 = new uint8_t[8]{0x02, 0x03, 0x00, 0x04, 0x00, 0x01, 0xC5, 0xF8};
  data_air_SO2 = new uint8_t[8]{0x0D, 0x03, 0x00, 0x02, 0x00, 0x01, 0x25, 0x06};
  data_air_NO2 = new uint8_t[8]{0x0C, 0x03, 0x00, 0x02, 0x00, 0x01, 0x24, 0xD7};
  data_air_O3 = new uint8_t[8]{0x0B, 0x03, 0x00, 0x02, 0x00, 0x01, 0x25, 0x60};
  data_air_PM25 = new uint8_t[8]{0x04, 0x03, 0x00, 0x0C, 0x00, 0x01, 0x44, 0x5C};
  data_air_PM10 = new uint8_t[8]{0x04, 0x03, 0x00, 0x0D, 0x00, 0x01, 0x15, 0x9C};


  data_soil_HUMID_TEMP = new uint8_t[8]{0x01, 0x03, 0x00, 0x12, 0x00, 0x02, 0x64, 0x0E};
  data_soil_EC = new uint8_t[8]{0x01, 0x03, 0x00, 0x15, 0x00, 0x01, 0x95, 0xCE};
  data_soil_NPK = new uint8_t[8]{0x01, 0x03, 0x00, 0x1E, 0x00, 0x03, 0x65, 0xCD};
  data_soil_PH = new uint8_t[8]{0x01, 0x03, 0x00, 0x06, 0x00, 0x01, 0x64, 0x0B};
};

SENSOR_RS485::~SENSOR_RS485() {
  delete[] relay_ON;
  delete[] relay_OFF;


  delete[] data_air_HUMID_TEMP;
  delete[] data_air_NOISE;
  delete[] data_air_PM25_PM10;
  delete[] data_air_ATMOSPHERE;
  delete[] data_air_LUX;
  
  delete[] data_soil_PH;
  delete[] data_soil_HUMID_TEMP;
  delete[] data_soil_NPK;
  delete[] data_soil_EC;
};

uint8_t* SENSOR_RS485::relay_turnON(){
  return relay_ON;
};

uint8_t* SENSOR_RS485::relay_turnOFF(){
  return relay_OFF;
};


uint8_t* SENSOR_RS485::getDataAIR_HUMID_TEMP(){
  return data_air_HUMID_TEMP;
};

uint8_t* SENSOR_RS485::getDataAIR_NOISE(){
  return data_air_NOISE;
};

uint8_t* SENSOR_RS485::getDataAIR_PM25_PM10(){
  return data_air_PM25_PM10;
};

uint8_t* SENSOR_RS485::getDataAIR_ATMOSPHERE(){
  return data_air_ATMOSPHERE;
};

uint8_t* SENSOR_RS485::getDataAIR_LUX(){
  return data_air_LUX;
};

uint8_t* SENSOR_RS485::getDataAIR_HUMID(){
  return data_air_HUMID;
};

uint8_t* SENSOR_RS485::getDataAIR_TEMP(){
  return data_air_TEMP;
};

uint8_t* SENSOR_RS485::getDataAIR_CO(){
  return data_air_CO;
};

uint8_t* SENSOR_RS485::getDataAIR_CO2(){
  return data_air_CO2;
};

uint8_t* SENSOR_RS485::getDataAIR_SO2(){
  return data_air_SO2;
};

uint8_t* SENSOR_RS485::getDataAIR_NO2(){
  return data_air_NO2;
};

uint8_t* SENSOR_RS485::getDataAIR_O3(){
  return data_air_O3;
};

uint8_t* SENSOR_RS485::getDataAIR_PM25(){
  return data_air_PM25;
};

uint8_t* SENSOR_RS485::getDataAIR_PM10(){
  return data_air_PM10;
};

uint8_t* SENSOR_RS485::getDataSOIL_PH(){
  return data_soil_PH;
};

uint8_t* SENSOR_RS485::getDataSOIL_HUMID_TEMP(){
  return data_soil_HUMID_TEMP;
};

uint8_t* SENSOR_RS485::getDataSOIL_NPK(){
  return data_soil_NPK;
};

uint8_t* SENSOR_RS485::getDataSOIL_EC(){
  return data_soil_EC;
};
