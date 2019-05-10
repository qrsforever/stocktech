/// @file StocktechAuthenticatorProvider.java
/// @brief
/// @author QRS
/// @version 1.0.0
/// @date 2019-05-10

package com.hivemq.extensions.stocktech.auth;

import com.hivemq.extension.sdk.api.annotations.NotNull;
import com.hivemq.extension.sdk.api.annotations.Nullable;
import com.hivemq.extension.sdk.api.auth.Authenticator;
import com.hivemq.extension.sdk.api.auth.parameter.AuthenticatorProviderInput;
import com.hivemq.extension.sdk.api.services.auth.provider.AuthenticatorProvider;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FileAuthenticatorProvider implements AuthenticatorProvider {

    private static final @NotNull Logger log = LoggerFactory.getLogger(FileAuthenticatorProvider.class);
    private final @NotNull FileAuthenticator authenticator;

    public FileAuthenticatorProvider(String resourceDir) {
        this.authenticator = new FileAuthenticator(resourceDir);
    }

    @Override
    public @Nullable Authenticator getAuthenticator(@NotNull final
            AuthenticatorProviderInput input) {
        // Always return the same authenticator, because it is thread-safe and can be
        // shared between multiple clients
        return authenticator;
    }
}
