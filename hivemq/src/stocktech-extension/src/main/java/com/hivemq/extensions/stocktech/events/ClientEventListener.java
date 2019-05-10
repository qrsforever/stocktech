/// @file StocktechListener.java
/// @brief
/// @author QRS
/// @version 1.0.0
/// @date 2019-05-10

package com.hivemq.extensions.stocktech.events;

import com.hivemq.extension.sdk.api.annotations.NotNull;
import com.hivemq.extension.sdk.api.events.client.ClientLifecycleEventListener;
import com.hivemq.extension.sdk.api.events.client.parameters.AuthenticationSuccessfulInput;
import com.hivemq.extension.sdk.api.events.client.parameters.ConnectionStartInput;
import com.hivemq.extension.sdk.api.events.client.parameters.DisconnectEventInput;
import com.hivemq.extension.sdk.api.packets.general.MqttVersion;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ClientEventListener implements ClientLifecycleEventListener {

    private static final Logger log = LoggerFactory.getLogger(ClientEventListener.class);

    @Override
    public void onMqttConnectionStart(final @NotNull ConnectionStartInput input) {

        final MqttVersion version = input.getConnectPacket().getMqttVersion();
        switch (version) {
            case V_5:
                log.info("MQTT 5 client connected with id: {} ", input.getClientInformation().getClientId());
                break;
            case V_3_1_1:
                log.info("MQTT 3.1.1 client connected with id: {} ", input.getClientInformation().getClientId());
                break;
            case V_3_1:
                log.info("MQTT 3.1 client connected with id: {} ", input.getClientInformation().getClientId());
                break;
        }
    }

    @Override
    public void onAuthenticationSuccessful(final @NotNull AuthenticationSuccessfulInput authenticationSuccessfulInput) {

    }

    @Override
    public void onDisconnect(final @NotNull DisconnectEventInput input) {
        log.info("Client disconnected with id: {} ", input.getClientInformation().getClientId());
    }
}
