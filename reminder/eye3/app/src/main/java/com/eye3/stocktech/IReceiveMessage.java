/// @file IReceiveMessage.java
/// @brief
/// @author QRS
/// @blog qrsforever.github.io
/// @version 1.0
/// @date 2019-05-16 18:40:10

package com.eye3.stocktech;

public interface IReceiveMessage {

    public void onData(String topic, String payload);
}
