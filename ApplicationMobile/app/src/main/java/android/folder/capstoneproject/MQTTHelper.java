package android.folder.capstoneproject;

import android.content.Context;
import android.util.Log;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.DisconnectedBufferOptions;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttPersistenceException;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.nio.charset.Charset;
import java.util.UUID;

public class MQTTHelper {
    public MqttAndroidClient mqttAndroidClient;

    private String jsonPump = "{\"station_id\":\"pump_station_0001\",\"station_name\":\"Irrigation station\",\"sensors\":[{\"id\":\"pump_0001\",\"value\":\"0\"},{\"id\":\"pump_0002\",\"value\":\"0\"},{\"id\":\"pump_0003\",\"value\":\"0\"},{\"id\":\"pump_0004\",\"value\":\"0\"},{\"id\":\"pump_0005\",\"value\":\"0\"}]}";
    private String jsonValve = "{\"station_id\":\"valve_station_0001\",\"station_name\":\"Mix Nutrition\",\"sensors\":[{\"id\":\"valve_0001\",\"value\":\"0\"},{\"id\":\"valve_0002\",\"value\":\"0\"},{\"id\":\"valve_0003\",\"value\":\"0\"}]}";

    public final String[] arrayTopics = {"/innovation/airmonitoring/WSNs",
            "/innovation/watermonitoring/WSNs",
            "/innovation/pumpcontroller",
            "/innovation/valvecontroller",
            "/innovation/watermonitoring/WSNs/schedules"
    };

    public final String MQTT_TOPIC_PUB_PUMP = "/innovation/pumpcontroller/WSNs";
    public final String MQTT_TOPIC_PUB_VALVE = "/innovation/valvecontroller/WSNs";

    final String CLIENT_ID = UUID.randomUUID().toString(); ;
    final String MQTT_USERNAME = "innovation";
    final String MQTT_PASSWORD = "Innovation_RgPQAZoA5N";

    final String MQTT_SERVER = "tcp://mqttserver.tk:1883";

    public MQTTHelper(Context context)
    {
        mqttAndroidClient = new MqttAndroidClient(context, MQTT_SERVER, CLIENT_ID);
        mqttAndroidClient.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean b, String s) {
                Log.w("mqtt", s);
            }

            @Override
            public void connectionLost(Throwable throwable) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage mqttMessage) throws Exception {
                Log.w("Mqtt", mqttMessage.toString());
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {

            }
        });
        connect();
    }

    public void setCallback(MqttCallbackExtended callback) {
        mqttAndroidClient.setCallback(callback);
    }

    private void connect(){
        MqttConnectOptions mqttConnectOptions = new MqttConnectOptions();
        mqttConnectOptions.setAutomaticReconnect(true);
        mqttConnectOptions.setCleanSession(false);
        mqttConnectOptions.setUserName(MQTT_USERNAME);
        mqttConnectOptions.setPassword(MQTT_PASSWORD.toCharArray());

        try {

            mqttAndroidClient.connect(mqttConnectOptions, null, new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {

                    DisconnectedBufferOptions disconnectedBufferOptions = new DisconnectedBufferOptions();
                    disconnectedBufferOptions.setBufferEnabled(true);
                    disconnectedBufferOptions.setBufferSize(100);
                    disconnectedBufferOptions.setPersistBuffer(false);
                    disconnectedBufferOptions.setDeleteOldestMessages(false);
                    mqttAndroidClient.setBufferOpts(disconnectedBufferOptions);
                    subscribeToTopic();
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Log.w("Mqtt", "Failed to connect to: " + MQTT_SERVER + exception.toString());
                }
            });


        } catch (MqttException ex){
            ex.printStackTrace();
        }
    }

    public void mqttPublished(String topic, String id, String value)
    {
        MqttConnectOptions mqttConnectOptions = new MqttConnectOptions();
        mqttConnectOptions.setAutomaticReconnect(true);
        mqttConnectOptions.setCleanSession(false);
        mqttConnectOptions.setUserName(MQTT_USERNAME);
        mqttConnectOptions.setPassword(MQTT_PASSWORD.toCharArray());

        try {
            mqttAndroidClient.connect(mqttConnectOptions, null, new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken)
                {
                    DisconnectedBufferOptions disconnectedBufferOptions = new DisconnectedBufferOptions();
                    disconnectedBufferOptions.setBufferEnabled(true);
                    disconnectedBufferOptions.setBufferSize(100);
                    disconnectedBufferOptions.setPersistBuffer(false);
                    disconnectedBufferOptions.setDeleteOldestMessages(false);
                    mqttAndroidClient.setBufferOpts(disconnectedBufferOptions);
                    try
                    {
                        JSONObject data;

                        if (MQTT_TOPIC_PUB_PUMP.equals(topic))
                        {
                            Log.d("MqttHelper", "Publish pump to Topic!!!");
                            data = new JSONObject(jsonPump);
                        }
                        else if (MQTT_TOPIC_PUB_VALVE.equals(topic))
                        {
                            Log.d("MqttHelper", "Publish valve to Topic!!!");
                            data = new JSONObject(jsonValve);
                        }
                        else return;

                        JSONArray sensors = data.getJSONArray("sensors");
                        for (int i = 0; i < sensors.length(); i++)
                        {
                            JSONObject sensor = sensors.getJSONObject(i);
                            if (sensor.getString("id").equals(id))
                            {
                                sensor.put("value", value);
                                break;
                            }
                        }

                        Log.d("MqttHelper", data.toString());

                        if (mqttAndroidClient != null && mqttAndroidClient.isConnected())
                        {
                            MqttMessage message = new MqttMessage();
                            message.setPayload(data.toString().getBytes());

                            mqttAndroidClient.publish(topic, message);
                            Log.d("MqttHelper", "Published successfully");
                        }
                        else
                        {
                            Log.e("MqttHelper", "MQTT client is not connected. Cannot publish message.");
                        }

                    }
                    catch (MqttException | JSONException e) {
                        e.printStackTrace();
                    }
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Log.w("Mqtt", "Failed to connect to: " + MQTT_SERVER + exception.toString());
                }
            });


        } catch (MqttException ex){
            ex.printStackTrace();
        }
    }

    public void mqttPublishedSchedule(String topic, JSONObject data_push)
    {
        MqttConnectOptions mqttConnectOptions = new MqttConnectOptions();
        mqttConnectOptions.setAutomaticReconnect(true);
        mqttConnectOptions.setCleanSession(false);
        mqttConnectOptions.setUserName(MQTT_USERNAME);
        mqttConnectOptions.setPassword(MQTT_PASSWORD.toCharArray());

        try {
            mqttAndroidClient.connect(mqttConnectOptions, null, new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken)
                {
                    DisconnectedBufferOptions disconnectedBufferOptions = new DisconnectedBufferOptions();
                    disconnectedBufferOptions.setBufferEnabled(true);
                    disconnectedBufferOptions.setBufferSize(100);
                    disconnectedBufferOptions.setPersistBuffer(false);
                    disconnectedBufferOptions.setDeleteOldestMessages(false);
                    mqttAndroidClient.setBufferOpts(disconnectedBufferOptions);
                    try
                    {
                        Log.d("MqttHelper", data_push.toString());

                        if (mqttAndroidClient != null && mqttAndroidClient.isConnected())
                        {
                            MqttMessage message = new MqttMessage();
                            message.setPayload(data_push.toString().getBytes());

                            mqttAndroidClient.publish(topic, message);
                            Log.d("MqttHelper", "Published successfully");
                        }
                        else
                        {
                            Log.e("MqttHelper", "MQTT client is not connected. Cannot publish message.");
                        }

                    }
                    catch (MqttException e) {
                        e.printStackTrace();
                    }
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                    Log.w("Mqtt", "Failed to connect to: " + MQTT_SERVER + exception.toString());
                }
            });


        } catch (MqttException ex){
            ex.printStackTrace();
        }
    }

    private void subscribeToTopic() {
        for(int i = 0; i < arrayTopics.length; i++) {
            try {
                mqttAndroidClient.subscribe(arrayTopics[i], 0, null, new IMqttActionListener() {
                    @Override
                    public void onSuccess(IMqttToken asyncActionToken) {
                        Log.d("TEST", "Subscribed!");
                    }

                    @Override
                    public void onFailure(IMqttToken asyncActionToken, Throwable exception) {
                        Log.d("TEST", "Subscribed fail!");
                    }
                });

            } catch (MqttException ex) {
                System.err.println("Exceptionst subscribing");
                ex.printStackTrace();
            }
        }
    }

}