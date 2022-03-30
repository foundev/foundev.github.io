---
layout: post
date: 2019-12-27 09:30:00 -6000
tags: [ cassandra, java, debugging ]
---
<h1>"Snakeyaml error handling is tough"</h1>

Cassandra for years has relied on snakeyaml to parse configuration files, and it does a fine job, really not a lot of complaints. Until one day a colleague of mine discovered an issue where a permission issue incorrectly reported as an invalid yaml file (complete with the supposedly offending key). Digging into the source code and trying to match up the message. I found that [we were handling YAMLException](https://github.com/apache/cassandra/blob/06209037ea56b5a2a49615a99f1542d6ea1b2947/src/java/org/apache/cassandra/config/YamlConfigurationLoader.java#L128)

```java
        Yaml yaml = new Yaml(constructor);
        Config result = loadConfig(yaml, configBytes);
        propertiesChecker.check();
        return result;
}
catch (YAMLException e)
{
        throw new ConfigurationException("Invalid yaml: " + url + SystemUtils.LINE_SEPARATOR
                                             +  " Error: " + e.getMessage(), false);
}
```

Which is effectively calling [loadAs from snakeyaml](https://github.com/apache/cassandra/blob/06209037ea56b5a2a49615a99f1542d6ea1b2947/src/java/org/apache/cassandra/config/YamlConfigurationLoader.java#L175)

```java
private Config loadConfig(Yaml yaml, byte[] configBytes)
{
        Config config = yaml.loadAs(new ByteArrayInputStream(configBytes), Config.class);
        // If the configuration file is empty yaml will return null. In this case we should use the default
        // configuration to avoid hitting a NPE at a later stage.
        return config == null ? new Config() : config;
}

```

So for this particular version I hunted down the release of snakeyaml as 1.12 and digging into the source I find load as uses StreamReader to wrap the stream passed into [loadAs](https://bitbucket.org/asomov/snakeyaml/src/9febf8df6d2bd9d772cf772f259f1a14860ef639/src/main/java/org/yaml/snakeyaml/Yaml.java#lines-438)

```java

@SuppressWarnings("unchecked")
public <T> T loadAs(Reader io, Class<T> type) {
    return (T) loadFromReader(new StreamReader(io), type);
}
```

A new StreamReader is called, which in the source calls [this.update](https://bitbucket.org/asomov/snakeyaml/src/68503888e285620fa77bb036ae27dc3d5abe6bf2/src/main/java/org/yaml/snakeyaml/reader/StreamReader.java#lines-60)

```java
public StreamReader(Reader reader) {
        this.name = "'reader'";
        this.buffer = "";
        this.stream = reader;
        this.eof = false;
        this.data = new char[1024];
        this.update();
}
```

Unfortunately, "this.update" handles IOException by throwing a [new YAMLException](https://bitbucket.org/asomov/snakeyaml/src/68503888e285620fa77bb036ae27dc3d5abe6bf2/src/main/java/org/yaml/snakeyaml/reader/StreamReader.java#lines-199). So this is how we turn a permission error into an invalid YAML

```java
} catch (IOException ioe) {
        throw new YAMLException(ioe);
}
```

## Conclusion

Just watch out for invalid yaml errors when using Cassandra (or anything consuming snakeyaml) it may not actually be what you think it is.
