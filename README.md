Ansible-Zimbra
=========

Ansible role to install and configure Zimbra Collaboration Open Source Edition in a monoserver environment

[![Build Status](https://travis-ci.org/lucascbeyeler/ansible-zimbra.svg?branch=master)](https://travis-ci.org/lucascbeyeler/ansible-zimbra)
[![Zimbra Version](https://img.shields.io/badge/Zimbra-8.7.5-blue.svg)](https://www.zimbra.com/downloads/zimbra-collaboration-open-source/)

Requirements
------------

* [Ansible](https://github.com/ansible/ansible) 2.2.0 or superior. Less than this and you will have problems running Zimbra's Playbook. See ansible-modules-core Bug #4202

* Configure de file /etc/ansible/ansible.cfg (create if don't exist) and set this options - not required if you using key and the ssh user is "root" already:
```
[defaults]
host_key_checking=False
stdout_callback=skippy

[ssh_connection]
pipelining=True
```

Install
--------------
ansible-zimbra is already in Ansible Galaxy, so the only thing you need to install this script in your machine is just use ansible-galaxy command:

```
ansible-galaxy install lucascbeyeler.ansible-zimbra
```

Update
--------------
When a new version of ansible-zimbra is released, you will need to run the install process again, but with the "-f" or "--force" parameter.

```
ansible-galaxy install -f lucascbeyeler.ansible-zimbra
```

Features
--------------

* Configuring SpamAssassin, Pyzor and Razor;
* Configure a logo for your server - **WARNING**: [Read this article for more details about the logo](https://blog.zimbra.com/2015/09/change-login-app-logo-open-source-network-edition/);
* Enable PolicyD service and web admin;
* Proxy Admin;
* HTTP to HTTPS redirect;
* LMTP Host Lookup in Native mode;


Role Variables
--------------

* **hostname:** set the hostname of your server **WITHOUT** the domain;
* **domain:** set the domain for the server and the primary domain for your Zimbra server;
* **zmpasswd:** set the password used for every single service in your Zimbra server, like the admin account and the LDAPServer - **WARNING:** do not put special characters in the password during the install;
* **zmnetwork:** set the network the Zimbra server is;
* **zmlogologin:** Inform the path for your logo (Login Screen) - don't inform and no image will be applied;
* **zmlogoapp:** Inform the path for your logo (Application Screen) - don't inform and no image will be applied;
* **timezone:** inform the timezone the playbook should set in your server;

Dependencies
------------

To run this playbook, you will need to run [lucascbeyeler.commons](https://github.com/lucascbeyeler/ansible-commons) too. We do not cover any kind of server preparation, like upgrade the system or change the hostname (even put the hostname in /etc/hosts is made by commons). The motive is because all my playbooks will need some kind of preparation before executed, so to not including the same code in every single project, I made a different playbook that will do everything that is considered "common" in each one of my playbooks.

Example Playbook
----------------
```
    - hosts: zimbra
      become: yes
      become_method: sudo
      roles:
         - role: lucascbeyeler.ansible-zimbra
           hostname: warudo
           domain: hollowbastion.com
           timezone: America/Sao_Paulo
           zmpasswd: 123change
           zmnetwork: 192.168.122.0/24
           zmlogologin: /tmp/login.png
           zmlogoapp: /tmp/app.png
```

License
-------

GNU GENERAL PUBLIC LICENSE

Author Information
------------------

https://github.com/lucascbeyeler
