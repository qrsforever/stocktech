/// @file StocktechMain.java
/// @brief
/// @author QRS
/// @blog qrsforever.github.io
/// @version 1.0
/// @date 2019-05-10 18:35:45

package com.hivemq.extensions.stocktech;

import com.hivemq.extension.sdk.api.ExtensionMain;
import com.hivemq.extension.sdk.api.annotations.NotNull;
import com.hivemq.extension.sdk.api.parameter.*;
import com.hivemq.extension.sdk.api.services.Services;

import java.io.File;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.hivemq.extensions.stocktech.auth.FileAuthenticator;
import com.hivemq.extensions.stocktech.auth.FileAuthenticatorProvider;
import com.hivemq.extensions.stocktech.events.ClientEventListener;

public class StocktechMain implements ExtensionMain {

    private static final @NotNull Logger log = LoggerFactory.getLogger(StocktechMain.class);

    @Override
    public void extensionStart(final @NotNull ExtensionStartInput input,
            final @NotNull ExtensionStartOutput output) {

        try {
            final ExtensionInformation info = input.getExtensionInformation();
            log.info("Started " + info.getName() + ":" + info.getVersion());
            final File fhome = info.getExtensionHomeFolder();
            log.info("HomeFolder: " + fhome);

            Services.eventRegistry().setClientLifecycleEventListener(
                    args->new ClientEventListener());

            Services.securityRegistry().setAuthenticatorProvider(
                    new FileAuthenticatorProvider(fhome.getPath()));

        } catch (Exception e) {
            log.error("Exception thrown at extension start: ", e);
        }
    }

    @Override
    public void extensionStop(final @NotNull ExtensionStopInput input,
            final @NotNull ExtensionStopOutput output) {

        final ExtensionInformation info = input.getExtensionInformation();
        log.info("Stopped " + info.getName() + ":" + info.getVersion());
    }
}
