package android.folder.capstoneproject;

import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.util.Log;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

public class SensorFragment extends Fragment {

    private List<SensorClass> SensorList;
    private RecyclerView SensorRecyclerView;
    private SensorClassAdapter SensorAdapter;

    private static final String TAG = "SensorFragment";
    private JsonObject topic_json;
    MQTTHelper mqttHelper;

    private int counterWater = 0;
    private int counterAir = 0;

    public SensorFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View rootView = inflater.inflate(R.layout.fragment_sensor, container, false);

        // Khởi tạo danh sách cảm biến
        SensorList = new ArrayList<>();

        startMQTT();

        SensorRecyclerView = rootView.findViewById(R.id.sensorRecyclerView);
        SensorRecyclerView.setLayoutManager(new GridLayoutManager(getActivity(), 2));

        SensorAdapter = new SensorClassAdapter(SensorList);
        SensorRecyclerView.setAdapter(SensorAdapter);

        return rootView;

    }

    private List<SensorClass> generateSensorItem(){
        List<SensorClass> SensorItems = new ArrayList<>();

        // Kiểm tra xem topic_json có null không trước khi truy cập vào nó
        if (topic_json != null)
        {
            String stationId = topic_json.get("station_id").getAsString();
            DecimalFormat decimalFormat = new DecimalFormat("0.00");

            switch(stationId)
            {
                case "air_0001":
                    for (int i = 0; i < topic_json.get("sensors").getAsJsonArray().size(); i++) {
                        JsonObject sensor = topic_json.get("sensors").getAsJsonArray().get(i).getAsJsonObject();
                        String sensorId = sensor.get("id").getAsString();
                        String sensorValue = decimalFormat.format(Double.parseDouble(sensor.get("value").getAsString()));

                        Log.d(TAG, sensorId);

                        switch (sensorId) {
                            case "temp_0001":
                                SensorItems.add(new SensorClass(R.drawable.airtemp, "Air_Temp", sensorValue + " °C"));
                                break;
                            case "humi_0001":
                                SensorItems.add(new SensorClass(R.drawable.humid, "Air_Humid", sensorValue));
                                break;
                            case "illuminance_0001":
                                SensorItems.add(new SensorClass(R.drawable.sun, "Air_Lux", sensorValue));
                                break;
                            case "atmosphere_0001":
                                SensorItems.add(new SensorClass(R.drawable.pressure, "Air_ATM", sensorValue));
                                break;
                            case "noise_0001":
                                SensorItems.add(new SensorClass(R.drawable.sound, "Air_Noise", sensorValue));
                                break;
                            case "pm10_0001":
                                SensorItems.add(new SensorClass(R.drawable.cloud, "Air_PM10", sensorValue));
                                break;
                            case "pm2.5_0001":
                                SensorItems.add(new SensorClass(R.drawable.cloud, "Air_PM2.5", sensorValue));
                                break;
                            case "CO_0001":
                                SensorItems.add(new SensorClass(R.drawable.cloud, "Air_CO", sensorValue));
                                break;
                            case "CO2_0001":
                                SensorItems.add(new SensorClass(R.drawable.co2, "Air_CO2", sensorValue));
                                break;
                            case "SO2_0001":
                                SensorItems.add(new SensorClass(R.drawable.cloud, "Air_SO2", sensorValue));
                                break;
                            case "NO2_0001":
                                SensorItems.add(new SensorClass(R.drawable.cloud, "Air_NO2", sensorValue));
                                break;
                            case "O3_0001":
                                SensorItems.add(new SensorClass(R.drawable.cloud, "Air_O3", sensorValue));
                                break;
                            case "temp_0002":
                                SensorItems.add(new SensorClass(R.drawable.soiltemp, "Soil_Temp", sensorValue + " °C"));
                                break;
                            case "humi_0002":
                                SensorItems.add(new SensorClass(R.drawable.humid, "Soil_Humid", sensorValue));
                                break;
                            case "ph_0002":
                                SensorItems.add(new SensorClass(R.drawable.ph, "Soil_PH", sensorValue));
                                break;
                            case "EC_0002":
                                SensorItems.add(new SensorClass(R.drawable.soil, "Soil_EC", sensorValue));
                                break;
                            case "Nito_0002":
                                SensorItems.add(new SensorClass(R.drawable.seeed, "Soil_N", sensorValue));
                                break;
                            case "Photpho_0002":
                                SensorItems.add(new SensorClass(R.drawable.seeed, "Soil_P", sensorValue));
                                break;
                            case "Kali_0002":
                                SensorItems.add(new SensorClass(R.drawable.seeed, "Soil_K", sensorValue));
                                break;
                        }
                    }
                    break;

                case "water_0001":
                    for (int i = 0; i < topic_json.get("sensors").getAsJsonArray().size(); i++)
                    {
                        JsonObject sensor = topic_json.get("sensors").getAsJsonArray().get(i).getAsJsonObject();
                        String sensorId = sensor.get("sensor_id").getAsString();
                        String sensorValue = decimalFormat.format(Double.parseDouble(sensor.get("sensor_value").getAsString()));

                        Log.d(TAG, sensorId);

                        switch (sensorId) {
                            case "EC_0001":
                                SensorItems.add(new SensorClass(R.drawable.water, "Water_EC", sensorValue));
                                break;
                            case "PH_0001":
                                SensorItems.add(new SensorClass(R.drawable.ph, "Water_PH", sensorValue));
                                break;
                            case "ORP_0001":
                                SensorItems.add(new SensorClass(R.drawable.water, "Water_ORP", sensorValue));
                                break;
                            case "SALINITY_0001":
                                SensorItems.add(new SensorClass(R.drawable.water, "Water_Sal", sensorValue));
                                break;
                            case "TEMP_0001":
                                SensorItems.add(new SensorClass(R.drawable.soiltemp, "Water_Temp", sensorValue + " °C"));
                                break;
                        }
                    }
                    break;
            }
        }
        else
            {
            Log.e("SensorFragment", "topic_json is NULL, cannot generate sensor items.");
        }

        return SensorItems;
    }

    public void startMQTT(){
        mqttHelper = new MQTTHelper(getActivity().getApplicationContext());
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {
                Log.d(TAG, "Failed to subscribe", cause);
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                if ((counterWater == 3) || (counterAir == 3))
                {
                    counterWater = 0;
                    counterAir = 0;
                    SensorList.clear();
                }

                if (topic.equals("/innovation/airmonitoring/WSNs"))
                {
                    Log.d(TAG, "Message received on topic: " + topic + " - " + message);
                    // Cập nhật topic_json và danh sách cảm biến
                    topic_json = parseJson(message.toString());
                    SensorList.addAll(0, generateSensorItem());
                    SensorAdapter.notifyDataSetChanged();
                    counterAir += 1;
                }

                if (topic.equals("/innovation/watermonitoring/WSNs"))
                {
                    // Cập nhật topic_json và danh sách cảm biến
                    topic_json = parseJson(message.toString());
                    SensorList.addAll(generateSensorItem()); // Thêm các cảm biến mới vào đầu danh sách
                    SensorAdapter.notifyDataSetChanged();
                    counterWater += 1;
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }

    // Phương thức để phân tích JSON từ MQTT message
    private JsonObject parseJson(String jsonString)
    {
        try
        {
            return new Gson().fromJson(jsonString, JsonObject.class);
        }
        catch (JsonParseException e)
        {
            Log.e(TAG, "Error parsing JSON", e);
            return null;
        }
    }
}

