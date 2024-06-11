package android.folder.capstoneproject;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.view.MenuItem;
import android.view.Window;
import android.view.WindowManager;
import android.widget.FrameLayout;
import android.widget.Toast;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.navigation.NavigationBarView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    BottomNavigationView bottomNavigationView;
    FragmentManager fragmentManager;
    JSONArray scheduleArray = new JSONArray();
    JSONObject data_push = new JSONObject();
    SharedPreferences sharedPreferences;
    String temp = "hi";
    String jsonData = "{\"station_id\":\"sche_0001\",\"station_name\":\"SCHE 0001\",\"schedule\":[]}";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getSupportActionBar().hide();   //This line hides the action bar

        setContentView(R.layout.activity_main);

        bottomNavigationView = findViewById(R.id.bottom_nav);

        sharedPreferences = getSharedPreferences("MyAppName", MODE_PRIVATE);
        temp = sharedPreferences.getString("logged", temp);

        if (getIntent() != null)
        {
            String option = getIntent().getStringExtra("Option");
            String startTime = getIntent().getStringExtra("Starttime");
            String endTime = getIntent().getStringExtra("Endtime");

            try {
                if  (temp.length() == "true".length())
                {
                    data_push = new JSONObject(sharedPreferences.getString("Data", jsonData));
                }
                else
                {
                    data_push = new JSONObject(jsonData);
                }

                if (option != null && startTime != null && endTime != null)
                {
                    // Tạo JSONObject mới cho lịch trình mới
                    JSONObject newScheduleObject = new JSONObject();
                    newScheduleObject.put("schedulerName", "LỊCH TƯỚI TIÊU");
                    newScheduleObject.put("isActive", option);
                    newScheduleObject.put("startTime", startTime);
                    newScheduleObject.put("stopTime", endTime);

                    // Cập nhật JSONObject chứa mảng lịch trình
                    scheduleArray = data_push.getJSONArray("schedule");
                    scheduleArray.put(newScheduleObject);
                    data_push.put("schedule", scheduleArray);
                }

                System.out.println("||-----jsonData--------- " + data_push);

                SharedPreferences.Editor editor = sharedPreferences.edit();
                editor.putString("logged", "true");
                editor.putString("Data", data_push.toString());
                editor.apply();

                MQTTHelper mqttHelper = new MQTTHelper(getApplicationContext());

                // Khai báo một biến Handler
                Handler handler = new Handler();

                // Sử dụng Handler để gửi dữ liệu MQTT sau 3 giây
                handler.postDelayed(new Runnable() {
                    @Override
                    public void run() {
                        // Gọi phương thức để gửi dữ liệu MQTT
                        mqttHelper.mqttPublishedSchedule("/innovation/watermonitoring/WSNs/schedules", data_push);
                    }
                }, 10000);
            }
            catch (JSONException e)
            {
                e.printStackTrace();
            }
        }

        bottomNavigationView.setOnItemSelectedListener(new NavigationBarView.OnItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                switch (item.getItemId())
                {
                    case R.id.menu_home:
                        openFragment(new SensorFragment());
                        return true;

                    case R.id.menu_control:
                        openFragment(new ControlFragment());
                        return true;

                    case R.id.menu_schedule:
                        openFragment(new ScheduleFragment());
                        return true;
                }
                return false;
            }
        });

        fragmentManager = getSupportFragmentManager();
        openFragment(new SensorFragment());
    }

    private void openFragment(Fragment fragment)
    {
        FragmentTransaction transaction = fragmentManager.beginTransaction();
        transaction.replace(R.id.frameLayout, fragment);
        transaction.commit();
    }
}