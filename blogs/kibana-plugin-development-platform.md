---
title: Kibana Plugin Development Platform
author: Michael Yee
published: True
---


# Kibana Plugin Development Platform

In this blog, I will explore the  Kibana plugin development platform which was released in version 7.9.

## The Kibana development platform - Goals

The primary goal of the Kibana platform project was to increase both the velocity and stability of adding new features. 
To achieve this goal, the new platform included the following features:

* Consistent architecture across client and server code
* A small and explicit set of foundational APIs that is separate from plugin code
* Simple and well-defined plugin runtime and execution flow
* Isolated plugins with explicit APIs and dependencies
* Framework-agnostic and futureproof APIs
* Full test coverage
* Type safety

## Key aspects of the Kibana platform

### Core

The Kibana core is the root system that boots Kibana, validates configuration, loads plugins, and provides the primitive APIs needed to build a plugin in Kibana. The core is made up of a set of services, each of which provides APIs to plugins at different points of the system’s lifecycle. Core services are always present and cannot be disabled. Anything we consider to be essential to building a Kibana plugin exists as a core service.

The core aims to be framework and technology agnostic.

### Plugins

While the core provides the framework for Kibana, plugins are where the magic happens. Virtually every feature used in Kibana is built inside of a plugin. In general, a plugin is a group of functionalities that can be toggled on or off to provide features and apps in Kibana.

### Lifecycles

All core services and plugins are organized and executed in the same set of lifecycle stages: setup, start, and stop. Both the client and server execute these lifecycle stages sequentially when starting Kibana.

Different sets of functionality are available during each lifecycle stage. It is up to each service and plugin to return the APIs it wishes to expose during these lifecycle stages for other services and plugins to consume.

By organizing all of Kibana around these stages, we make reasoning about when code will execute much simpler and have tight control over which features are available to other components at different points in time.

### Server and browser

In reality, the core consists of a server-side and client-side. Each follows a similar design but is made up of a slightly different set of services.

The server-side services provide typical backend functionality and the client-side services provide frontend functionality. 

## Development Guide (https://www.elastic.co/guide/en/kibana/current/development.html#development)

### Set up the environment for developing Kibana Plugin using AWS Linux 2

1) Update all the things!

```sudo yum update -y```

2) Install complile software

```
sudo yum groupinstall "Development Tools"
```

3) Install git and clone the Kibana repo

```
sudo yum install git -y

git clone https://github.com/elastic/kibana.git

cd kibana
```

Note: Kibana is a big project and for some commands it can happen that the process hits the default heap limit and crashes with an out-of-memory error. If you run into this problem, you can increase maximum heap size by setting the --max_old_space_size option on the command line. To set the limit for all commands, simply add the following line to your shell config: export NODE_OPTIONS="--max_old_space_size=2048".

4) Install Node.js (Install the version of Node.js listed in the .node-version file)

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash

nvm install 14.15.1

nvm use 14.15.1
```

NOTE: 14.15.1 was the current version @ the time of this blog

5) Install Yarn

```npm install yarn -g```


6) Bootstrap Kibana and install all the dependencies (This step could take up to 30 mins to complete depending on you system)

```
yarn kbn bootstrap 
```

NOTE: When switching branches which use different versions of npm packages you may need to run:

```
yarn kbn clean
```

If you have failures during yarn kbn bootstrap you may have some corrupted packages in your yarn cache which you can clean with:

```
yarn cache clean
```

7) Run Elasticsearch

Run the latest Elasticsearch snapshot. Specify an optional license with the --license flag.

```
yarn es snapshot --license trial
```

Check Elasticsearch is running

```
curl -u elastic:changeme localhost:9200
```

8) Run Kibana (This step could take up to 30 mins to complete depending on you system)

a) In another terminal window, perform steps 4, 5 and 6. 

b) In config/kibana.yml, update the server.host

```
server.host: "0.0.0.0"
```

Start Kibana by including developer examples by adding an optional --run-examples flag.

Method 1:

```
yarn start --run-examples
```

Method 2:

```
node scripts/build_kibana_platform_plugins
yarn start --run-examples
```

View all available options by running yarn start --help

Known issues:

1) Elasticsearch - Increase max_map_count Kernel Parameter

Solution:

Add the following line to the end of /etc/sysctl.conf:

```
vm.max_map_count=262144
```

Reload the config as root:

```
sudo sysctl -p
```

2) Kibana - [watcher] fatal error  Error: ENOSPC: System limit for number of file watchers reached, watch '/home/ec2-user/repos/kibana/src/plugins/console/server/routes/api/console/proxy/create_handler.ts'


Solution: Modify max_user_watches

Add the following lione to the end of this file `/etc/sysctl.conf`

```
fs.inotify.max_user_watches=524288
```
