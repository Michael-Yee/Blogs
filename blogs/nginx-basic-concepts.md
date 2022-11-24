---
title: Nginx: Basic Concepts
author: Michael Yee
published: True
---


# Nginx

In this blog, I will provide the reader a basic introduction to nginx and describes some simple tasks that can be done with it.

# Let's go!

## What is nginx

NGINX is open source software for web serving, reverse proxying, caching, load balancing, media streaming, and more. 

## Base commands

Base commands

To start nginx, simply type:

```$ nginx```

While your nginx instance is running, you can manage it by sending signals:

```$ nginx -s signal```

Available signals:

- stop: fast shutdown
- quit: graceful shutdown (wait for workers to finish their processes)
- reload: reload the configuration file
- reopen: reopen the log files

## Directive and Context

Depending on the Linux distributions, the nginx configuration file can be found in the following paths:

- /etc/nginx/nginx.conf
- /usr/local/etc/nginx/nginx.conf
- /usr/local/nginx/conf/nginx.conf


This file consists of:

- directive: an option that consists of name and parameters

```gzip on;```

- context: the section where you can declare directives 

```
worker_processes 2; # directive in global context

http {              # http context
    gzip on;        # directive in http context

  server {          # server context
    listen 80;      # directive in server context
  }
}
```

## Directive types

You have to pay attention when using the same directive in multiple contexts, as the inheritance model differs for different directives. There are 3 types of directives, each with its own inheritance model.

### Normal

Has one value per context. Also, it can be defined only once in the context. Subcontexts can override the parent directive, but this override will be valid only in a given subcontext.

```
gzip on;
gzip off; # illegal to have 2 normal directives in same context

server {
  location /downloads {
    gzip off;
  }

  location /assets {
    # gzip is in here
  }
}
```

### Array

Adding multiple directives in the same context will add to the values instead of overwriting them altogether. Defining a directive in a subcontext will override ALL parent values in the given subcontext.

```
error_log /var/log/nginx/error.log;
error_log /var/log/nginx/error_notive.log notice;
error_log /var/log/nginx/error_debug.log debug;

server {
  location /downloads {
    # this will override all the parent directives
    error_log /var/log/nginx/error_downloads.log;
  }
}
```

### Action directive

Actions are directives that change things. Their inheritance behaviour will depend on the module.

For example, in the case of the rewrite directive, every matching directive will be executed:

```
server {
  rewrite ^ /foobar;

  location /foobar {
    rewrite ^ /foo;
    rewrite ^ /bar;
  }
}
```

If the user tries to fetch /sample:

- a server rewrite is executed, rewriting from /sample, to /foobar
- the location /foobar is matched
- the first location rewrite is executed, rewriting from /foobar, to /foo
- the second location rewrite is executed, rewriting from /foo, to /bar

This is a different behaviour than what the return directive provides:

```
server {
  location / {
    return 200;
    return 404;
  }
}
```
In the case above, the 200 status is returned immediately.

## Processing requests

Inside nginx, you can specify multiple virtual servers, each described by a server { } context.
```
server {
  listen      *:80 default_server;
  server_name netguru.co;

  return 200 "Hello from netguru.co";
}

server {
  listen      *:80;
  server_name foo.co;

  return 200 "Hello from foo.co";
}

server {
  listen      *:81;
  server_name bar.co;

  return 200 "Hello from bar.co";
}
```

This will give nginx some insight on how to handle incoming requests. Nginx will first check the listen directive to test which virtual server is listening on the given IP:port combination. Then, the value from server_name directive is tested against the Host header, which stores the domain name of the server.

Nginx will choose the virtual server in the following order:

- Server listing on IP:port, with a matching server_name directive;
- Server listing on IP:port, with the default_server flag;
- Server listing on IP:port, first one defined;
- If there are no matches, refuse the connection.

In the example above, this will mean:

```
Request to foo.co:80     => "Hello from foo.co"
Request to www.foo.co:80 => "Hello from netguru.co"
Request to bar.co:80     => "Hello from netguru.co"
Request to bar.co:81     => "Hello from bar.co"
Request to foo.co:81     => "Hello from bar.co"
```

## server_name directive

The server_name directive accepts multiple values. It also handles wildcard matching and regular expressions.

```
server_name netguru.co www.netguru.co; # exact match
server_name *.netguru.co;              # wildcard matching
server_name netguru.*;                 # wildcard matching
server_name  ~^[0-9]*\.netguru\.co$;   # regexp matching
```

When there is ambiguity, nginx uses the following order:

- Exact name;
- Longest wildcard name starting with an asterisk, e.g. “*.example.org”;- 
Longest wildcard name ending with an asterisk, e.g. “mail.*”;
- First matching regular expression (in the order of appearance in the configuration file).

Nginx will store 3 hash tables: exact names, wildcards starting with an asterisk, and wildcards ending with an asterisk. If the result is not in any of the tables, the regular expressions will be tested sequentially.

It is worth keeping in mind that

```server_name .netguru.co;```

is an abbreviation of:

```server_name  netguru.co  www.netguru.co  *.netguru.co;```

With one difference: .netguru.co is stored in the second table, which means that it is a bit slower than an explicit declaration.
















# Conclusion


---

## Appendix One: Installation instructions

Before you install nginx for the first time on a new machine, you need to set up the nginx packages repository. Afterward, you can install and update nginx from the repository.

RHEL/CentOS

Install the prerequisites:

```$ sudo yum install yum-utils```

To set up the yum repository, create the file named /etc/yum.repos.d/nginx.repo with the following contents:

```
[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true

[nginx-mainline]
name=nginx mainline repo
baseurl=http://nginx.org/packages/mainline/centos/$releasever/$basearch/
gpgcheck=1
enabled=0
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true
```

By default, the repository for stable nginx packages is used. If you would like to use mainline nginx packages, run the following command:

```$ sudo yum-config-manager --enable nginx-mainline```

To install nginx, run the following command:

```$ sudo yum install nginx```

When prompted to accept the GPG key, verify that the fingerprint matches 573B FD6B 3D8F BC64 1079 A6AB ABF5 BD82 7BD9 BF62, and if so, accept it.

AWS Linux AMI 2

```
$ sudo amazon-linux-extras list | grep nginx
 38  nginx1=latest            disabled      [ =stable ]

$ sudo amazon-linux-extras enable nginx1
 38  nginx1=latest            enabled      [ =stable ]
        
Now you can install:
$ sudo yum clean metadata
$ sudo yum -y install nginx
    
$ nginx -v
nginx version: nginx/1.16.1
```

Run Kibana with systemdedit
To configure Kibana to start automatically when the system boots up, run the following commands:

```
$ sudo /bin/systemctl daemon-reload 
$ sudo /bin/systemctl enable nginx.service
$ sudo systemctl start nginx.service
```
