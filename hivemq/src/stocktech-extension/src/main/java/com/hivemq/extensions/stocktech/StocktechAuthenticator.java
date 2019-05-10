/// @file StocktechAuthenticator.java
/// @brief
/// @author QRS
/// @version 1.0.0
/// @date 2019-05-10

package com.hivemq.extensions.stocktech;

import com.hivemq.extension.sdk.api.annotations.NotNull;
import com.hivemq.extension.sdk.api.auth.SimpleAuthenticator;
import com.hivemq.extension.sdk.api.auth.parameter.SimpleAuthInput;
import com.hivemq.extension.sdk.api.auth.parameter.SimpleAuthOutput;
import com.hivemq.extension.sdk.api.packets.connect.ConnackReasonCode;

import java.nio.ByteBuffer;
import java.util.Optional;

import java.util.List;
import java.util.Map;
import java.util.HashMap;

import org.dom4j.*;
import org.dom4j.io.SAXReader;

// import com.mongodb.MongoClient;
// import com.mongodb.client.MongoDatabase;

import com.hivemq.extensions.stocktech.utils.Log;

public class StocktechAuthenticator implements SimpleAuthenticator {

    private static final @NotNull Log log = Log.getLogger();

    private final Map<String, String> usernamePasswordMap = new HashMap<>();

    StocktechAuthenticator(@NotNull String file) {
       //  try {
       //      ;
       //     //  SAXReader reader = new SAXReader();
       //     //  Document document = reader.read(file);
       //     //  Element root = document.getRootElement();
       //     //  @SuppressWarnings("unchecked")
       //     //  List<Element> list = root.elements();
       //     //  for (Element e : list) {
       //     //      String name = e.element("name").getTextTrim();
       //     //      String pass = e.element("password").getTextTrim();
       //     //      log.info("name = " + name + " , pass = " + pass);
       //     //      usernamePasswordMap.put(name, pass);
       //     //  }
       //  } catch (DocumentException e) {
       //      log.error("Exception: ", e);
       //  }
        // MongoClient mongoClient = new MongoClient( "localhost" , 27017 );
        // MongoDatabase mongoDatabase = mongoClient.getDatabase("mycol");
    }

    @Override
    public void onConnect(@NotNull final SimpleAuthInput input,
            @NotNull final SimpleAuthOutput output) {

        final Optional<String> userNameOptional = input.getConnectPacket().getUserName();
        final Optional<ByteBuffer> passwordOptional = input.getConnectPacket().getPassword();
        final String clientId = input.getClientInformation().getClientId();

        if (!userNameOptional.isPresent() || !passwordOptional.isPresent()) {
            output.failAuthentication(ConnackReasonCode.BAD_USER_NAME_OR_PASSWORD,
                    "Authentication failed because userNameOptional or passwordOptional are missing");
            return;
        }

        final String username = userNameOptional.get();

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

    }

}
