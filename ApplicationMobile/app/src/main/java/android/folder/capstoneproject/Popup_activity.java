package android.folder.capstoneproject;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.InputType;
import android.view.KeyEvent;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.textfield.TextInputEditText;

import java.util.HashMap;
import java.util.Map;

public class Popup_activity extends AppCompatActivity
{
    private TextInputEditText textInputStart, textInputEnd;
    private Button buttonConfirm;
    private Spinner spinnerOptions;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        getSupportActionBar().hide();   //This line hides the action bar

        setContentView(R.layout.activity_popup);

        textInputStart = findViewById(R.id.Starttime);
        textInputEnd = findViewById(R.id.Endtime);
        buttonConfirm = findViewById(R.id.buttonConfirm);
        spinnerOptions = findViewById(R.id.spinnerOptions);

        // kill keyboard when enter is pressed
        textInputStart.setInputType(InputType.TYPE_TEXT_VARIATION_URI); // optional - sets the keyboard to URL mode
        textInputStart.setOnKeyListener(new View.OnKeyListener() {
            /**
             * This listens for the user to press the enter button on
             * the keyboard and then hides the virtual keyboard
             */
            public boolean onKey(View arg0, int arg1, KeyEvent event) {
                // If the event is a key-down event on the "enter" button
                if ((event.getAction() == KeyEvent.ACTION_DOWN) &&
                        (arg1 == KeyEvent.KEYCODE_ENTER)) {
                    InputMethodManager imm = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);
                    imm.hideSoftInputFromWindow(textInputStart.getWindowToken(), 0);
                    return true;
                }
                return false;
            }
        });

        // kill keyboard when enter is pressed
        textInputEnd.setInputType(InputType.TYPE_TEXT_VARIATION_URI); // optional - sets the keyboard to URL mode
        textInputEnd.setOnKeyListener(new View.OnKeyListener() {
            /**
             * This listens for the user to press the enter button on
             * the keyboard and then hides the virtual keyboard
             */
            public boolean onKey(View arg0, int arg1, KeyEvent event) {
                // If the event is a key-down event on the "enter" button
                if ((event.getAction() == KeyEvent.ACTION_DOWN) &&
                        (arg1 == KeyEvent.KEYCODE_ENTER)) {
                    InputMethodManager imm = (InputMethodManager) getSystemService(INPUT_METHOD_SERVICE);
                    imm.hideSoftInputFromWindow(textInputEnd.getWindowToken(), 0);
                    return true;
                }
                return false;
            }
        });

        buttonConfirm.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                String selectedOption = (String) spinnerOptions.getSelectedItem();
                String Starttime = String.valueOf(textInputStart.getText());
                String Endtime = String.valueOf(textInputEnd.getText());

                // Tạo Intent để truyền dữ liệu
                Intent intent = new Intent(Popup_activity.this, MainActivity.class);
                intent.putExtra("Option", selectedOption);
                intent.putExtra("Starttime", Starttime);
                intent.putExtra("Endtime", Endtime);

                // Chuyển sang MainActivity để thêm ScheduleFragment vào fragment_container
                startActivity(intent);
            }

        });
    }
}
