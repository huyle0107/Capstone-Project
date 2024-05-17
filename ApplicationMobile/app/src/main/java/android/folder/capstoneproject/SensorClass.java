package android.folder.capstoneproject;

import java.io.Serializable;

public class SensorClass implements Serializable
{
    private int image;
    private String sensor_item;
    private String sensor_value;

    public SensorClass(int image, String sensor_item, String sensor_value)
    {
        this.image = image;
        this.sensor_item = sensor_item;
        this.sensor_value = sensor_value;
    }

    public int getImage()
    {
        return image;
    }

    public void setImage(int image)
    {
        this.image = image;
    }

    public String getSensor_item() {
        return sensor_item;
    }

    public void setSensor_item(String sensor_item)
    {
        this.sensor_item = sensor_item;
    }

    public String getSensor_value()
    {
        return sensor_value;
    }

    public void setSensor_value(String sensor_value)
    {
        this.sensor_value = sensor_value;
    }
}
