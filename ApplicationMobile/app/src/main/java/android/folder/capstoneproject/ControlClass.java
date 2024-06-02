package android.folder.capstoneproject;

import java.io.Serializable;

public class ControlClass implements Serializable
{
    private int image;
    private String control_item;
    private String control_value;

    public ControlClass(int image, String control_item, String control_value)
    {
        this.image = image;
        this.control_item = control_item;
        this.control_value = control_value;
    }

    public int getImage()
    {
        return image;
    }

    public void setImage(int image)
    {
        this.image = image;
    }

    public String getControl_item() {
        return control_item;
    }

    public void setControl_item(String control_item)
    {
        this.control_item = control_item;
    }

    public String getControl_value()
    {
        return control_value;
    }

    public void setControl_value(String control_value)
    {
        this.control_value = control_value;
    }
}
