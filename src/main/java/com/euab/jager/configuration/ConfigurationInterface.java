package com.euab.jager.configuration;

import java.io.IOException;

public interface ConfigurationInterface {

    ConfigurationCastableInterface loadConfiguration(String fileName, Class<?> type) throws IOException;

    String defaultConfiguration(String name);
}
