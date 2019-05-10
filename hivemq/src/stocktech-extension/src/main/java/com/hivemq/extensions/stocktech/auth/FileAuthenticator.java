/// @file StocktechAuthenticator.java
/// @brief
/// @author QRS
/// @version 1.0.0
/// @date 2019-05-10

package com.hivemq.extensions.stocktech.auth;

import com.hivemq.extension.sdk.api.annotations.NotNull;
import com.hivemq.extension.sdk.api.auth.SimpleAuthenticator;
import com.hivemq.extension.sdk.api.auth.parameter.SimpleAuthInput;
import com.hivemq.extension.sdk.api.auth.parameter.SimpleAuthOutput;
import com.hivemq.extension.sdk.api.auth.parameter.TopicPermission;
import com.hivemq.extension.sdk.api.packets.auth.ModifiableDefaultPermissions;
import com.hivemq.extension.sdk.api.packets.connect.ConnackReasonCode;
import com.hivemq.extension.sdk.api.packets.connect.ConnectPacket;

import com.hivemq.extension.sdk.api.services.builder.Builders;

import java.nio.charset.Charset; 

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FileAuthenticator implements SimpleAuthenticator {

    private static final @NotNull Logger log = LoggerFactory.getLogger(FileAuthenticator.class);

    private final String[] topics = {
        "/stocktech/tapereading/up",
        "/stocktech/tapereading/down",
    };

    FileAuthenticator(@NotNull String resourceDir) {
    }

    @Override
    public void onConnect(@NotNull final SimpleAuthInput input, 
            @NotNull final SimpleAuthOutput output) {

        ConnectPacket connect = input.getConnectPacket();

        if (!connect.getUserName().isPresent() || !connect.getPassword().isPresent()) {
            output.failAuthentication(ConnackReasonCode.BAD_USER_NAME_OR_PASSWORD,
                    "Authentication failed because userNameOptional or passwordOptional are missing");
        }
        String username = connect.getUserName().get();
        String password = Charset.forName("UTF-8").decode(connect.getPassword().get()).toString();
        String clientId = input.getClientInformation().getClientId();

        log.info("onConnect(" + username + ", " + password + ", " + clientId + ")");

        if (clientId.contains("#") || clientId.contains("+")) {
            output.failAuthentication(ConnackReasonCode.CLIENT_IDENTIFIER_NOT_VALID,
                    "'#' and '+' are not allowed in the clientidentifier");
            return;
        }

        if (username.contains("#") || username .contains("+")) {
            output.failAuthentication(ConnackReasonCode.BAD_USER_NAME_OR_PASSWORD,
                    "'#' and '+' are not allowed in the userNameOptional");
            return;
        }

        // TODO need check using urers.xml
        if (!username.equals("stocktech") || !password.equals("stocktech")) {
            output.failAuthentication(ConnackReasonCode.BAD_USER_NAME_OR_PASSWORD,
                    "username or password error");
        }

        final ModifiableDefaultPermissions defaultPermissions = output.getDefaultPermissions();
        for (String each : topics) {
            TopicPermission permission = Builders.topicPermission()
                .topicFilter(clientId + each)
                .qos(TopicPermission.Qos.ALL)
                .activity(TopicPermission.MqttActivity.ALL)
                .type(TopicPermission.PermissionType.ALLOW)
                .retain(TopicPermission.Retain.ALL)
                .build();
            defaultPermissions.add(permission);
        }
        log.info("onConnect sucessfully!");
        output.authenticateSuccessfully();
    }
}
