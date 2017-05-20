Sangoma Vega Integration for Datadog
===================

DataDog Agent plugin for the Sangoma Vega Hardware.

Prerequisites
-----------
- Datadog

Installation
-----------

Get the module files for the datadog agent.

```
cd /usr/src/
wget https://github.com/mafairnet/datadog-svega/archive/master.zip
unzip master.zip
cd datadog-svega/
```

Copy the module files to the datadog directories.

```
cp -R checks.d/svega.py /opt/datadog-agent/agent/checks.d/
cp -R conf.d/svega.yaml /etc/dd-agent/conf.d/
```

Edit the configuration file for the module.

```
nano /etc/dd-agent/conf.d/svega.yaml
```

Insert the IP, Name, User and Password for the Vega.

```
init_config:
	instances:
		- host: 0.0.0.0         #vega adress
          name: vega_name       #vega name
          user: user            #vega user
          secret: pass          #vega user pass
```

Restart  the datadog service.

```
/etc/init.d/datadog-agent restart
```

Check the datadog service status.

```
/etc/init.d/datadog-agent info
```

The output should be like the next text.

```
    svega
    -----
      - instance #0 [OK]
      - instance #1 [OK]
      - Collected 10 metrics, 0 events & 1 service check

```