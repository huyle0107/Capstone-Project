#include "espnow.h"

uint8_t WaterNode[] = {0xd4, 0xd4, 0xda, 0x9d, 0x05, 0x00};
uint8_t SoilAirNode[] = {0xd4, 0xd4, 0xda, 0x83, 0xb2, 0x3c};
uint8_t GateWayMacAddress[] = {0x64, 0xb7, 0x08, 0x80, 0xc5, 0x44};


struct_message message;
esp_now_peer_info_t GateWayInfo;


float decode_32bit(uint8_t receivedData[9]) {
  int A = int(receivedData[5]);
  int B = int(receivedData[6]);
  int C = int(receivedData[3]);
  int D = int(receivedData[4]);
  long long int my_32_bit = A << 24 | B << 16 | C << 8 | D;

  uint8_t sign_bit = (my_32_bit >> 31) & 0x01;
  float exponent = 0;
  for (int j = 30; j > 22; j--) {
    exponent += pow(2, (j - 23)) * ((my_32_bit >> j) & 0x01);
  }

  float mantissa = 0;
  int power_count = -1;
  for (int j = 22; j >= 0; j--) {
    mantissa += pow(2, power_count) * ((my_32_bit >> j) & 0x01);
    power_count--;
  }
  mantissa += 1;
  return pow(-1, sign_bit) * pow(2, exponent - 127) * mantissa;
}

// Callback when data is sent
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial1.print("\r\nLast Packet Send Status:\t");
  Serial1.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}


// Callback when data is received
void OnDataRecv(const uint8_t *mac, const uint8_t *data, int len) {
  getResponse = true;
  Serial1.print("Received data: ");
  Serial1.write(data, len);
  Serial1.println();
}

void SendData(const char *NodeID, const char *SensorID, float value) {
    getResponse = false;
    const uint8_t *peer_addr = GateWayInfo.peer_addr;

    message.NodeID = NodeID;
    message.SensorID = SensorID;
    message.value = value;


    char messageStr[50];
    snprintf(messageStr, sizeof(messageStr), "%s/%s/%.2f", NodeID, SensorID, message.value);
  

    uint8_t messageData[strlen(messageStr)];
    memcpy(messageData, messageStr, strlen(messageStr));


    esp_err_t result = esp_now_send(peer_addr, messageData, strlen(messageStr));
    Serial1.print("Sending result: "); Serial1.println(result);
}
