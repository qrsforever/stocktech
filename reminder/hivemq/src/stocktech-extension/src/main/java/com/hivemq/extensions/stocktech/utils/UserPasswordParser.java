/// @file UserPasswordParser.java
/// @brief
/// @author QRS
/// @blog qrsforever.github.io
/// @version 1.0
/// @date 2019-05-13 13:50:38

package com.hivemq.extensions.stocktech.utils;

import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;

import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

import java.util.Map;
import java.util.HashMap;
import java.io.File;

public class UserPasswordParser {

    public class UserInfo {
        public String clientId;
        public String name;
        public String password;
    }

    private Map<String, UserInfo> users;

    public UserPasswordParser(String xmlfile) {
		SAXParserFactory factory = SAXParserFactory.newInstance();
		try {
			SAXParser parser = factory.newSAXParser();
			parser.parse(new File(xmlfile), new QHandler());
		} catch (Exception e) {
			e.printStackTrace();
		}
    }

    public final UserInfo getUserInfo(final String name) {
        return users.get(name);
    }

    class QHandler extends DefaultHandler {

        private String tag;
        private UserInfo user;

        @Override
        public void startDocument() throws SAXException {
            users = new HashMap<String, UserInfo>();
        }

        @Override
        public void startElement(String uri, String localName, String qName,
                Attributes attributes) throws SAXException {
            if (null == qName)
                return;
            tag = qName;

            if (qName.equals("user")) {
                user = new UserInfo();
                user.clientId = attributes.getValue("clientid");
            }
        }

        @Override
        public void characters(char[] ch, int start, int length) throws SAXException {
            String str = new String(ch, start, length);
            str = str.trim();
            if (str.length() == 0 || null == tag || null == user)
                return;

            switch (tag) {
                case "name":
                    user.name = str;
                    break;
                case "password":
                    user.password = str;
                    break;
                default:
                    ;
            }
        }

        @Override
        public void endElement(String uri, String localName, String qName)
            throws SAXException {
            if (qName.equals("user") && null != user) {
                users.put(user.clientId, user);
                user = null;
            }
            tag = null;
        }

        @Override
        public void endDocument() throws SAXException {
            for (Map.Entry<String, UserInfo> each : users.entrySet()) {
                UserInfo info = each.getValue();
                System.out.println("ClientId: " + info.clientId +
                        ", Username: " + info.name + ", Password: " + info.password);
            }
        }
    }
}
