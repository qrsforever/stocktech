/// @file tPublishAuthorizer.java
/// @brief
/// @author QRS
/// @blog qrsforever.github.io
/// @version 1.0
/// @date 2019-05-13 19:06:17

package com.hivemq.extensions.stocktech.auth;

import com.hivemq.extension.sdk.api.annotations.NotNull;
import com.hivemq.extension.sdk.api.auth.PublishAuthorizer;
import com.hivemq.extension.sdk.api.auth.parameter.PublishAuthorizerInput;
import com.hivemq.extension.sdk.api.auth.parameter.PublishAuthorizerOutput;
import com.hivemq.extension.sdk.api.packets.disconnect.DisconnectReasonCode;
import com.hivemq.extension.sdk.api.packets.general.UserProperties;
import com.hivemq.extension.sdk.api.packets.publish.PublishPacket;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SimPublishAuthorizer implements PublishAuthorizer {

    private static final Logger log = LoggerFactory.getLogger(SimPublishAuthorizer.class);

	@Override
    public void authorizePublish(@NotNull PublishAuthorizerInput input,
            @NotNull PublishAuthorizerOutput output) {

            final PublishPacket publishPacket = input.getPublishPacket();

            log.info("Topic: " + publishPacket.getTopic());
            if (publishPacket.getTopic().contains("stocktech")) {
                output.authorizeSuccessfully();
                return;
            }

            if (publishPacket.getTopic().startsWith("admin")) {
                output.failAuthorization();
                return;
            }

            final UserProperties userProperties = publishPacket.getUserProperties();

            if (userProperties.getFirst("notallowed").isPresent()) {
                output.disconnectClient(DisconnectReasonCode.ADMINISTRATIVE_ACTION, "User property not allowed");
                return;
            }

            output.nextExtensionOrDefault();
    }
}
