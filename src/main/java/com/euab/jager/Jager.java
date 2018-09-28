package com.euab.jager;

import com.euab.jager.configuration.ConfigurationLoader;
import com.euab.jager.configuration.MainConfiguration;

import java.io.IOException;

public class Jager {

    public final MainConfiguration configuration;

    public Jager() throws IOException {
        ConfigurationLoader configurationLoader = new ConfigurationLoader();
        this.configuration = (MainConfiguration) configurationLoader.loadConfiguration("config.json",
                MainConfiguration.class);

        if (this.configuration == null) {
            System.out.println("Something went wrong whilst trying to load configuration. Exiting program. :(");
            System.exit(0);
        }
    }
}
