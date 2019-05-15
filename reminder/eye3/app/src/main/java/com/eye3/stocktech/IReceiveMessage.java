package com.eye3.stocktech;

public interface IReceiveMessage {

    public void onData(String topic, String payload);
}
