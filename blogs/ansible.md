---
title: The fundamentals of Ansible
author: Michael Yee
published: True
---


# Overview

In this blog, I will describe some of the fundamentals concepts of Ansible.  
NOTE: This blog assume the reader has an understanding of the Jinja2 and YAML.

## Installation

Download instructions can be found [here](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html). To verify that ansible installed properly, run the following command:

	ansible --version

## Background

Ansible is simple open source IT engine which automates application deployment, cloud provisioning, configuration management, intra service orchestration and many other IT tools.

Ansible is easy to deploy because it uses no agents (Ansible management node connects to each nodes through ssh, Ansible pushes the desired state of the system in small programs called as “Ansible Modules”. Ansible runs these modules on your nodes and removes them when finished.) and no additional custom security infrastructure.

Ansible is designed for multi-tier deployment. Ansible does not manage one system at time, but rather models IT infrastructure by describing all of your systems are interrelated.

Ansible uses playbook to describe automation jobs written in a very simple and human readble language called YAML. 

## Environment Setup

Two "types of machines" are exist in a deployment control machine and remote machine(s).

The control machine manages other machine(s). Python 2.7 or higher and Ansible must be install on the control machine. 
    
The remote machine(s) are managed by control machine.

## Inventory

Ansible works against multiple systems in your infrastructure at the same time. It does this by selecting portions of systems listed in Ansible’s inventory,
which defaults to being saved in the location /etc/ansible/hosts. However, you can configure ansible to look somewhere else, use an environment variable (ANSIBLE_HOSTS) or use the -i flag in ansible commands and provide the inventory path. 

Example inventory file:

```
host0.example.org ansible_host=172.18.0.2 ansible_user=root
host1.example.org ansible_host=172.18.0.3 ansible_user=root
host2.example.org ansible_host=172.18.0.4 ansible_user=root

ansible_host is a special variable that sets the IP ansible will use when trying to connect to this host. 

ansible_user is another special variable that tells ansible to connect as this user when using ssh. By default ansible would use your current username, or use another default provided in ~/.ansible.cfg (remote_user).
```

To verify ansible can communicate with these hosts, run the following command:

    ansible -i hosts -m ping all

Output:

```
host0.example.org | SUCCESS => {
    "changed": false, 
    "failed": false, 
    "ping": "pong"
}
host2.example.org | SUCCESS => {
    "changed": false, 
    "failed": false, 
    "ping": "pong"
}
host1.example.org | SUCCESS => {
    "changed": false, 
    "failed": false, 
    "ping": "pong"
}
```

## Ad-Hoc Commands

An ad-hoc command is something that you might type in to do something really quick, but don’t want to save for later. In the inventory section, I introduced the ping module which take no arguments.  Modules that take arguements are passed via -a switch.  Some other useful modules are as follows:

### Copy

This module lets you copy a file from the controlling machine to the node. Lets say we want to copy our /etc/motd to /tmp of our target node, host0.example.org. Please run the following command: 

    ansible -i hosts -m copy -a 'src=/etc/motd dest=/tmp/' host0.example.org 

Output:

```
host0.example.org | SUCCESS => {
    "changed": true, 
    "checksum": "31a50737f45fdf62dfebb3b0aead415d053bbac1", 
    "dest": "/tmp/motd", 
    "failed": false, 
    "gid": 0, 
    "group": "root", 
    "md5sum": "00f982257d17daa03ad2fb1f2c53dc5f", 
    "mode": "0644", 
    "owner": "root", 
    "size": 282, 
    "src": "/root/.ansible/tmp/ansible-tmp-1542228181.71-39039961665543/source", 
    "state": "file", 
    "uid": 0
}

```

### Shell

This module lets you execute a shell command on the remote host.  For example, say we wanted to do a foldering listing on host0.example.org, run the following command:

    ansible -i hosts -m shell -a 'ls' host0.example.org 

### Setup

This module gathers all the information about a node.

    ansible -i hosts -m setup host0.example.org 

The output is in JSON format and contains a bunch of information about the host.

Say you only wanted something specific like ansible_memtotal_mb, you would run the following command:

    ansible -i hosts -m setup -a 'filter=ansible_memtotal_*' all
    NOTE: You can use * in the filter = expression to act like a wildcard(s)

### Many host

In the examples in this section, we have directed commands to one host, but how do we broadcast to all hosts?  The folloiwing command will gather and display all the versions of Ubuntu that are deployed on each system:

    ansible -i hosts -m shell -a 'grep DISTRIB_RELEASE /etc/lsb-release' all 
    NOTE: all is a shortcut meaning all hosts found in inventory file

Output:

```
host2.example.org | SUCCESS | rc=0 >>
DISTRIB_RELEASE=16.04

host1.example.org | SUCCESS | rc=0 >>
DISTRIB_RELEASE=16.04

host0.example.org | SUCCESS | rc=0 >>
DISTRIB_RELEASE=16.04
```

## Groups and variables

### Grouping hosts 

Hosts in inventory can be arbitrarily grouped. For instance, you could have a Selenium grid group, 

     [selenium_grid]
     host0.example.org
     host1.example.org
     host2.example.org
    
If you wish to use child groups, just define a [groupname:children] and add child groups in it. For instance, we could organize our selenium grid inventory like the following: 

     [selenium_hub]
     host0.example.org
     
     [selenium_node]
     host1.example.org
     host2.example.org
     
     [selenium_grid:children]
     selenium_hub
     selenium_node

Grouping of course, leverages configuration mutualization. 

### Setting variables 

You can assign variables to hosts in several places: inventory file, host vars files, group vars files, etc... 

One helpful example of assigning variables the ansible_host (IP address for the host), ansible_port (ssh port ansible will try to connect) and ansible_user (user name on host) in the inventory file, comes when Ansible tries to resolves hosts' name when it attempts to connect via SSH. But when you're bootstrapping a host, it might not have its definitive ip address yet. 

     [selenium_hub]
     host0.example.org ansible_host=192.168.0.12 ansible_port=2222 ansible_user=root

Ansible will look for variables definitions in group and host variable files. These files will be searched in directories group_vars and host_vars, below the directory where the main inventory file is located. 

The files will be searched by name. For instance, using the previously mentioned inventory file, host0.example.org variables will be searched in those files: 

     - group_vars/selenium_grid
     - group_vars/selenium_hub
     - host_vars/host0.example.org

It doesn't matter if those files do not exist, but if they do, ansible will use them. 

NOTE: When using ansible-playbook command (not the regular Ansible command), variables can also be set with --extra-vars (or -e) command line switch. 

## Playbooks

Playbooks are Ansible’s configuration, deployment, and orchestration language. Playbooks are files written in YAML where Ansible code is written. Playbooks are a series of ansible commands (tasks), like the ones we used with the ansible CLI tool. These tasks are targeted at a specific set of hosts/groups.

### Apache example - Start here

For this example, create two files with the following file names and content as follows:

apache.yml:

    - hosts: web
      tasks:
        - name: Installs apache web server
          apt: pkg=apache2 state=installed update_cache=true


hosts:

    [web]
    host1.example.org

Files and folders structure:

```
├── apache.yml
├── hosts 
```

We just need to say what we want to do using the right ansible modules. Here, we're using the apt module to install debian packages and update the package cache. 

We also added a name for this task. While this is not necessary, it's very informative when the playbook runs, so it's highly recommended. 

We will now continue with the command below. Here, hosts is the inventory file, -l limits the run only to host1.example.org and apache.yml is our playbook.

Run the playbook with the following command:  

    ansible-playbook -i hosts -l host1.example.org apache.yml 

Output:

```
PLAY [web] *********************

TASK [Gathering Facts] *********************
ok: [host1.example.org]

TASK [Installs apache web server] *********************
changed: [host1.example.org]

PLAY RECAP *********************
host1.example.org          : ok=2    changed=1    unreachable=0    failed=0   
```

Output analysis:

    PLAY [web] ********************* 
 
Ansible tells us it's running the play on hosts web. A play is a suite of ansible instructions related to a host. If we'd have another play (-host: blah) line in our playbook, it would show up too, but after the first play has completed. 

     TASK [Gathering Facts] ********************* 
     ok: [host1.example.org]
     

Remember when we used the setup module? Before each play, ansible runs it on necessary hosts to gather facts. If this is not required because you don't need any info from the host, you can just add gather_facts: no below the host entry (same level as tasks:). 

     TASK: [Installs apache web server] ********************* 
     changed: [host1.example.org]
     

Next, our only task is executed and because it says changed, we know that it changed something on host1.example.org. 

     PLAY RECAP ********************* 
     host1.example.org              : ok=2    changed=1    unreachable=0    failed=0 
     

Finally, ansible outputs a recap of what happened: two tasks have been executed and one of them changed something on the host: setup module (doesn't change anything) and the apache task). 

 Now let's try to run it again and see what happens: 

    ansible-playbook -i hosts -l host1.example.org apache.yml 

Output: 

```
PLAY [web] *********************

TASK [Gathering Facts] *********************
ok: [host1.example.org]

TASK [Installs apache web server] *********************
ok: [host1.example.org]

PLAY RECAP *********************
host1.example.org          : ok=2    changed=0    unreachable=0    failed=0   
```

Note the changed field, it is now 0, which is absolutely normal and is one of the core feature of ansible: the playbook will act only if there is something to do. It's called idempotency, and means that you can run your playbook as many times as you want, you will always end up in the same state. 

### Apache example - Pushing files on nodes

To setp up a our virtualhost on our server, we will have to remove the default virtualhost, send our virtualhost, activate it and restart apache. 

Created a folder called files. 
Within the folder call files, create the following file name and virtualhost configuration content as follows:

awesome-app:

```
<VirtualHost *:80>
  DocumentRoot /var/www/awesome-app

  Options -Indexes

  ErrorLog /var/log/apache2/error.log
  TransferLog /var/log/apache2/access.log
</VirtualHost>
```

Update the playbook with the following content:

apache.yml

```
- hosts: web
  tasks:
    - name: Installs apache web server
      apt: pkg=apache2 state=installed update_cache=true

    - name: Push default virtual host configuration
      copy: src=files/awesome-app dest=/etc/apache2/sites-available/awesome-app.conf mode=0640 

    - name: Disable the default virtualhost
      file: dest=/etc/apache2/sites-enabled/000-default.conf state=absent
      notify:
        - restart apache

    - name: Disable the default ssl virtualhost
      file: dest=/etc/apache2/sites-enabled/default-ssl.conf state=absent
      notify:
        - restart apache

    - name: Activates our virtualhost
      file: src=/etc/apache2/sites-available/awesome-app.conf dest=/etc/apache2/sites-enabled/awesome-app.conf state=link
      notify:
        - restart apache
        
  handlers:
    - name: restart apache
      service: name=apache2 state=restarted
```

#### File module

src: path of the file to link to (applies only to *state=link* and *state=hard*). Will accept absolute, relative and nonexisting paths. 

state: If *directory*, all intermediate subdirectories will be created if they do not exist. If *file*, the file will NOT be created if it does not exist. If *link*, the symbolic link will be created or changed. Use *hard* for hardlinks. If *absent*, directories will be recursively deleted, and files or symlinks will be unlinked. Note that *absent* will not cause *file* to fail if the *path* does not exist as the state did not change. If *touch*, an empty file will be created if the path does not exist, while an existing file or directory will receive updated file access and modification times.
  
These ‘notify’ actions are triggered at the end of each block of tasks in a play, and will only be triggered once even if notified by multiple different tasks. For instance, multiple resources may indicate that apache needs to be restarted because they have changed a config file, but apache will only be bounced once to avoid unnecessary restarts. 

Handlers is task(s), not really any different from regular task. They are referenced by a globally unique name and are notified by notifiers. If nothing notifies a handler, it will not run. Regardless of how many tasks notify a handler, it will run only once, after all of the tasks complete in a particular play

Enabling the virtual host within Apache via manually symlinking the config file into /etc/apache2/sites-enabled/.

Files and folders structure:

```
├── apache.yml
├── hosts 
├── files 
│   ├── awesome-app  
```

Run the following command to execute our playbook: 

    ansible-playbook -i hosts -l host1.example.org apache.yml 

Output:

```
PLAY [web] *********************

TASK [Gathering Facts] *********************
ok: [host1.example.org]

TASK [Installs apache web server] *********************
ok: [host1.example.org]

TASK [Push default virtual host configuration] *********************
changed: [host1.example.org]

TASK [Disable the default virtualhost] *********************
changed: [host1.example.org]

TASK [Disable the default ssl virtualhost] *********************
ok: [host1.example.org]

TASK [Activates our virtualhost] *********************
changed: [host1.example.org]

RUNNING HANDLER [restart apache] *********************
changed: [host1.example.org]

PLAY RECAP *********************
host1.example.org          : ok=7    changed=4    unreachable=0    failed=0   

```

### Apache example - Failure

In production, we want to make sure our servers are only restart say if our configuraiton is correct. Ansible has a nifty feature to stop all processes if something goes wrong. We'll take advantage of this feature to stop our playbook if the configuraiton is not valid.

I have altered the awesome-app file with a typo as follows:

awesome-app:

```
<VirtualHost *:80>
  ToortnemucoD /var/www/awesome-app

  Options -Indexes

  ErrorLog /var/log/apache2/error.log
  TransferLog /var/log/apache2/access.log
</VirtualHost>
```

To ensure when a task fails, the processes stops, we will ensure that the configuration is valid before restarting the server. We  also start by adding our virtualhost before removing the default virtualhost, so a subsequent restart (possibly done directly on the server) won't break apache. 

Update the playbook with the following content:

apache.yml

```
- hosts: web
  tasks:
    - name: Installs apache web server
      apt: pkg=apache2 state=installed update_cache=true

    - name: Push future default virtual host configuration
      copy: src=files/awesome-app dest=/etc/apache2/sites-available/awesome-app.conf mode=0640

    - name: Activates our virtualhost
      command: a2ensite awesome-app

    - name: Check that our config is valid
      command: apache2ctl configtest
    
    - name: Deactivates the default virtualhost
      command: a2dissite 000-default

    - name: Deactivates the default ssl virtualhost
      command: a2dissite default-ssl
      notify: 
        - restart apache

  handlers:
    - name: restart apache
      service: name=apache2 state=restarted
```

### Command module

The command module takes the command name followed by a list of space-delimited arguments. The given command will be executed on all selected nodes. It will not be processed through the shell, so variables like $HOME and operations like "<", ">", "|", ";" and "&" will not work (use the shell module if you need these features).

Enabling the virtual host within Apache via a2ensite awesome-app.

Run the following command to execute our playbook: 

    ansible-playbook -i hosts -l host1.example.org apache.yml

Output:

```
PLAY [web] *********************

TASK [Gathering Facts] *********************
ok: [host1.example.org]

TASK [Installs apache web server] *********************
ok: [host1.example.org]

TASK [Push future default virtual host configuration] *********************
changed: [host1.example.org]

TASK [Activates our virtualhost] *********************
changed: [host1.example.org]

TASK [Check that our config is valid] *********************
fatal: [host1.example.org]: FAILED! => {"changed": true, "cmd": ["apache2ctl", "configtest"], "delta": "0:00:00.028736", "end": "2018-11-15 18:20:00.194825", "failed": true, "msg": "non-zero return code", "rc": 1, "start": "2018-11-15 18:20:00.166089", "stderr": "AH00526: Syntax error on line 2 of /etc/apache2/sites-enabled/awesome-app.conf:\nInvalid command 'RocumentDoot', perhaps misspelled or defined by a module not included in the server configuration", "stderr_lines": ["AH00526: Syntax error on line 2 of /etc/apache2/sites-enabled/awesome-app.conf:", "Invalid command 'RocumentDoot', perhaps misspelled or defined by a module not included in the server configuration"], "stdout": "Action 'configtest' failed.\nThe Apache error log may have more information.", "stdout_lines": ["Action 'configtest' failed.", "The Apache error log may have more information."]}
    to retry, use: --limit @/root/workspace/apache.retry

PLAY RECAP *********************
host1.example.org          : ok=4    changed=2    unreachable=0    failed=1   

```

As you can see since apache2ctl returns with an exit code of 1 when it fails, ansible is aware of it and stops the processes. 

Based on this failure, how do we revert back to a good state?

### Apache example - Conditionals

Ansible does not know how to revert back to a previous good state automatically. It is up to the DevOps person to undo any task(s) to the the point where the playbook has failed.

Update the playbook with the following content:

apache.yml

```
- hosts: web
  tasks:
    - name: Installs apache web server
      apt: pkg=apache2 state=installed update_cache=true

    - name: Push future default virtual host configuration
      copy: src=files/awesome-app dest=/etc/apache2/sites-available/awesome-app.conf mode=0640

    - name: Deactivates the default virtualhost
      command: a2dissite 000-default

    - name: Activates our virtualhost
      command: a2ensite awesome-app

    - name: Check that our config is valid
      command: apache2ctl configtest
      register: result
      ignore_errors: True

    - name: Rolling back - Restoring old default virtualhost
      command: a2ensite 000-default
      when: result|failed

    - name: Rolling back - Removing our virtualhost
      command: a2dissite awesome-app
      when: result|failed

    - name: Rolling back - Ending playbook
      fail: msg="Configuration file is not valid. Please check that before re-running the playbook."
      when: result|failed
    
    - name: Deactivates the default ssl virtualhost
      command: a2dissite default-ssl

      notify:
        - restart apache

  handlers:
    - name: restart apache
      service: name=apache2 state=restarted
```

#### Register Variables
Often in a playbook it may be useful to store the result of a given command in a variable and access it later. Use of the command module in this way can in many ways eliminate the need to write site specific facts, for instance, you could test for the existence of a particular program.

The ‘register’ keyword decides what variable to save a result in. The resulting variables can be used in templates, action lines, or when statements. 

#### When Statement
Sometimes you will want to skip a particular step on a particular host. This could be something as simple as not installing a certain package if the operating system is a particular version or it could be something like performing some cleanup steps if a filesystem is getting full.

#### Fail with custom message

The fail module fails the progress with a custom message. It can be useful for bailing out when a certain condition is met using when statement

Run the following command to execute our playbook: 

    ansible-playbook -i hosts -l host1.example.org apache.yml 

Output:

```
PLAY [web] *********************

TASK [Gathering Facts] *********************
ok: [host1.example.org]

TASK [Installs apache web server] *********************
ok: [host1.example.org]

TASK [Push future default virtual host configuration] *********************
ok: [host1.example.org]

TASK [Deactivates the default virtualhost] *********************
changed: [host1.example.org]

TASK [Activates our virtualhost] *********************
changed: [host1.example.org]

TASK [Check that our config is valid] *********************
fatal: [host1.example.org]: FAILED! => {"changed": true, "cmd": ["apache2ctl", "configtest"], "delta": "0:00:00.028029", "end": "2018-11-15 19:19:45.516863", "failed": true, "msg": "non-zero return code", "rc": 1, "start": "2018-11-15 19:19:45.488834", "stderr": "AH00526: Syntax error on line 2 of /etc/apache2/sites-enabled/awesome-app.conf:\nInvalid command 'RocumentDoot', perhaps misspelled or defined by a module not included in the server configuration", "stderr_lines": ["AH00526: Syntax error on line 2 of /etc/apache2/sites-enabled/awesome-app.conf:", "Invalid command 'RocumentDoot', perhaps misspelled or defined by a module not included in the server configuration"], "stdout": "Action 'configtest' failed.\nThe Apache error log may have more information.", "stdout_lines": ["Action 'configtest' failed.", "The Apache error log may have more information."]}
...ignoring

TASK [Rolling back - Restoring old default virtualhost] *********************
changed: [host1.example.org]

TASK [Rolling back - Removing our virtualhost] *********************
changed: [host1.example.org]

TASK [Rolling back - Ending playbook] *********************
fatal: [host1.example.org]: FAILED! => {"changed": false, "failed": true, "msg": "Configuration file is not valid. Please check that before re-running the playbook."}
    to retry, use: --limit @/root/workspace/apache.retry

PLAY RECAP *********************
host1.example.org          : ok=8    changed=5    unreachable=0    failed=1   
```

### Apache example - Git


In this section we will show how to effectively install a few packages and use the git module to deploy the application.

Update the playbook with the following content:

apache.yml

```
- hosts: web
  tasks:
    - name: Updates apt cache
      apt: update_cache=true

    - name: Installs apache web server
      apt: pkg=apache2 state=installed update_cache=true

    - name: Installs php module
      apt: pkg=libapache2-mod-php state=installed

    - name: Installs git
      apt: pkg=git state=installed

    - name: Push future default virtual host configuration
      copy: src=files/awesome-app dest=/etc/apache2/sites-available/awesome-app.conf mode=0640

    - name: Activates our virtualhost
      command: a2ensite awesome-app

    - name: Check that our config is valid
      command: apache2ctl configtest
      register: result
      ignore_errors: True

    - name: Rolling back - Restoring old default virtualhost
      command: a2ensite 000-default
      when: result|failed

    - name: Rolling back - Removing our virtualhost
      command: a2dissite awesome-app
      when: result|failed

    - name: Rolling back - Ending playbook
      fail: msg="Configuration file is not valid. Please check that before re-running the playbook."
      when: result|failed

    - name: Deploy our awesome application
      git: repo=https://github.com/leucos/ansible-tuto-demosite.git dest=/var/www/awesome-app
      tags: deploy

    - name: Deactivates the default virtualhost
      command: a2dissite 000-default

    - name: Deactivates the default ssl virtualhost
      command: a2dissite default-ssl
      notify:
        - restart apache

  handlers:
    - name: restart apache
      service: name=apache2 state=restarted
```

Instead of creating a few tasks to install the necessary packages, in Ansible, you can loop over a series of items as follows:

    - name: Installs necessary packages
      apt: pkg={{ item }} state=latest 
      with_items:
        - apache2
        - libapache2-mod-php
        - git  

Update the playbook with the new way of install multiple packages:

apache.yml

```
- hosts: web
  tasks:
    - name: Updates apt cache
      apt: update_cache=true

    - name: Installs necessary packages
      apt: pkg={{ item }} state=latest 
      with_items:
        - apache2
        - libapache2-mod-php
        - git

    - name: Push future default virtual host configuration
      copy: src=files/awesome-app dest=/etc/apache2/sites-available/awesome-app.conf mode=0640

    - name: Activates our virtualhost
      command: a2ensite awesome-app

    - name: Check that our config is valid
      command: apache2ctl configtest
      register: result
      ignore_errors: True

    - name: Rolling back - Restoring old default virtualhost
      command: a2ensite 000-default
      when: result|failed

    - name: Rolling back - Removing our virtualhost
      command: a2dissite awesome-app
      when: result|failed

    - name: Rolling back - Ending playbook
      fail: msg="Configuration file is not valid. Please check that before re-running the playbook."
      when: result|failed

    - name: Deploy our awesome application
      git: repo=https://github.com/leucos/ansible-tuto-demosite.git dest=/var/www/awesome-app
      tags: deploy

    - name: Deactivates the default virtualhost
      command: a2dissite 000-default

    - name: Deactivates the default ssl virtualhost
      command: a2dissite default-ssl
      notify:
        - restart apache

  handlers:
    - name: restart apache
      service: name=apache2 state=restarted
```

Run the following command to execute our playbook: 

    ansible-playbook -i hosts -l host1.example.org apache.yml 

Output:

```
PLAY [web] *********************

TASK [Gathering Facts] *********************
ok: [host1.example.org]

TASK [Updates apt cache] *********************
changed: [host1.example.org]

TASK [Installs necessary packages] *********************
changed: [host1.example.org] => (item=[u'apache2', u'libapache2-mod-php', u'git'])

TASK [Push future default virtual host configuration] *********************
changed: [host1.example.org]

TASK [Activates our virtualhost] *********************
changed: [host1.example.org]

TASK [Check that our config is valid] *********************
changed: [host1.example.org]

TASK [Rolling back - Restoring old default virtualhost] *********************
skipping: [host1.example.org]

TASK [Rolling back - Removing our virtualhost] *********************
skipping: [host1.example.org]

TASK [Rolling back - Ending playbook] *********************
skipping: [host1.example.org]

TASK [Deploy our awesome application] *********************
changed: [host1.example.org]

TASK [Deactivates the default virtualhost] *********************
changed: [host1.example.org]

TASK [Deactivates the default ssl virtualhost] *********************
changed: [host1.example.org]

RUNNING HANDLER [restart apache] *********************
changed: [host1.example.org]

PLAY RECAP *********************
host1.example.org          : ok=10   changed=9    unreachable=0    failed=0   

```

Note: We have added *tags* to our task "Deploy our awesome application". If  you have a large playbook it may become useful to be able to run a specific part of the configuration without running the whole playbook.  Let us say the git repo has been updated and we to speed up its deployment.

Run the following command to execute only the tags portion of the playbook: 

    ansible-playbook -i hosts -l host1.example.org apache.yml -t deploy

Output:

```
PLAY [web] *********************

TASK [Gathering Facts] *********************
ok: [host1.example.org]

TASK [Deploy our awesome application] *********************
ok: [host1.example.org]

PLAY RECAP *********************
host1.example.org          : ok=2    changed=0    unreachable=0    failed=0   
```

### Apache example - Bigger and better

In this section, we'll add another web server and a load balancer.

First, we will need to update the inventory file with following content:

hosts

```
[web]
host1.example.org
host2.example.org

[haproxy]
host0.example.org
```

To create two web servers, just remove "-l host1.example.org" from our previous command line. 

NOTE: -l is a switch that limits the playbook to run on specific hosts. Now, we would like playbooks to run on all hosts where the playbook is intended to run on, in this case [web].

Run the following command to execute our playbook: 

    ansible-playbook -i hosts apache.yml 

Output:

```
PLAY [web] *********************

TASK [Gathering Facts] *********************
ok: [host2.example.org]
ok: [host1.example.org]

TASK [Updates apt cache] *********************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [Installs necessary packages] *********************
ok: [host1.example.org] => (item=[u'apache2', u'libapache2-mod-php', u'git'])
changed: [host2.example.org] => (item=[u'apache2', u'libapache2-mod-php', u'git'])

TASK [Push future default virtual host configuration] *********************
ok: [host1.example.org]
changed: [host2.example.org]

TASK [Activates our virtualhost] *********************
changed: [host2.example.org]
changed: [host1.example.org]

TASK [Check that our config is valid] *********************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [Rolling back - Restoring old default virtualhost] *********************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [Rolling back - Removing our virtualhost] *********************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [Rolling back - Ending playbook] *********************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [Deploy our awesome application] *********************
ok: [host1.example.org]
changed: [host2.example.org]

TASK [Deactivates the default virtualhost] *********************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [Deactivates the default ssl virtualhost] *********************
changed: [host1.example.org]
changed: [host2.example.org]

RUNNING HANDLER [restart apache] *********************
changed: [host2.example.org]
changed: [host1.example.org]

PLAY RECAP *********************
host1.example.org          : ok=10   changed=6    unreachable=0    failed=0   
host2.example.org          : ok=10   changed=9    unreachable=0    failed=0   

```

We see that the webservers are up and running, the next step is to put a load balancer in front of them.

### Apache example - Templates

We'll use the [haproxy] as loadbalancer and install is just like we did for apache. But now configuration is a bit more tricky since we need to list all web servers in [haproxy]'s configuration... Luckily, Ansible uses Jinja2 a templating engine for Python. When you write Jinja2 templates, you can use any variable defined by Ansible. 

#### HAProxy configuration template

Created a folder called templates and created a Jinja template with name haproxy.cfg.j2 with the following content: 

haproxy.cfg.j2

```
global
    daemon
    maxconn 256

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

listen cluster
    bind {{ ansible_eth0['ipv4']['address'] }}:80
    mode http
    stats enable
    balance roundrobin
{% for backend in groups['web'] %}
    server {{ hostvars[backend]['ansible_hostname'] }} {{ hostvars[backend]['ansible_eth0']['ipv4']['address'] }} check port 80
{% endfor %}
    option httpchk HEAD /index.php HTTP/1.0
```

NOTE:  I have use the .j2 extension by convention, but this is not mandatory.

{% for backend in groups['web'] %} {% endfor %} loops through all the [web] hosts and put this host in the backend variable. For each of the hosts it will render a line using host's facts. All hosts' facts are exposed in the hostvars variable, so it's easy to access another host variables (like its hostname or in this case IP). 

{{ ansible_eth0['ipv4']['address'] }} will be replaced by the IP of the load balancer on eth0.  This value is known to Ansible from by means of the setup module.

Files and folders structure:

```
├── apache.yml
├── hosts 
├── files 
│   ├── awesome-app
├── templates 
│   ├── haproxy.cfg.j2  
```

#### HAProxy playbook

Since we are playbook experts by now, we should very familiar with with the following content for our new haproxy playbook:

haproxy.yml

```
- hosts: haproxy
  tasks:
    - name: Installs haproxy load balancer
      apt: pkg=haproxy state=installed update_cache=yes

    - name: Pushes configuration
      template: src=templates/haproxy.cfg.j2 dest=/etc/haproxy/haproxy.cfg mode=0640 owner=root group=root
      notify:
        - restart haproxy

    - name: Sets default starting flag to 1
      lineinfile: dest=/etc/default/haproxy regexp="^ENABLED" line="ENABLED=1"
      notify:
        - restart haproxy 

  handlers:
    - name: restart haproxy
      service: name=haproxy state=restarted
```

We have added the a new module called templates and restrict this playbook to the group haproxy.

Files and folders structure:

```
├── apache.yml
├── files 
├── haproxy.yml 
├── hosts 
│   ├── awesome-app
├── templates 
│   ├── haproxy.cfg.j2  
```

We need to run both playbooks in the same command line since haproxy.yml is dependant on data from the two web servers.

Run the following command to execute our playbooks: 

    ansible-playbook -i hosts apache.yml haproxy.yml 

Output:

```
PLAY [web] *********************

TASK [Gathering Facts] *********************
ok: [host2.example.org]
ok: [host1.example.org]

TASK [Updates apt cache] *********************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [Installs necessary packages] *********************
ok: [host1.example.org] => (item=[u'apache2', u'libapache2-mod-php', u'git'])
ok: [host2.example.org] => (item=[u'apache2', u'libapache2-mod-php', u'git'])

TASK [Push future default virtual host configuration] *********************
ok: [host2.example.org]
ok: [host1.example.org]

TASK [Activates our virtualhost] *********************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [Check that our config is valid] *********************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [Rolling back - Restoring old default virtualhost] *********************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [Rolling back - Removing our virtualhost] *********************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [Rolling back - Ending playbook] *********************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [Deploy our awesome application] *********************
ok: [host1.example.org]
ok: [host2.example.org]

TASK [Deactivates the default virtualhost] *********************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [Deactivates the default ssl virtualhost] *********************
changed: [host1.example.org]
changed: [host2.example.org]

RUNNING HANDLER [restart apache] *********************
changed: [host2.example.org]
changed: [host1.example.org]

PLAY RECAP *********************
host1.example.org          : ok=10   changed=6    unreachable=0    failed=0   
host2.example.org          : ok=10   changed=6    unreachable=0    failed=0   


PLAY [haproxy] *********************

TASK [Gathering Facts] *********************
ok: [host0.example.org]

TASK [Installs haproxy load balancer] *********************
changed: [host0.example.org]

TASK [Pushes configuration] *********************
changed: [host0.example.org]

TASK [Sets default starting flag to 1] *********************
changed: [host0.example.org]

RUNNING HANDLER [restart haproxy] *********************
changed: [host0.example.org]

PLAY RECAP *********************
host0.example.org          : ok=5    changed=4    unreachable=0    failed=0   
host1.example.org          : ok=10   changed=6    unreachable=0    failed=0   
host2.example.org          : ok=10   changed=6    unreachable=0    failed=0
```

NOTE 1: HAProxy's statistics at http://<IP>/haproxy?stats 

NOTE 2: Adding an empty play for web hosts at the top is a little trick in running the haproxy playbook solo. It will trigger facts gathering on hosts in group web that is required because the haproxy playbook needs to pick facts from hosts in this group. 

Update the plabook with the following content:

haproxy.yml

```
- hosts: web

- hosts: haproxy
  tasks:
    - name: Installs haproxy load balancer
      apt: pkg=haproxy state=installed update_cache=yes

    - name: Pushes configuration
      template: src=templates/haproxy.cfg.j2 dest=/etc/haproxy/haproxy.cfg mode=0640 owner=root group=root
      notify:
        - restart haproxy

    - name: Sets default starting flag to 1
      lineinfile: dest=/etc/default/haproxy regexp="^ENABLED" line="ENABLED=1"
      notify:
        - restart haproxy 

  handlers:
    - name: restart haproxy
      service: name=haproxy state=restarted
```

Run the following command to execute the playbook: 

    ansible-playbook -i hosts haproxy.yml

### Apache example - Veriables revisted

So we've setup our loadbalancer, and it works quite well. We grabbed variables from facts and used them to build the configuration. But Ansible also supports other kinds of variables. We already saw ansible_host in inventory, but now we'll use variables defined in host_vars and group_vars files. 

#### group_vars

HAProxy usually checks if the backends are alive. When a backend seems dead, it is removed from the backend pool and HAproxy doesn't send requests to it anymore. The check interval will be set in a group_vars file for haproxy. This will ensure all haproxies will inherit from it. 

Below the inventory folder, create the folder group_vars with the file name haproxy and the following content: 

haproxy

    haproxy_check_interval: 3000
    haproxy_stats_socket: /tmp/sock

NOTE: The file has to be named after the group you want to define the variables for. 

#### host_vars

Backends can also have different weights (between 0 and 256). The higher the weight, the higher number of connections the backend will receive compared to other backends. It's useful to spread traffic more appropriately if nodes are not equally powerful. 

Below the inventory folder, create the folder host_vars with the file name of the hosts and the following content: 

host0.example.com:

    haproxy_backend_weight: 150
    haproxy_stats_socket: /tmp/sock

NOTE: If we'd define haproxy_backend_weight in group_vars/web, it would be used as a 'default': variables defined in host_vars files overrides varibles defined in group_vars. 

host1.example.com:

    haproxy_backend_weight: 100

host2.example.com: 

    haproxy_backend_weight: 150

NOTE: The file has to be named after the host you want to define the variables for. 

Finally, the template must be updated to use these variables.

Update the template with the following content:

haproxy.cfg.j2

```
global
    daemon
    maxconn 256
{% if haproxy_stats_socket %}
    stats socket {{ haproxy_stats_socket }}
{% endif %}

defaults
    mode http
    timeout connect 5000ms
    timeout client 50000ms
    timeout server 50000ms

listen cluster
    bind {{ ansible_eth0['ipv4']['address'] }}:80
    mode http
    stats enable
    balance roundrobin
{% for backend in groups['web'] %}
    server {{ hostvars[backend]['ansible_hostname'] }} {{ hostvars[backend]['ansible_eth0']['ipv4']['address'] }} check inter {{ haproxy_check_interval }} weight {{ hostvars[backend]['haproxy_backend_weight'] }} port 80
{% endfor %}
    option httpchk HEAD /index.php HTTP/1.0
```

NOTE: {% if ... block. This block enclosed will only be rendered if the test is true. So if we define haproxy_stats_socket somewhere for our loadbalancer (we might even use the --extra-vars="haproxy_stats_sockets=/tmp/sock" at the command line), the enclosed line will appear in the generated configuration file. 

Files and folders structure:

```
├── apache.yml
├── files 
├── group_vars
│   ├── haproxy 
├── haproxy.yml 
├── hosts 
│   ├── awesome-app
├── host_vars
│   ├── host1.example.com
│   ├── host2.example.com
├── templates 
│   ├── haproxy.cfg.j2  
```

Run the following command to execute the haproxy.yml playbook with the web hosts trick: 

    ansible-playbook -i hosts haproxy.yml 

Output:

PLAY [web] *********************

TASK [Gathering Facts] *********************
ok: [host1.example.org]
ok: [host2.example.org]

PLAY [haproxy] *********************

TASK [Gathering Facts] *********************
ok: [host0.example.org]

TASK [Installs haproxy load balancer] *********************
ok: [host0.example.org]

TASK [Pushes configuration] *********************
changed: [host0.example.org]

TASK [Sets default starting flag to 1] *********************
ok: [host0.example.org]

RUNNING HANDLER [restart haproxy] *********************
changed: [host0.example.org]

PLAY RECAP *********************
host0.example.org          : ok=5    changed=2    unreachable=0    failed=0   
host1.example.org          : ok=1    changed=0    unreachable=0    failed=0   
host2.example.org          : ok=1    changed=0    unreachable=0    failed=0   

### Apache example - Roles

Roles are just a new way of organizing files but bring interesting [features](http://docs.ansible.com/ansible/latest/playbooks.html). Roles assume a specific file organization. While there is a suggested layout regarding roles, you can organize things the way you want using includes. However, role's conventions help building modular playbooks and housekeeping will be much simpler. 

Files and folders structure:

```
roles
│
└── common
    │
    ├── defaults 
    │   ├── main.yml
    │   ├── ... 
    │    
    ├── files 
    │   ├── file1
    │   ├── ... 
    │  
    ├── handlers 
    │   ├── main.yml
    │   ├── some_other_yml_file.yml  
    │   ├── ...  
    │     
    ├── meta 
    │   ├── main.yml
    │   ├── some_other_yml_file.yml  
    │   ├── ... 
    │       
    ├── tasks 
    │   ├── main.yml
    │   ├── some_other_yml_file.yml  
    │   ├── ...  
    │     
    ├── templates 
    │   ├── template.j2
    │   ├── ... 
    │       
    └── vars 
        ├── main.yml
        ├── some_other_yml_file.yml  
        ├── ...  

```

Roles must include at least one of these directories, however it is perfectly fine to exclude any which are not being used. When in use, each directory must contain a main.yml file, which contains the relevant content:

    defaults - default variables for the role.
    files - contains files which can be deployed via this role.
    handlers - contains handlers, which may be used by this role or even anywhere outside this role.
    meta - defines some meta data for this role. See below for more details.
    tasks - contains the main list of tasks to be executed by the role.
    templates - contains templates which can be deployed via this role.
    vars - other variables for the role.

The steps to create apache roles from our apache playbook are as follows: 

    create the roles directory and apache role layout
    extract the apache handler into roles/apache/handlers/main.yml
    move the apache configuration file awesome-app into roles/apache/files/
    create a role playbook

#### Apache Folders

Create the required folder structure for apache role. 

Run the following command: 

    mkdir -p roles/apache/{tasks,handlers,files} 

#### Apache Files

In the folder roles/apache/tasks, create the file name main.yml and the contents as follows:

main.yml:

```
- name: Updates apt cache
  apt: update_cache=true

- name: Installs necessary packages
  apt: pkg={{ item }} state=latest
  with_items:
    - apache2
    - libapache2-mod-php
    - git

- name: Push future default virtual host configuration
  copy: src=awesome-app dest=/etc/apache2/sites-available/awesome-app.conf mode=0640

- name: Activates our virtualhost
  command: a2ensite awesome-app

- name: Check that our config is valid
  command: apache2ctl configtest
  register: result
  ignore_errors: True

- name: Rolling back - Restoring old default virtualhost
  command: a2ensite 000-default
  when: result|failed

- name: Rolling back - Removing our virtualhost
  command: a2dissite awesome-app
  when: result|failed

- name: Rolling back - Ending playbook
  fail: msg="Configuration file is not valid. Please check that before re-running the playbook."
  when: result|failed

- name: Deploy our awesome application
  git: repo=https://github.com/leucos/ansible-tuto-demosite.git dest=/var/www/awesome-app
  tags: deploy

- name: Deactivates the default virtualhost
  command: a2dissite 000-default

- name: Deactivates the default ssl virtualhost
  command: a2dissite default-ssl
  notify:
    - restart apache
```

The contents of the main.yml file contains only the tasks found in the apache.yml file.


In the folder roles/apache/handlers, create the file name main.yml and the contents as follows:

main.yml:

```
- name: restart apache
  service: name=apache2 state=restarted
```

The contents of the main.yml file contains only the handlers found in the apache.yml file.


Move the configuration file into the roles/apache/files folder using the following command:

    mv files/awesome-app roles/apache/files/ 

#### HAProxy Folders

We will not go through the same steps we just did for the apache role, but instead we will use ansible-galaxy.

Run the following command: 

    ansible-galaxy --offline init roles/haproxy

Output:

    - roles/haproxy was created successfully

You can check the directory structure with ls -la roles/haproxy. 

#### HAProxy Files

In the folder roles/haproxy/tasks, create the file name main.yml and the contents as follows:

main.yml:

```
- name: Installs haproxy load balancer
  apt: pkg=haproxy state=installed update_cache=yes

- name: Pushes configuration
  template: src=haproxy.cfg.j2 dest=/etc/haproxy/haproxy.cfg mode=0640 owner=root group=root
  notify:
    - restart haproxy

- name: Sets default starting flag to 1
  lineinfile: dest=/etc/default/haproxy regexp="^ENABLED" line="ENABLED=1"
  notify:
    - restart haproxy
```

In the folder roles/haproxy/handlers, create the file name main.yml and the contents as follows:

main.yml:

```
- name: restart haproxy
  service: name=haproxy state=restarted
```

Finally move templates folder (which only contains the haproxy template file) to the correct folder with the following command:

    mv templates roles/haproxy/ 

Files and folders structure:

```
group_vars
│
├── haproxy
hosts
│
host_vars
│
├── host0.example.com
├── host1.example.com
├── host2.example.com
│
site.yml
│
role
├─── apache
│   │
│   ├── files 
│   │   └── awesome-app
│   │    
│   ├── handlers 
│   │   └── main.yml
│   │  
│   └── tasks 
│       └── main.yml
│
└── haproxy
    │
    README.MD
    │
    ├── defaults 
    │   └── main.yml
    │    
    ├── files 
    │  
    ├── handlers 
    │   └── main.yml
    │    
    ├── meta 
    │   └── main.yml
    │       
    ├── tasks 
    │   └── main.yml
    │     
    ├── templates 
    │   └── haproxy.cfg.j2
    │       
    └── vars 
        └── main.yml 
```


### Role playbook

We will call our top level playbook that we'll use to map hosts and host groups to roles site.yml.

site.yml

```
- hosts: web
  roles:
    - { role: apache }

- hosts: haproxy
  roles:
    - { role: haproxy }
```

Run the site.yml playbook with the following command: 

    ansible-playbook -i hosts site.yml

Output:

```
PLAY [web] ************************************************************************************************************************

TASK [Gathering Facts] ************************************************************************************************************
ok: [host2.example.org]
ok: [host1.example.org]

TASK [apache : Updates apt cache] *************************************************************************************************
changed: [host2.example.org]
changed: [host1.example.org]

TASK [apache : Installs necessary packages] ***************************************************************************************
ok: [host1.example.org] => (item=[u'apache2', u'libapache2-mod-php', u'git'])
ok: [host2.example.org] => (item=[u'apache2', u'libapache2-mod-php', u'git'])

TASK [apache : Push future default virtual host configuration] ********************************************************************
changed: [host2.example.org]
changed: [host1.example.org]

TASK [apache : Activates our virtualhost] *****************************************************************************************
changed: [host2.example.org]
changed: [host1.example.org]

TASK [apache : Check that our config is valid] ************************************************************************************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [apache : Rolling back - Restoring old default virtualhost] ******************************************************************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [apache : Rolling back - Removing our virtualhost] ***************************************************************************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [apache : Rolling back - Ending playbook] ************************************************************************************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [apache : Deploy our awesome application] ************************************************************************************
ok: [host1.example.org]
ok: [host2.example.org]

TASK [apache : Deactivates the default virtualhost] *******************************************************************************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [apache : Deactivates the default ssl virtualhost] ***************************************************************************
changed: [host1.example.org]
changed: [host2.example.org]

RUNNING HANDLER [apache : restart apache] *****************************************************************************************
changed: [host2.example.org]
changed: [host1.example.org]

PLAY [haproxy] ********************************************************************************************************************

TASK [Gathering Facts] ************************************************************************************************************
ok: [host0.example.org]

TASK [haproxy : Installs haproxy load balancer] ***********************************************************************************
ok: [host0.example.org]

TASK [haproxy : Pushes configuration] *********************************************************************************************
ok: [host0.example.org]

TASK [haproxy : Sets default starting flag to 1] **********************************************************************************
ok: [host0.example.org]

PLAY RECAP ************************************************************************************************************************
host0.example.org          : ok=4    changed=0    unreachable=0    failed=0   
host1.example.org          : ok=10   changed=7    unreachable=0    failed=0   
host2.example.org          : ok=10   changed=7    unreachable=0    failed=0  
```

NOTE: Running all the roles in site.yml may take a long time. What if you only wanted to push changes to web? This is also easy, with the limit flag. Run the following: 

    ansible-playbook -i hosts -l web site.yml 

```
PLAY [web] ************************************************************************************************************************

TASK [Gathering Facts] ************************************************************************************************************
ok: [host2.example.org]
ok: [host1.example.org]

TASK [apache : Updates apt cache] *************************************************************************************************
changed: [host2.example.org]
changed: [host1.example.org]

TASK [apache : Installs necessary packages] ***************************************************************************************
ok: [host1.example.org] => (item=[u'apache2', u'libapache2-mod-php', u'git'])
ok: [host2.example.org] => (item=[u'apache2', u'libapache2-mod-php', u'git'])

TASK [apache : Push future default virtual host configuration] ********************************************************************
ok: [host1.example.org]
ok: [host2.example.org]

TASK [apache : Activates our virtualhost] *****************************************************************************************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [apache : Check that our config is valid] ************************************************************************************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [apache : Rolling back - Restoring old default virtualhost] ******************************************************************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [apache : Rolling back - Removing our virtualhost] ***************************************************************************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [apache : Rolling back - Ending playbook] ************************************************************************************
skipping: [host1.example.org]
skipping: [host2.example.org]

TASK [apache : Deploy our awesome application] ************************************************************************************
ok: [host2.example.org]
ok: [host1.example.org]

TASK [apache : Deactivates the default virtualhost] *******************************************************************************
changed: [host1.example.org]
changed: [host2.example.org]

TASK [apache : Deactivates the default ssl virtualhost] ***************************************************************************
changed: [host1.example.org]
changed: [host2.example.org]

RUNNING HANDLER [apache : restart apache] *****************************************************************************************
changed: [host1.example.org]
changed: [host2.example.org]

PLAY [haproxy] ********************************************************************************************************************
skipping: no hosts matched

PLAY RECAP ************************************************************************************************************************
host1.example.org          : ok=10   changed=6    unreachable=0    failed=0   
host2.example.org          : ok=10   changed=6    unreachable=0    failed=0   
```

# Conclusion

Ansible is simple agentless automation tool that anyone can use for application deployment, configuration management, and orchestration — all from one system.