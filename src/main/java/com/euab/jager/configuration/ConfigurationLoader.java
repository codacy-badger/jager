package com.euab.jager.configuration;

import com.google.gson.Gson;

import java.io.*;
import java.lang.reflect.Type;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;

public class ConfigurationLoader implements ConfigurationInterface {

    @Override
    public ConfigurationCastableInterface loadConfiguration(String fileName, Class<?> type) throws IOException {
        File file = new File(fileName);
        if (!file.exists()) {
            try {
                file.createNewFile();

                FileWriter fw = new FileWriter(file.getAbsoluteFile());
                BufferedWriter buf = new BufferedWriter(fw);
                buf.write(this.defaultConfiguration(fileName));
                buf.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

        if (!(file.canRead() || file.canWrite())) {
            System.out.printf("%s config file cannot be read or written to.", fileName);
            System.exit(0);
        }

        try (BufferedReader buf = new BufferedReader(new FileReader(file.getAbsoluteFile()))) {
            StringBuilder stringBuilder = new StringBuilder();
            String line = buf.readLine();

            while (line != null) {
                stringBuilder.append(line);
                stringBuilder.append(System.lineSeparator());
                line = buf.readLine();
            }

            return (ConfigurationCastableInterface) new Gson().fromJson(stringBuilder.toString(), (Type) type);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return null;
    }

    @Override
    public String defaultConfiguration(String name) {
        InputStream stream = getClass().getClassLoader().getResourceAsStream(name);
        StringBuilder textBuilder = new StringBuilder();

        try (Reader buf = new BufferedReader(new InputStreamReader(stream, Charset.forName(StandardCharsets
                .UTF_8.name())))) {
            int read;
            while ((read = buf.read()) != -1) {
                textBuilder.append((char) read);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return textBuilder.toString();
    }
}
