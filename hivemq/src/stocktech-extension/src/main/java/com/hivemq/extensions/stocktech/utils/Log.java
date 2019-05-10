/// @file Log.java
/// @brief
/// @author QRS
/// @blog qrsforever.github.io
/// @version 1.0
/// @date 2019-05-10 18:35:18

package com.hivemq.extensions.stocktech.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Log {

    private static Log instance = null;
    private static final Logger _log = LoggerFactory.getLogger("Stocktech");

    Log() {
    }

    public static Log getLogger() {
        if (instance  == null)
            instance  = new Log();
        return instance ;
    }

    public void info(String txt) {
        _log.info(txt);
    }

    public void warn(String txt) {
        _log.warn(txt);
    }

    public void error(String txt) {
        _log.error(txt);
    }

    public void info(String txt, Exception e) {
        _log.info(txt, e);
    }

    public void warn(String txt, Exception e) {
        _log.warn(txt, e);
    }

    public void error(String txt, Exception e) {
        _log.error(txt, e);
    }
}
