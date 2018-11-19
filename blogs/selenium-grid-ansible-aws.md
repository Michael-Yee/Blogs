---
title: Building a Selenium Grid on AWS EC2 instances using Ansible
author: Michael Yee
published: True
---


# Overview

In this blog, I will describe how to create a Selemium Grid on AWS EC2 instances using Ansible.

NOTE: This blog assume the reader has an understanding of Ansible and AWS cloud platform.

## What Is Selenium & Selenium Grid?

Selenium Grid is a part of the Selenium Suite that specializes in running multiple tests across different browsers, operating systems and machines in parallel.

![Selenium Grid](../images/selenium/hub_and_nodes.jpg "Selenium Grid")

Selenium Grid uses a hub-node concept where you only run the test on a single machine called a hub, but the execution will be done by different machines called nodes. 

### Selenium Grid Architecture
Selenium Grid has a Hub and Node Architecture.

#### The Hub

- The hub is the central point where the tests are loaded
- The hub is launched on a single machine and there is only one hub in a grid.
- The machine containing the hub is where the tests will be run, but you will see the browser being automated on the node.

#### The Nodes

- Nodes are one or more Selenium instances that will execute the tests that you loaded on the hub.
- Nodes can be launched on multiple machines with different platforms and browsers.
- The machines running the nodes need not be the same platform as that of the hub.

Let's start!

---

## Prerequisites

### Ansible

Ansible is simple open source IT engine which automates application deployment, cloud provisioning, configuration management, intra service orchestration and many other IT tools.

Download instructions can be found [here](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html). To verify that ansible installed properly, run the following command:

    ansible --version


###Boto3 

Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which allows Ansible to communiate with the AWS API.

Run the following command to install boto3 (preferably on a virtural environment):

    pip install boto3

To verify that boto3 installed properly, run the following command:

    python -c "import boto3; print(boto3.__version__)"

Note which python you have installed boto3 onto by running this command:

  which python

## Identity Access Management (IAM)

### Groups

We need to create Group to define policies like users to have EC2FullAccess rights.

![Set Group Name](../images/selenium/set_group_name.png "Set Group Name")

![Attach Policy](../images/selenium/attach_policy.png "Attach Policy")

![Create Group](../images/selenium/create_group.png "Create Group")

### Users

We need to create User for programmatic access and add this user to Group that we created above.

![Set User Details](../images/selenium/set_user_details.png "Set User Details")

![Set Permissions](../images/selenium/set_permisssions.png "Set Permissions")

![Create User](../images/selenium/create_user.png "Create User")

After you have created a User, the fourth page will generate an Access key ID and Secret access key used for AWS API, CLI, SDK and other development tools... Save these keys!

## Ansible vault

Ansible Vault is a feature of ansible that allows you to keep sensitive data such as passwords or keys in encrypted files, rather than as plaintext in playbooks or roles. These vault files can then be distributed or placed in source control.

In the group_vars folder, create a file called aws_secret_key.yml with contents as follows:

    aws_access_key: <AWS_ACCESS_KEY>
    aws_secret_key: <AWS_SECRET_KEY>

Using ansible-vault, we can encrypt this and define the password needed to later decrypt it. Run the following command:

    ansible-vault encrypt group_vars/aws_secret_key.yml
    New Vault password: 
    Confirm New Vault password: 
    Encryption successful

The ansible-vault command will prompt you for a password twice (a second time to confirm the first). Once that's done, the file will be encrypted! If you edit the file directly, you'll just see encrypted text. It looks something like this:

    $ANSIBLE_VAULT;1.1;AES256
    38313030376238636530383537383131326330356462353030393764333032343431616436363262
    6264313137353164323866643363643065373633633539310a396534376663623364643331303239
    30616135303365663638306561363865373436346630616262363336376430643437393863313236
    6434326236383231650a393961643236383630616431363233343665623761343462353035353163
    32636636366364363265376330336437313330346263393036346630323233393164666239313964
    35626133666361316231393436373333363232316430353564646136636664373530663932333363
    37636434363634356663366466336536623833326135353463373731643339323131336532343139
    38373266386532333632306565376130666461353831376465356634633666303966643830626136
    3864

Once the file is encrypted, you can only edit the file by using ansible-vault. Run the following command:

    ansible-vault edit group_vars/aws_access_secret_keys.yml 
    Vault password: 

The file can be decrypted back to plaintext. Run the following command:

    ansible-vault decrypt group_vars/aws_access_secret_keys.yml 
    Vault password:

## roles

We will initalize the roles with ansible-galaxy.  First we need to create the roles folder:

    mkdir roles

Next, run the following command:

    ansible-galaxy --offline init roles/selenium-hub
    ansible-galaxy --offline init roles/selenium-chrome-node
    ansible-galaxy --offline init roles/selenium-firefox-node

## hosts file

The hosts file to handle our new EC2 instance that has yet to be created. Create the hosts file with the following content:

```
[local]
localhost ansible_python_interpreter=<PATH/TO/PYTHON>
```

## variables

The all file to store all our vairables that has yet to be created. First we need to create the group_vars folder:

    mkdir group_vars

Create the all file with the following content:

all:

```
# ---------------------------------------------------------------------------------------------------------------------
# General Variables
# ---------------------------------------------------------------------------------------------------------------------

aws_access_secret_keys: group_vars/aws_access_secret_keys.yml
keypair: selenium-grid
region: us-east-1
security_group: selenium-grid-node-sg

# ---------------------------------------------------------------------------------------------------------------------
# Selenium Hub Variables
# ---------------------------------------------------------------------------------------------------------------------

selenium_hub_count: 1
selenium_hub_image: ami-0dacf8938d3920488
selenium_hub_instance_type: t2.micro

# ---------------------------------------------------------------------------------------------------------------------
# Selenium Chrome Node Variables
# ---------------------------------------------------------------------------------------------------------------------

selenium_chrome_node_count: 1
selenium_chrome_node_image: ami-0075c96fd0f7e4109
selenium_chrome_node_instance_type: t2.micro

# ---------------------------------------------------------------------------------------------------------------------
# Selenium Firefox Node Variables
# ---------------------------------------------------------------------------------------------------------------------

selenium_firefox_node_count: 1
selenium_firefox_node_image: ami-0075c96fd0f7e4109
selenium_firefox_node_instance_type: t2.micro

```

These variables are the options we intend to use with our EC2 instance:

The aws_access_secret_keys variable points to the aws_access_secret_keys.yml file location.

The keypair refers to the name of the public/private key pair

The region is the region of your choice. If you receive huge volumes of traffic, it’s advised that you choose a region that it geographically closest to where most of your customers are located.

The count variable is the number of instances you want to launch. In our case, we will only need to create one Selenium Hub instance.

The image specifies a AMI (Amazon Machine Image). These are AMI I have previously created.

The instace type is t2.micro, this is suitable for our lab. It’s also eligible for the free tier, in which Amazon will not charge you for some services (including selected EC2 instance types) for a period of 1 year.

A security group acts as a virtual firewall for your instance to control inbound and outbound traffic. This is a security group I have previously created.

NOTE: If the security group did not exist, one could create a task to create the security grop as follows:

```
tasks:
    - name: Create a security group
      ec2_group:
        name: "{{ security_group }}"
        description: The Selenium Hub security group
        region: "{{ region }}"
        aws_access_key: "{{ aws_access_key }}"
        aws_secret_key: "{{ aws_secret_key }}"
        rules:
          - proto: tcp
            from_port: 22
            to_port: 22
            cidr_ip: 0.0.0.0/0
          - proto: tcp
            from_port: 4444
            to_port: 4444
            cidr_ip: 0.0.0.0/0
        rules_egress:
          - proto: all
            cidr_ip: 0.0.0.0/0
```

We use the ec2_group module provided natively by Ansible. The module requires a name, region and description for the security group. 

AWS security groups access two types of rules: incoming and outgoing. We’re more interested in what arrrives at our instance rather than what leaves it. So, we instruct our security group to allow:

    SSH on port 22
    webriver-manager on port 4444

NOTE:   The security group can also filter the source IP address from which the traffic is originating. By setting cidr_ip option to 0.0.0.0/0, it will accept traffic from anywhere in the world.

The rules_engress controls the network traffic leaving your instance to the outside world. We are not placing any filters on this.

## Role playbook

We will call our top level playbook to deploy the Selenium Grid selenium-grid-activate.yml. Create the selenium-grid-activate.yml file with the following content:

selenium-grid-activate.yml

```
- hosts: local
  connection: local
  gather_facts: False
  vars_files:
    - "{{ aws_access_secret_keys }}"
  roles:
    - { role: selenium-hub }

 - hosts: local
  connection: local
  gather_facts: False
  vars_files:
    - "{{ aws_access_secret_keys }}"  
  roles:
    - { role: selenium-chrome-node }

 - hosts: local
  connection: local
  gather_facts: False
  vars_files:
    - "{{ aws_access_secret_keys }}"  
  roles:
    - { role: selenium-chrome-node }
```

Let’s have a quick look at what each line of the file does:

```
hosts: Limits the hosts groups to local. It contains localhost and this is the way Ansible will work with EC2 instances. Behind the scenes, Ansible connects to Python boto3 on the local machine and use to establish connection with the AWS API and issue the necessary commands.

connection: sets the connection to local so that Ansible won’t attempt to establish an SSH connection session with localhost.

gather_facts: will not connect to the remote host and gather useful varibables about it.

vars_files: points the the locations of our aws_access_secret_keys.yml file

roles: points to each role module
```
## Create Selenium Hub EC2 instance

### selenium-hub tasks

The first task is to create and lauch an EC2 instance with the Selenium Hub AMI.

In the folder roles/selenium-hub/tasks, edit the file name main.yml and add the contents as follows:

main.yml:

```
- name: Launch Selenium Hub EC2 Instance
  ec2:
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
    count: "{{ selenium_hub_count }}"
    group: "{{ security_group }}"
    instance_type: "{{ selenium_hub_instance_type }}"
    image: "{{ selenium_hub_image }}"
    keypair: "{{ keypair }}"
    region: "{{ region }}"    
    wait: true
  register: ec2
```

We use the ec2 module provided natively by Ansible to creates an ec2 instances. The module requires the following parameters:

    AWS credential
    Number of instances to create
    Security group name
    Instance type
    AMI image id
    Keypair
    Region
 
NOTE ONE: we register a variable called ec2. The information within this variable (instance id, public IP, etc...) will be require at a later time.

NOTE TWO: The wait parameter instructs Ansible to wait for the instance to be created before reporting that the task is complete.

The next task is to add the newly created Selenium Hub EC2 instance to the hosts file.

In the folder roles/selenium-hub/tasks, edit the file name main.yml and add the contents as follows:

main.yml:

```
- name: Launch Selenium Hub EC2 Instance
  ec2:
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
    count: "{{ selenium_hub_count }}"
    group: "{{ security_group }}"
    instance_type: "{{ selenium_hub_instance_type }}"
    image: "{{ selenium_hub_image }}"
    keypair: "{{ keypair }}"
    region: "{{ region }}"    
    wait: true
  register: ec2

- name: Add Selenium Hub EC2 Instance to the hosts file
  add_host:
    name: "{{ item.public_ip }}"
    groups: selenium_hubs
  with_items: "{{ ec2.instances }}"
```

The add_host module allows you to add one or more hosts to a group. The group will be created if it does not already exist. In our case, we are adding the instance to selenium_hubs group.

The with_items takes the instances list in the ec2 variable that we created in the Launch Selenium Hub EC2 Instance task and loop through all of them with the reference of item. So, item.public_ip will get the public IP address assigned by AWS to that specific instance in the list.

Additionally, we want to the ec2_tag module to set a tag to our instance. A tag consists of a name and a value. We will need to add at least one tag to our instance specifying its name. The reason we need this tag is to be able to identify our instance later on when we need to perform additional actions against it, including termination. 

In the folder roles/selenium-hub/tasks, edit the file name main.yml and add the contents as follows:

main.yml:

```
- name: Launch Selenium Hub EC2 Instance
  ec2:
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
    count: "{{ selenium_hub_count }}"
    group: "{{ security_group }}"
    instance_type: "{{ selenium_hub_instance_type }}"
    image: "{{ selenium_hub_image }}"
    keypair: "{{ keypair }}"
    region: "{{ region }}"    
    wait: true
  register: ec2

- name: Add Selenium Hub EC2 Instance to the hosts file
  add_host:
    name: "{{ item.public_ip }}"
    groups: selenium_hubs
  with_items: "{{ ec2.instances }}"

- name: Add tag to Selenium Hub EC2 Instance
  ec2_tag:
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
    resource: "{{ item.id }}"
    region: "{{ region }}"
    state: "present"
  with_items: "{{ ec2.instances }}"
  args:
    tags:
      Type: selenium_hub
```

Finally, we want to make sure the Selenium Hub EC2 Instance creation process is completed and ready for communications.

In the folder roles/selenium-hub/tasks, edit the file name main.yml and add the contents as follows:

main.yml:

```
- name: Launch Selenium Hub EC2 Instance
  ec2:
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
    count: "{{ selenium_hub_count }}"
    group: "{{ security_group }}"
    instance_type: "{{ selenium_hub_instance_type }}"
    image: "{{ selenium_hub_image }}"
    keypair: "{{ keypair }}"
    region: "{{ region }}"    
    wait: true
  register: ec2

- name: Add Selenium Hub EC2 Instance to the hosts file
  add_host:
    name: "{{ item.public_ip }}"
    groups: selenium_hubs
  with_items: "{{ ec2.instances }}"

- name: Add tag to Selenium Hub EC2 Instance
  ec2_tag:
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
    resource: "{{ item.id }}"
    region: "{{ region }}"
    state: "present"
  with_items: "{{ ec2.instances }}"
  args:
    tags:
      Type: selenium_hub

- name: Wait for SSH port to be ready
  wait_for:
    host: "{{ item.public_ip }}"
    port: 22
    state: started
  with_items: "{{ ec2.instances }}"
```

The wait_for module pause playbook execution until a specific condition is met. In our case, checking if the port 22 has started to ensure the port is open.

### selenium-chrome-node tasks

In the folder roles/selenium-chrome-node/tasks, edit the file name main.yml and add the contents as follows:

main.yml:

```
- name: Launch Selenium Chrome Node EC2 Instance
  ec2:
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
    count: "{{ selenium_chrome_node_count }}"
    group: "{{ security_group }}"
    instance_type: "{{ selenium_chrome_node_instance_type }}"
    image: "{{ selenium_chrome_node_image }}"
    keypair: "{{ keypair }}"
    region: "{{ region }}"    
    wait: true
  register: ec2

- name: Add Selenium Chrome Node Instance to the hosts file
  add_host:
    name: "{{ item.public_ip }}"
    groups: selenium_chrome_nodes
  with_items: "{{ ec2.instances }}"

- name: Add a tag to Selenium Chrome Node EC2 Instance
  ec2_tag:
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
    resource: "{{ item.id }}"
    region: "{{ region }}"
    state: "present"
  with_items: "{{ ec2.instances }}"
  args:
    tags:
      Type: selenium_chrome_node

- name: Wait for SSH to be ready
  wait_for:
    host: "{{ item.public_ip }}"
    port: 22
    state: started
  with_items: "{{ ec2.instances }}"
```

### selenium-firefox-node tasks

In the folder roles/selenium-chrome-node/tasks, edit the file name main.yml and add the contents as follows:

main.yml:

```
- name: Launch Selenium Firefox Node EC2 Instance
  ec2:
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
    count: "{{ selenium_firefox_node_count }}"
    group: "{{ security_group }}"
    instance_type: "{{ selenium_firefox_node_instance_type }}"
    image: "{{ selenium_firefox_node_image }}"
    keypair: "{{ keypair }}"
    region: "{{ region }}"    
    wait: true
  register: ec2

- name: Add Selenium Firefox Node Instance to the hosts file
  add_host:
    name: "{{ item.public_ip }}"
    groups: selenium_firefox_nodes
  with_items: "{{ ec2.instances }}"

- name: Add a tag to Selenium Firefox Node EC2 Instance
  ec2_tag:
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
    resource: "{{ item.id }}"
    region: "{{ region }}"
    state: "present"
  with_items: "{{ ec2.instances }}"
  args:
    tags:
      Type: selenium_firefox_node

- name: Wait for SSH to be ready
  wait_for:
    host: "{{ item.public_ip }}"
    port: 22
    state: started
  with_items: "{{ ec2.instances }}"

```

## Running the playbook

Run the selenium-grid-activate.yml playbook along with the Ansible vault password by running the following command: 

    ansible-playbook --ask-vault-pass -i hosts selenium-grid-activate.yml
    Vault password:

Output:

```
PLAY [local] *********************

TASK [selenium-hub : Launch Selenium Hub EC2 Instance] *********************
changed: [localhost]

TASK [selenium-hub : Add Selenium Hub EC2 Instance to the hosts file] *********************
changed: ...

TASK [selenium-hub : Add a tag to Selenium Hub EC2 Instance] *********************
changed: ...

TASK [selenium-hub : Wait for SSH to be ready] *********************
ok: ...
PLAY [local] *********************

TASK [selenium-chrome-node : Launch Selenium Chrome Node EC2 Instance] *********************
changed: [localhost]

TASK [selenium-chrome-node : Add Selenium Chrome Node Instance to the hosts file] *********************
changed: ...

TASK [selenium-chrome-node : Add a tag to Selenium Chrome Node EC2 Instance] *********************
changed: ...

TASK [selenium-chrome-node : Wait for SSH to be ready] *********************
ok: ...

PLAY [local] *********************

TASK [selenium-firefox-node : Launch Selenium Firefox Node EC2 Instance] *********************
changed: [localhost]

TASK [selenium-firefox-node : Add Selenium Firefox Node Instance to the hosts file] *********************
changed: ...

TASK [selenium-firefox-node : Add a tag to Selenium Firefox Node EC2 Instance] *********************
changed: [...

TASK [selenium-firefox-node : Wait for SSH to be ready] *********************
ok: ...

PLAY RECAP *********************
localhost                  : ok=12   changed=9    unreachable=0    failed=0  
```

## Terminating the Selenium Hub EC2 instance

We will initalize the selenium-grid-terminate role with ansible-galaxy by running the following command:

    ansible-galaxy --offline init roles/selenium-grid-terminate

Create the top level playbook selenium-grid-activate.yml file that we'll use to terminate the Selenium Grid with the following content:

selenium-grid-terminate.yml

```
- hosts: local
  connection: local
  gather_facts: False
  vars_files:
    - "{{ aws_access_secret_keys }}"
  roles:
    - { role: selenium-grid-terminate }
```

In the folder roles/selenium-grid-terminate/tasks, edit the file name main.yml and add the contents as follows:

main.yml:

```
- name: Gather Selenium Hub EC2 instances facts
  ec2_instance_facts:
    region: "{{ region }}"
    filters:
      "tag:Type": "selenium_hub"
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
  register: ec2

- name: Terminate Selenium Hub EC2 Instance(s)
  ec2:
    instance_ids: '{{ item.instance_id }}'
    state: absent
    region: "{{ region }}"
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
  with_items: "{{ ec2.instances }}"

- name: Gather Selenium Chrome Node EC2 instances facts
  ec2_instance_facts:
    region: "{{ region }}"
    filters:
      "tag:Type": "selenium_chrome_node"
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
  register: ec2

- name: Terminate Selenium Chrome Node EC2 Instance(s)
  ec2:
    instance_ids: '{{ item.instance_id }}'
    state: absent
    region: "{{ region }}"
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
  with_items: "{{ ec2.instances }}"

- name: Gather Selenium Firefox Node EC2 instances facts
  ec2_instance_facts:
    region: "{{ region }}"
    filters:
      "tag:Type": "selenium_firefox_node"
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
  register: ec2

- name: Terminate Selenium Firefox Node EC2 Instance(s)
  ec2:
    instance_ids: '{{ item.instance_id }}'
    state: absent
    region: "{{ region }}"
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
  with_items: "{{ ec2.instances }}"

```

ec2_instance_facts: This task is responsible for collecting the instance facts. Don’t confuse this with the traditional fact-gathering that Ansible performs by default when it executes any playbook. Here, Ansible is collecting facts that are related to the presence of this instance on the AWS platform. Facts like the tags that were assigned to the instance are collected, which is what interests us.

ec2: We use the ec2 module to terminate the instance. The state parameter can take other values than absent depending on your requirements. For example, stopped will just shut down the instance, restarted will reboot it, and running will ensure that it is running (it will start the machine if stopped).

## Running the playbook

Run the selenium-grid-terminate.yml playbook along with the Ansible vault password by running the following command: 

    ansible-playbook --ask-vault-pass -i hosts selenium-grid-terminate.yml
    Vault password:

Output:

```
PLAY [local] *********************

TASK [selenium-grid-terminate : Gather Selenium Hub EC2 instances facts] *********************
ok: [localhost]

TASK [selenium-grid-terminate : Terminate Selenium Hub EC2 Instance(s)] *********************
changed: ...

TASK [selenium-grid-terminate : Gather Selenium Chrome Node EC2 instances facts] *********************
ok: [localhost]

TASK [selenium-grid-terminate : Terminate Selenium Chrome Node EC2 Instance(s)] *********************
changed: ...

TASK [selenium-grid-terminate : Gather Selenium Firefox Node EC2 instances facts] *********************
ok: [localhost]

TASK [selenium-grid-terminate : Terminate Selenium Firefox Node EC2 Instance(s)] *********************
changed: ...

PLAY RECAP *********************
localhost                  : ok=6    changed=3    unreachable=0    failed=0   
```













































