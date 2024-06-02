package android.folder.capstoneproject;

import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class ControlClassAdapter extends RecyclerView.Adapter<ControlClassAdapter.ControlClassViewHolder>{
    private List<ControlClass> mListControl;
    private Context mContext;


    public ControlClassAdapter(Context context, List<ControlClass> mListControl)
    {
        this.mContext = context;
        this.mListControl = mListControl;
    }

    @NonNull
    @Override
    public ControlClassViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType)
    {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_control, parent, false);
        return new ControlClassViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ControlClassViewHolder holder, int position)
    {
        ControlClass Control = mListControl.get(position);
        if (Control == null)
        {
            return;
        }

        holder.imgClass.setImageResource(Control.getImage());
        holder.ControlItem.setText(Control.getControl_item());
        holder.ControlValue.setText(Control.getControl_value());

        if (Control.getControl_value() != null)
        {
            if (Control.getControl_value().equals("OFF"))
            {
                holder.ControlValue.setTextColor(Color.parseColor("#FF0000"));
            }
            else
            {
                holder.ControlValue.setTextColor(Color.parseColor("#00874B"));
            }
        }

        holder.layitem.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                OnClickGoToDetail(Control);
            }
        });

    }

    public void OnClickGoToDetail(ControlClass Control)
    {
        MQTTHelper mqttHelper = new MQTTHelper(mContext);
        String temp = Control.getControl_value().equals("OFF") ? "1" : "0";

        String topic = "/innovation/pumpcontroller/WSNs";
        String sensorId = "";

        switch (Control.getControl_item())
        {
            case "Irrigation Subdivision 1":
                sensorId = "pump_0001";
                break;
            case "Irrigation Subdivision 2":
                sensorId = "pump_0002";
                break;
            case "Irrigation Subdivision 3":
                sensorId = "pump_0003";
                break;
            case "Main Pump In":
                sensorId = "pump_0004";
                break;
            case "Main Pump Out":
                sensorId = "pump_0005";
                break;
            case "Mix Nutrition 1":
                topic = "/innovation/valvecontroller/WSNs";
                sensorId = "valve_0001";
                break;
            case "Mix Nutrition 2":
                topic = "/innovation/valvecontroller/WSNs";
                sensorId = "valve_0002";
                break;
            case "Mix Nutrition 3":
                topic = "/innovation/valvecontroller/WSNs";
                sensorId = "valve_0003";
                break;
        }

        if (!sensorId.isEmpty())
        {
            mqttHelper.mqttPublished(topic, sensorId, temp);
            Control.setControl_value(temp.equals("1") ? "ON" : "OFF");
            notifyDataSetChanged();
        }
    }

    @Override
    public int getItemCount()
    {
        if (mListControl!= null)
        {
            return mListControl.size();
        }
        return 0;
    }

    public class ControlClassViewHolder extends RecyclerView.ViewHolder {

        private ImageView imgClass;
        private TextView ControlItem;
        private TextView ControlValue;
        private LinearLayout layitem;

        public ControlClassViewHolder(@NonNull View itemView)
        {
            super(itemView);

            imgClass = itemView.findViewById(R.id.img_background_Control);
            ControlItem = itemView.findViewById(R.id.Control_name);
            ControlValue = itemView.findViewById(R.id.Control_value);
            layitem = itemView.findViewById(R.id.layout_item_control);
        }
    }
}