package android.folder.capstoneproject;

import android.os.Bundle;

import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import java.util.ArrayList;
import java.util.List;

public class SensorFragment extends Fragment {

    private List<SensorClass> SensorList;
    private RecyclerView SensorRecyclerView;
    private SensorClassAdapter SensorAdapter;

    public SensorFragment() {
        // Required empty public constructor
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View rootView = inflater.inflate(R.layout.fragment_sensor, container, false);

        SensorList = generateSensorItem(10);

        SensorRecyclerView = rootView.findViewById(R.id.sensorRecyclerView);
        SensorRecyclerView.setLayoutManager(new LinearLayoutManager(getActivity()));

        SensorAdapter = new SensorClassAdapter(SensorList);
        SensorRecyclerView.setAdapter(SensorAdapter);


        return rootView;

    }

    private List<SensorClass> generateSensorItem(int a){
        List<SensorClass> SensorItems = new ArrayList<>();
        for(int i = 1; i <= a; i++)
        {
            SensorItems.add(new SensorClass(R.drawable.cloud, String.valueOf(i), "#ffffff"));
        }
        return SensorItems;
    }
}