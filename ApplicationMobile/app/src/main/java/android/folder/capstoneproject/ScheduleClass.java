package android.folder.capstoneproject;

import java.io.Serializable;

public class ScheduleClass implements Serializable
{
    private String Schedule_name;

    private String Schedule_machine_title;
    private String Schedule_status_title;
    private String Schedule_start_title;
    private String Schedule_end_title;
    private String Schedule_machine;
    private String Schedule_status;
    private String Schedule_start;
    private String Schedule_end;

    public ScheduleClass(String Schedule_name,
                         String Schedule_machine_title,
                         String Schedule_machine,
                         String Schedule_status_title,
                         String Schedule_status,
                         String Schedule_start_title,
                         String Schedule_start,
                         String Schedule_end_title,
                         String Schedule_end)
    {
        this.Schedule_name = Schedule_name;
        this.Schedule_machine_title = Schedule_machine_title;
        this.Schedule_machine = Schedule_machine;
        this.Schedule_status_title = Schedule_status_title;
        this.Schedule_status = Schedule_status;
        this.Schedule_start_title = Schedule_start_title;
        this.Schedule_start = Schedule_start;
        this.Schedule_end_title = Schedule_end_title;
        this.Schedule_end = Schedule_end;
    }

    public String getSchedule_name() {
        return Schedule_name;
    }

    public void setSchedule_name(String Schedule_name) {
        this.Schedule_name = Schedule_name;
    }

    public String getSchedule_machine_title() {
        return Schedule_machine_title;
    }

    public void setSchedule_machine_title(String Schedule_machine_title) {
        this.Schedule_machine_title = Schedule_machine_title;
    }

    public String getSchedule_status_title() {
        return Schedule_status_title;
    }

    public void setSchedule_status_title(String Schedule_status_title) {
        this.Schedule_status_title = Schedule_status_title;
    }

    public String getSchedule_start_title() {
        return Schedule_start_title;
    }

    public void setSchedule_start_title(String Schedule_start_title) {
        this.Schedule_start_title = Schedule_start_title;
    }

    public String getSchedule_end_title() {
        return Schedule_end_title;
    }

    public void setSchedule_end_title(String Schedule_end_title) {
        this.Schedule_end_title = Schedule_end_title;
    }

    public String getSchedule_machine() {
        return Schedule_machine;
    }

    public void setSchedule_machine(String Schedule_machine) {
        this.Schedule_machine = Schedule_machine;
    }

    public String getSchedule_status() {
        return Schedule_status;
    }

    public void setSchedule_status(String Schedule_status) {
        this.Schedule_status = Schedule_status;
    }

    public String getSchedule_start() {
        return Schedule_start;
    }

    public void setSchedule_start(String Schedule_start) {
        this.Schedule_start = Schedule_start;
    }

    public String getSchedule_end() {
        return Schedule_end;
    }

    public void setSchedule_end(String Schedule_end) {
        this.Schedule_end = Schedule_end;
    }
}
