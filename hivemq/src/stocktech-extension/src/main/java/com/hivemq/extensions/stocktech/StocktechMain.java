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

import com.hivemq.extensions.stocktech.utils.Log;

import java.io.File;

import java.util.List;
import java.util.Map;
import java.util.HashMap;
import org.dom4j.*;
import org.dom4j.io.SAXReader;
import javax.xml.parsers.SAXParserFactory;
import javax.xml.parsers.SAXParser;

public class StocktechMain implements ExtensionMain {

    private static final @NotNull Log log = Log.getLogger();

    @Override
    public void extensionStart(final @NotNull ExtensionStartInput input,
            final @NotNull ExtensionStartOutput output) {

        try {
            System.setProperty("org.xml.sax.driver","org.apache.xerces.parsers.SAXparser");
            final ExtensionInformation info = input.getExtensionInformation();
            log.info("Started " + info.getName() + ":" + info.getVersion());
            final File fhome = info.getExtensionHomeFolder();
            log.info("HomeFolder: " + fhome);

            Services.eventRegistry().setClientLifecycleEventListener(
                    args->new StocktechEventListener());

            Services.securityRegistry().setAuthenticatorProvider(
                    new StocktechAuthenticatorProvider(fhome.getPath() + "/users.xml"));

            SAXReader reader = new SAXReader();
            // SAXParserFactory factory = SAXParserFactory.newInstance();
            // SAXParser parser = factory.newSAXParser();
            // XMLReader reader = newSAXParser.getXMLReader();
            Document document = reader.read(fhome.getPath() + "/users.xml");
            Element root = document.getRootElement();
            @SuppressWarnings("unchecked")
            List<Element> list = root.elements();

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
