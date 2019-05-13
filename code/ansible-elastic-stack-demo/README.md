# centos-elastic-stack-ansible
Ansible Playbook Example for Elastic Stack (Elasticsearch, Logstash, Kibana, Beats)

### Configure IP address on the following file
```
hosts/elastic.hosts
```

### Set up Elastic Stack (Elasticsearch, Logstash and Kibana)
Note: will be installed on the same hosts
```
sudo ansible-playbook -i hosts/elastic.hosts playbooks/elastic_stack_setup.yml
```

### Set up Filebeat
```
sudo ansible-playbook -i hosts/elastic.hosts playbooks/filebeat.yml
```