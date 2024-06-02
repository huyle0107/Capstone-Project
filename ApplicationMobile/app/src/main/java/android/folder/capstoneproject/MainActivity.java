package android.folder.capstoneproject;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;
import androidx.fragment.app.FragmentTransaction;

import android.content.Intent;
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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getSupportActionBar().hide();   //This line hides the action bar

        setContentView(R.layout.activity_main);

        bottomNavigationView = findViewById(R.id.bottom_nav);

        if (getIntent() != null)
        {
            String selectedOption = getIntent().getStringExtra("Option");
            String Starttime = getIntent().getStringExtra("Starttime");
            String Endtime = getIntent().getStringExtra("Endtime");

            try {
                // Tạo JSONObject mới cho lịch trình mới
                JSONObject newScheduleObject = new JSONObject();
                newScheduleObject.put("schedulerName", "LỊCH TƯỚI TIÊU");
                newScheduleObject.put("isActive", selectedOption);
                newScheduleObject.put("startTime", Starttime);
                newScheduleObject.put("stopTime", Endtime);

                // Đọc dữ liệu JSON từ Intent (nếu cần) hoặc tạo một JSONObject mới
                JSONObject data_push;
                if (getIntent().hasExtra("data_push"))
                {
                    String jsonData = getIntent().getStringExtra("data_push");
                    data_push = new JSONObject(jsonData);
                }
                else
                {
                    data_push = new JSONObject();
                    data_push.put("station_id", "sche_0001");
                    data_push.put("station_name", "SCHE 0001");
                }

                // Kiểm tra xem JSONObject có chứa mảng lịch trình không
                JSONArray scheduleArray;
                if (data_push.has("schedule"))
                {
                    scheduleArray = data_push.getJSONArray("schedule");
                }
                else
                {
                    scheduleArray = new JSONArray();
                }

                // Thêm lịch trình mới vào mảng lịch trình
                scheduleArray.put(newScheduleObject);

                // Cập nhật JSONObject chứa mảng lịch trình
                data_push.put("schedule", scheduleArray);
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