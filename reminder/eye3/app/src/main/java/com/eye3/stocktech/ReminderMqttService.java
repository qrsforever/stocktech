/// @file ReminderMqttService.java
/// @brief
/// @author QRS
/// @blog qrsforever.github.io
/// @version 1.0
/// @date 2019-05-15 20:29:44

package com.eye3.stocktech;

import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.app.Service;
import android.util.Log;
import android.widget.Toast;

import java.util.HashMap;
import java.io.UnsupportedEncodingException;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttPersistenceException;

public class ReminderMqttService extends Service {
    public static final String TAG = ReminderMqttService.class.getSimpleName();

    private MqttAndroidClient client;
    private MqttConnectOptions connectOptions;

    /* private HashMap<String, IReceiveMessage> callbacks; */

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        onConnect();
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    public void onConnect() {
        Log.i(TAG, "Connect(" + Constants.CLIENTID + ")");
        client = new MqttAndroidClient(this, Constants.HOST, Constants.CLIENTID);
        client.setCallback(onMqttCallback);
        connectOptions = new MqttConnectOptions();
        connectOptions.setCleanSession(true);
        connectOptions.setConnectionTimeout(10);
        connectOptions.setKeepAliveInterval(20);
        connectOptions.setUserName(Constants.USERNAME);
        connectOptions.setPassword(Constants.PASSWORD.toCharArray());

        String message = "{\"diedClientId\":\"" + Constants.CLIENTID + "\"}";
        Integer qos = 2;
        Boolean retained = false;
        try {
            connectOptions.setWill(Constants.PUB_TOPIC_WILL, message.getBytes(),
                    qos.intValue(), retained.booleanValue());
        } catch (Exception e) {
            Log.e(TAG, "Exception Occured", e);
            return;
        }
        try{
            client.connect(connectOptions, null, new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken arg0) {
                    Toast.makeText(getApplicationContext(), "Connnect Success",
                            Toast.LENGTH_LONG).show();
                    try {
                        client.subscribe(Constants.SUB_TOPIC_LATESTQUOTA, 0);
                        client.subscribe(Constants.SUB_TOPIC_TAPEREADING, 0);
                        client.subscribe(Constants.SUB_TOPIC_LEADERNEWS, 0);
                    } catch (MqttException e) {
                        Log.e(TAG, "Exception Occured", e);
                    }
                }
                @Override
                public void onFailure(IMqttToken arg0, Throwable arg1) {
                    Toast.makeText(getApplicationContext(), "Connnect Failure",
                            Toast.LENGTH_LONG).show();
                }
            });
        } catch (MqttException e) {
            Log.e(TAG, "Exception Occured", e);
        }
    }

    private MqttCallback onMqttCallback = new MqttCallback() {
        @Override
        public void connectionLost(Throwable cause) {
            Toast.makeText(getApplicationContext(), "Connnect Lost",
                    Toast.LENGTH_LONG).show();
        }

        @Override
        public void messageArrived(String topic, MqttMessage msg){
            Log.i(TAG, "Received Topic : " + topic);
            try {
                String payload = new String(msg.getPayload(), "utf-8");
                Log.i(TAG, "Payload: " + payload);
                Intent intent = new Intent();
                intent.setAction(Constants.ACTIONS_RECV_MESSAGE);
                intent.putExtra("payload", payload);
                sendBroadcast(intent);
            }catch (UnsupportedEncodingException e) {
                Log.e(TAG, "Exception Occured", e);
            }
        }

        @Override
        public void deliveryComplete(IMqttDeliveryToken token) {
            Log.i(TAG, "Delivery Complete");
        }
    };

    @Override
    public void onDestroy() {
        try {
            client.disconnect();
        } catch (MqttException e) {
            Log.e(TAG, "Exception Occured", e);
        }
        super.onDestroy();
    }
}

    /* public void subscribe(String topic, int qos, IReceiveMessage callback) {
     *     if (client == null)
     *         return;
     *     int[] qoss = {qos};
     *     String[] topics = {topic};
     *     try {
     *         client.subscribe(topics , qoss);
     *         callbacks.put(topic, callback);
     *         Log.d(TAG, "subscribe topic : " + topic);
     *     } catch (MqttException e) {
     *         e.printStackTrace();
     *     }
     * } */

    /* public void publish(String topic, String msg, int qos) {
     *     if (client == null)
     *         return;
     *
     *     try {
     *         MqttMessage message = new MqttMessage();
     *         message.setQos(qos);
     *         message.setPayload(msg.getBytes());
     *         client.publish(topic, message);
     *         Log.d(TAG, "publish topic : " + topic);
     *     } catch (MqttPersistenceException e) {
     *         e.printStackTrace();
     *     } catch (MqttException e) {
     *         e.printStackTrace();
     *     }
     * } */
