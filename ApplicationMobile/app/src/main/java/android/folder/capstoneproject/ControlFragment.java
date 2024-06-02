package android.folder.capstoneproject;

import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.util.ArrayList;
import java.util.List;

public class ControlFragment extends Fragment {

    private List<ControlClass> ControlList = new ArrayList<>();
    private RecyclerView ControlRecyclerView;
    private ControlClassAdapter ControlAdapter;

    private static final String TAG = "ControlFragment";
    private JsonObject topic_json;
    MQTTHelper mqttHelper;

    String pump_0001_temp = "0", pump_0002_temp = "0", pump_0003_temp = "0", pump_0004_temp = "0", pump_0005_temp = "0";
    String valve_0001_temp = "0", valve_0002_temp = "0", valve_0003_temp = "0";

    public ControlFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View rootView = inflater.inflate(R.layout.fragment_control, container, false);

        startMQTT();

        ControlRecyclerView = rootView.findViewById(R.id.controlRecyclerView);
        ControlRecyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));

        ControlAdapter = new ControlClassAdapter(getActivity(), ControlList);
        ControlRecyclerView.setAdapter(ControlAdapter);

        return rootView;

    }

    private List<ControlClass> generateSensorItemSecond()
    {
        ControlList.add(new ControlClass(R.drawable.valve, "Irrigation Subdivision 1", "OFF"));
        ControlList.add(new ControlClass(R.drawable.valve, "Irrigation Subdivision 2", "OFF"));
        ControlList.add(new ControlClass(R.drawable.valve, "Irrigation Subdivision 3", "OFF"));
        ControlList.add(new ControlClass(R.drawable.valve, "Main Pump In", "OFF"));
        ControlList.add(new ControlClass(R.drawable.valve, "Main Pump Out", "OFF"));
        ControlList.add(new ControlClass(R.drawable.pump, "Mix Nutrition 1", "OFF"));
        ControlList.add(new ControlClass(R.drawable.pump, "Mix Nutrition 2", "OFF"));
        ControlList.add(new ControlClass(R.drawable.pump, "Mix Nutrition 3", "OFF"));
        return ControlList;
    }

    private List<ControlClass> generateSensorItem()
    {
        // Kiểm tra xem topic_json có null không trước khi truy cập vào nó
        if (topic_json != null)
        {
            String stationId = topic_json.get("station_id").getAsString();

            switch(stationId)
            {
                case "pump_station_0001":
                    for (int i = 0; i < topic_json.get("sensors").getAsJsonArray().size(); i++)
                    {
                        JsonObject control = topic_json.get("sensors").getAsJsonArray().get(i).getAsJsonObject();
                        String controlId = control.get("id").getAsString();
                        String controlValue = control.get("value").getAsString();

                        Log.d(TAG, controlId);

                        String status = controlValue.equals("1") ? "ON" : "OFF";

                        switch (controlId)
                        {
                            case "pump_0001":
                                if (pump_0001_temp != controlValue)
                                {
                                    pump_0001_temp = controlValue;
                                    ControlList.get(0).setControl_value(status);
                                }
                                break;
                            case "pump_0002":
                                if (pump_0002_temp != controlValue)
                                {
                                    pump_0002_temp = controlValue;
                                    ControlList.get(1).setControl_value(status);
                                }
                                break;
                            case "pump_0003":
                                if (pump_0003_temp != controlValue)
                                {
                                    pump_0003_temp = controlValue;
                                    ControlList.get(2).setControl_value(status);
                                }
                                break;
                            case "pump_0004":
                                if (pump_0004_temp != controlValue)
                                {
                                    pump_0004_temp = controlValue;
                                    ControlList.get(3).setControl_value(status);
                                }
                                break;
                            case "pump_0005":
                                if (pump_0005_temp != controlValue)
                                {
                                    pump_0005_temp = controlValue;
                                    ControlList.get(4).setControl_value(status);
                                }
                                break;
                            default:
                                Log.d(TAG, "Unknown control ID: " + controlId);
                                break;
                        }
                    }
                    break;

                case "valve_station_0001":
                    for (int i = 0; i < topic_json.get("sensors").getAsJsonArray().size(); i++)
                    {
                        JsonObject control = topic_json.get("sensors").getAsJsonArray().get(i).getAsJsonObject();
                        String controlId = control.get("id").getAsString();
                        String controlValue = control.get("value").getAsString();

                        Log.d(TAG, controlId);

                        String status = controlValue.equals("1") ? "ON" : "OFF";

                        switch (controlId)
                        {
                            case "valve_0001":
                                if (valve_0001_temp != controlValue)
                                {
                                    valve_0001_temp = controlValue;
                                    ControlList.get(5).setControl_value(status);
                                }
                                break;
                            case "valve_0002":
                                if (valve_0002_temp != controlValue)
                                {
                                    valve_0002_temp = controlValue;
                                    ControlList.get(6).setControl_value(status);
                                }
                                break;
                            case "valve_0003":
                                if (valve_0003_temp != controlValue)
                                {
                                    valve_0003_temp = controlValue;
                                    ControlList.get(7).setControl_value(status);
                                }
                                break;
                            default:
                                Log.d(TAG, "Unknown control ID: " + controlId);
                                break;
                        }
                    }
                    break;
            }
        }
        else
        {
            Log.e("ControlFragment", "topic_json is NULL, cannot generate sensor items.");
        }

        return ControlList;
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
                if (ControlList.isEmpty())
                {
                    generateSensorItemSecond();
                }
                else
                {
                    Log.d(TAG, "Message received on topic: " + topic + " - " + message);
                    // Cập nhật topic_json và danh sách cảm biến
                    topic_json = parseJson(message.toString());
                    generateSensorItem();
                }
                ControlAdapter.notifyDataSetChanged();
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
            Log.e(TAG, "Error parsing JSON");
            return null;
        }
    }
}