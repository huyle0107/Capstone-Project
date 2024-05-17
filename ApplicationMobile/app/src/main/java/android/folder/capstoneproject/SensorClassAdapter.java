package android.folder.capstoneproject;

import android.annotation.SuppressLint;
import android.content.ClipData;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

public class SensorClassAdapter extends RecyclerView.Adapter<SensorClassAdapter.SensorClassViewHolder>{
    private List<SensorClass> mListSensor;

    public SensorClassAdapter(List<SensorClass> mListClass)
    {
        this.mListSensor = mListClass;
    }

    @NonNull
    @Override
    public SensorClassViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType)
    {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_sensor, parent, false);
        return new SensorClassViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull SensorClassViewHolder holder, int position)
    {
        SensorClass sensor = mListSensor.get(position);
        if (sensor == null)
        {
            return;
        }

        holder.imgClass.setImageResource(sensor.getImage());
        holder.SensorItem.setText(sensor.getSensor_item());
        holder.SensorValue.setText(sensor.getSensor_value());

        holder.layitem.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                OnClickGoToDetail(sensor);
            }
        });

    }

    private void OnClickGoToDetail(SensorClass sensor)
    {
//        Intent intent = new Intent(mContext, Detail_Activity.class);
//        Bundle bundle = new Bundle();
//        cla_ss.setClass_item("http://khotailieuhoctruongthcschuvanan.net/mobile_lectures/" + cla_ss.getClass_item().replace("Lớp ", "grade") + "/");
//        bundle.putSerializable("object_class", cla_ss);
//        intent.putExtras(bundle);
//        mContext.startActivity(intent);
    }

    @Override
    public int getItemCount()
    {
        if (mListSensor != null)
        {
            return mListSensor.size();
        }
        return 0;
    }

    public class SensorClassViewHolder extends RecyclerView.ViewHolder {

        private ImageView imgClass;
        private TextView SensorItem;
        private TextView SensorValue;
        private LinearLayout layitem;

        public SensorClassViewHolder(@NonNull View itemView)
        {
            super(itemView);

            imgClass = itemView.findViewById(R.id.img_background_sensors);
            SensorItem = itemView.findViewById(R.id.sensor_name);
            SensorValue = itemView.findViewById(R.id.sensor_value);
            layitem = itemView.findViewById(R.id.layout_item);
        }
    }
}
