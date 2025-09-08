package com.Project.InventoryManagement.DTO;

public class SuccessMsg {
    private String msg;

    public SuccessMsg() {
        msg = "Success";
    }

    public String getMsg(){
        return msg;
    }

    public void setMsg(String newMsg){
        this.msg = newMsg;
    }
}
