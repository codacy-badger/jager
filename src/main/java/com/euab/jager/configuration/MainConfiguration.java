package com.euab.jager.configuration;

import java.util.ArrayList;

public class MainConfiguration {

    private String environment;
    private BotAuth bot;
    private Database database;
    private ArrayList<String> playing;
    private ArrayList<String> botAccess;
    private Webhook webhook;
    private APIKeys apiKeys;

    public class BotAuth {
        private String token;
        private String oauth;
        private int activationDelay;

        public String getToken() {
            return token;
        }

        public String getOauth() {
            return oauth;
        }

        public int getActivationDelay() {
            return activationDelay;
        }
    }

    private BotAuth botAuth() {
        return bot;
    }

    public class Database {
        private String type;
        private String database;
        private String hostname;
        private String username;
        private String password;

        public String getType() {
            return type;
        }

        public String getDatabase() {
            return database;
        }

        public String getHostname() {
            return hostname;
        }

        public String getUsername() {
            return username;
        }

        public String getPassword() {
            return password;
        }
    }

    public class Webhook {
        private String id;
        private String token;

        public String getId() {
            return id;
        }

        public String token() {
            return token;
        }
    }

    public class APIKeys {
        private String googleKey;

        public String getGoogleKey() {
            return googleKey;
        }
    }
}
