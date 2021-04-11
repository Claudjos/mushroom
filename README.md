# mushroom

### About
Network sniffer collecting data about incoming TCP SYN messages. Data can then be used to identify clients' OS, device and connection type. Comparing data with client provided information (like HTTP user-agent) can help identify fraud visits, proxies, traffic reviewer, etc..

### Start sniffer
```
$ sudo python3 -m mushroom 80,443
Collecting SYN data for ports: 80, 443
SET syn 192.168.0.1:59796 {'ttl': 64, 'synsize': 60, 'winsize': 65495}
```

### Retrieve collected data
```
>>> from mushroom.client import Client
>>> c = Client()
>>> c.get_syn_data("192.168.0.1", 59796)
{'ttl': 64, 'synsize': 60, 'winsize': 65495}
```

### Some values to start..
SYN data change based on device, OS version and connection type (e.g., WiFi, 2G, 4G).
To correctly identify traffic you'll need to build a table. This might help you getting started.

|Device|TTL|SYNSize|WinSize|
|-|-|-|-|
|Android|64|60|65535|
|Android 4|64|60|14600|
|iOS|64|64|65535|
|Win|128|64|65535|
|Win10|128|52|64240|
|Android 6 Huawei Nova Young 4G LTE|64|60|43520|
|Android Huawei|64|60|12240|
|Android 2G Edge|64|60|18980|
|Android 6 2G Edge|64|60|42340|
|Android 9 2G Edge|64|60|13140|
|Ubuntu|64|60|29200|
