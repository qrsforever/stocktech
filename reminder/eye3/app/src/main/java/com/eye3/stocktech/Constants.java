package com.eye3.stocktech;

import android.os.Build;

public class Constants {

    public final static String HOST     = "tcp://192.168.1.222:1883";
    public final static String USERNAME = "stocktech";
    public final static String PASSWORD = "stocktech";
    public final static String CLIENTID = Build.SERIAL;

    public final static String PUB_TOPIC_WILL = "/stocktech/reminder/will";
    public final static String SUB_TOPIC_LATESTQUOTA = "/stocktech/reminder/latestquota";

    public final static String ACTIONS_RECV_MESSAGE = "com.eye3.stocktech.recv.message";
}
