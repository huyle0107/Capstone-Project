package android.folder.capstoneproject;

import android.content.Context;
import android.graphics.Color;
import android.os.CountDownTimer;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.List;

public class ScheduleClassAdapter extends RecyclerView.Adapter<ScheduleClassAdapter.ScheduleClassViewHolder>{
    private List<ScheduleClass> mListSchedule;
    private Context mContext;

    public ScheduleClassAdapter(Context context, List<ScheduleClass> mListClass)
    {
        this.mContext = context;
        this.mListSchedule = mListClass;
    }

    @NonNull
    @Override
    public ScheduleClassViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType)
    {
        View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.item_schedule, parent, false);
        return new ScheduleClassViewHolder(view);
    }

    @Override
    public void onBindViewHolder(@NonNull ScheduleClassViewHolder holder, int position)
    {
        ScheduleClass Schedule = mListSchedule.get(position);
        if (Schedule == null)
        {
            return;
        }

        holder.ScheduleName.setText(Schedule.getSchedule_name());
        holder.ScheduleMachine_title.setText(Schedule.getSchedule_machine_title());
        holder.ScheduleMachine.setText(Schedule.getSchedule_machine());
        holder.ScheduleStatus_title.setText(Schedule.getSchedule_status_title());
        holder.ScheduleStatus.setText(Schedule.getSchedule_status());
        holder.ScheduleStart_title.setText(Schedule.getSchedule_start_title());
        holder.ScheduleStart.setText(Schedule.getSchedule_start());
        holder.ScheduleEnd_title.setText(Schedule.getSchedule_end_title());
        holder.ScheduleEnd.setText(Schedule.getSchedule_end());

        if (Schedule.getSchedule_status() != null)
        {
            if (Schedule.getSchedule_status().equals("Accomplished"))
            {
                holder.ScheduleStatus.setTextColor(Color.parseColor("#00874B"));
            }
            else
            {
                holder.ScheduleStatus.setTextColor(Color.parseColor("#FF0000"));
            }
        }

        holder.layitem.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v)
            {
                OnClickGoToDetail(Schedule);
            }
        });

    }

    private void OnClickGoToDetail(ScheduleClass Schedule)
    {
        Log.d("Schedule", "Clicked is toggle");
    }

    @Override
    public int getItemCount()
    {
        if (mListSchedule != null)
        {
            return mListSchedule.size();
        }
        return 0;
    }

    public class ScheduleClassViewHolder extends RecyclerView.ViewHolder {

        private TextView ScheduleName;
        private TextView ScheduleMachine_title;
        private TextView ScheduleMachine;
        private TextView ScheduleStatus_title;
        private TextView ScheduleStatus;
        private TextView ScheduleStart_title;
        private TextView ScheduleStart;
        private TextView ScheduleEnd_title;
        private TextView ScheduleEnd;
        private LinearLayout layitem;

        public ScheduleClassViewHolder(@NonNull View itemView)
        {
            super(itemView);
            ScheduleName = itemView.findViewById(R.id.Schedule_name);
            ScheduleMachine_title = itemView.findViewById(R.id.Schedule_machine_title);
            ScheduleMachine = itemView.findViewById(R.id.Schedule_machine);
            ScheduleStatus_title = itemView.findViewById(R.id.Schedule_status_title);
            ScheduleStatus = itemView.findViewById(R.id.Schedule_status);
            ScheduleStart_title = itemView.findViewById(R.id.Schedule_start_title);
            ScheduleStart = itemView.findViewById(R.id.Schedule_start);
            ScheduleEnd_title = itemView.findViewById(R.id.Schedule_end_title);
            ScheduleEnd = itemView.findViewById(R.id.Schedule_end);
            layitem = itemView.findViewById(R.id.layout_item_schedule);
        }
    }
}
