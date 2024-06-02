package android.folder.capstoneproject;

import android.content.Intent;
import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.jakewharton.threetenabp.AndroidThreeTen;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttMessage;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import java.util.List;

public class ScheduleFragment extends Fragment {

    private List<ScheduleClass> ScheduleList;
    private RecyclerView ScheduleRecyclerView;
    private ScheduleClassAdapter ScheduleAdapter;
    TextView createNew;

    private static final String TAG = "ScheduleFragment";
    private String topic_json;
    MQTTHelper mqttHelper;

    public ScheduleFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View rootView = inflater.inflate(R.layout.fragment_schedule, container, false);

        AndroidThreeTen.init(getActivity());

        // Khởi tạo danh sách cảm biến
        ScheduleList = new ArrayList<>();

        startMQTT();

        ScheduleRecyclerView = rootView.findViewById(R.id.ScheduleRecyclerView);
        ScheduleRecyclerView.setLayoutManager(new GridLayoutManager(getActivity(), 1));

        ScheduleAdapter = new ScheduleClassAdapter(getActivity(), ScheduleList);
        ScheduleRecyclerView.setAdapter(ScheduleAdapter);

        createNew = rootView.findViewById(R.id.text_title);
        createNew.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getActivity(), Popup_activity.class);
                startActivity(intent);
            }
        });

        return rootView;

    }

    private List<ScheduleClass> generateScheduleItem()
    {
        List<ScheduleClass> ScheduleItems = new ArrayList<>();

        // Kiểm tra xem topic_json có null không trước khi truy cập vào nó
        if (topic_json != null)
        {
            int counter = 1;
            // Tạo một đối tượng Gson
            Gson gson = new Gson();

            // Chuyển chuỗi JSON thành đối tượng
            StationData stationData = gson.fromJson(topic_json.toString(), StationData.class);

            // In thông tin của đối tượng
            System.out.println("Station ID: " + stationData.station_id);
            System.out.println("Station Name: " + stationData.station_name);
            System.out.println("Schedule:");
            for (Schedule schedule : stationData.schedule) {
                System.out.println("Scheduler Name: " + schedule.schedulerName);
                System.out.println("Is Active: " + schedule.isActive);
                System.out.println("Start Time: " + schedule.startTime);
                System.out.println("Stop Time: " + schedule.stopTime);
                System.out.println();

                // So sánh thời gian dừng với thời gian hiện tại
                if (isCurrentTimeAfter(schedule.stopTime))
                {
                    ScheduleItems.add(new ScheduleClass((String) ("Irrigation Schedule " + counter),
                            "Machine:", schedule.isActive,
                            "Status:", "Unfinished",
                            "Start time: ", schedule.startTime,
                            "End time: ", schedule.stopTime));
                }
                else
                {
                    ScheduleItems.add(new ScheduleClass((String) ("Irrigation Schedule " + counter),
                            "Machine:", schedule.isActive,
                            "Status:", "Accomplished",
                            "Start time: ", schedule.startTime,
                            "End time: ", schedule.stopTime));
                }

                counter++;
            }
        }
        return ScheduleItems;
    }

    public static boolean isCurrentTimeAfter(String timeStr)
    {
        Date currentTime = Calendar.getInstance().getTime();
        String time = currentTime.toString().substring(11, 16);

        String[] parts = time.split(":");
        int hours = Integer.parseInt(parts[0]);
        int minutes = Integer.parseInt(parts[1]);

        // Chuyển đổi giờ và phút thành giây
        int totalSecondsCuerrent = (hours * 3600) + (minutes * 60);

        String[] partsCom = timeStr.split(":");
        int hoursCom = Integer.parseInt(partsCom[0]);
        int minutesCom = Integer.parseInt(partsCom[1]);

        // Chuyển đổi giờ và phút thành giây
        int totalSeconds = (hoursCom * 3600) + (minutesCom * 60);

        System.out.print(totalSeconds + "------" + totalSecondsCuerrent);

        if (totalSeconds > totalSecondsCuerrent)
        {
            return true;
        }
        else
        {
            return false;
        }
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
                if (topic.equals("/innovation/watermonitoring/WSNs/schedules"))
                {
                    Log.d(TAG, "Message received on topic: " + topic + " - " + message);
                    topic_json = message.toString();
                    if (!ScheduleList.isEmpty())
                    {
                        ScheduleList.clear();
                    }
                    ScheduleList.addAll(0, generateScheduleItem());
                    ScheduleAdapter.notifyDataSetChanged();
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }

    // Định nghĩa các lớp đối tượng tương ứng với cấu trúc JSON
    static class StationData {
        String station_id;
        String station_name;
        Schedule[] schedule;
    }

    static class Schedule {
        String schedulerName;
        String isActive;
        String startTime;
        String stopTime;
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