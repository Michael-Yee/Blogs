---
title: The fundamentals of Ansible
author: Michael Yee
published: True
---


# Overview

In this blog, I will describe some of the fundamentals concepts of Ansible.  
NOTE: This blog assume the reader has an understanding of the YAML syntax.

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

### Apahe example - Start here

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

### Apahe example - Pushing files on nodes

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

### Apahe example - Failure

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

As you can see since apache2ctl returns with an exit code of 1 when it fails, ansible is aware of it and stops processing. 

Based on this failure, how do we revert back to a good state?






























# Conclusion

Ansible is simple agentless automation tool that anyone can use for application deployment, configuration management, and orchestration — all from one system.