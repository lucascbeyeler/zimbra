Zimbra
=========

Non-Official ansible role to install and configure Zimbra Collaboration Open Source Edition on Red Hat, CentOS and Ubuntu Server.

[![Build Status](https://travis-ci.org/lucascbeyeler/zimbra.svg?branch=master)](https://travis-ci.org/lucascbeyeler/zimbra)
[![Zimbra Version](https://img.shields.io/badge/Zimbra-8.8.15-blue.svg)](https://www.zimbra.com/downloads/zimbra-collaboration-open-source/)
![Linux Distro](https://img.shields.io/badge/platform-CentOS%20%7C%20Red%20Hat%20%7C%20Ubuntu-blue.svg)
![Branch](https://img.shields.io/badge/Branch-Master-green.svg)
[![Ansible Version](https://img.shields.io/badge/Ansible-2.9.6-green.svg)](https://www.ansible.com/)

Requirements
------------

* [Ansible](https://github.com/ansible/ansible) 2.9.6 or high.

Install
--------------
Zimbra is already in Ansible Galaxy, so the only thing you need to install this script in your machine is just use ansible-galaxy command:

```
ansible-galaxy install lucascbeyeler.zimbra
```

Update
--------------
When a new version of ansible-zimbra is released, you will need to run the install process again, but with the "-f" or "--force" parameter.

```
ansible-galaxy install -f lucascbeyeler.zimbra
```

Features
--------------

* Run many times you want to apply the configuration - installatin only occur if the server has no Zimbra installed
* Configuring SpamAssassin, Pyzor and Razor;
* Configure a logo for your server - **WARNING**: [Read this article for more details about the logo](https://blog.zimbra.com/2015/09/change-login-app-logo-open-source-network-edition/);
* Enable PolicyD service and web admin;
* Proxy Admin;
* HTTP to HTTPS redirect;
* LMTP Host Lookup in Native mode;
* Customize your Zimbra OSE server;


Role Variables
--------------

* **hostname:** set the hostname of your server **WITHOUT** the domain;
* **domain:** set the domain for the server and the primary domain for your Zimbra server;
* **zmpasswd:** set the password used for every single service in your Zimbra server, like the admin account and the LDAPServer - **WARNING:** do not put special characters in the password during the install;
* **zmnetwork:** set the network the Zimbra server is;
* **zmlogologin:** Inform the path for your logo (Login Screen) - don't inform and no image will be applied;
* **zmlogoapp:** Inform the path for your logo (Application Screen) - don't inform and no image will be applied;
* **timezone:** inform the timezone the playbook should set in your server;
* **zimbra_version:** Inform which version of Zimbra you want to install. Default: 8.8.15

Service Variables - Inform "y" or "n"
--------------

* **zimbra_ldap:** Enable Zimbra LDAP Server - default: **y**
* **zimbra_logger:** Enable Zimbra Logger Service - default: **y**
* **zimbra_mta:**  Enable Zimbra MTA Service - default: **y**
* **zimbra_dnscache:** Enable Zimbra DNS Cache Service (unbound) - default: **n**
* **zimbra_snmp:**  Enable Zimbra SNMP Checks - default: **n**
* **zimbra_store:**  Enable Zimbra Store Service - default: **y**
* **zimbra_apache:**  Enable Zimbra Web Interface (Apache Web Server) - default: **y**
* **zimbra_spell:**  Enable Zimbra Spell Check - default: **y**
* **zimbra_memcached:**  Enable Zimbra Cache Service (Memcached) - default: **y**
* **zimbra_proxy:**  Enable Zimbra Proxy Service - default: **y**
* **zimbra_chat:**  Enable Zimbra Chat - default: **n**
* **zimbra_drive:**  Enable Zimbra ownCloud Drive - default: **n**
* **zimbra_imapd:** Enable Zimbra IMAPD Solo Service **BETA**  - default: **n**
* **zimbra_policyd:**  Enable Zimbra PolicyD Service - default: **n**

Dependencies
------------

To run this playbook, you will need to run [lucascbeyeler.baseline](https://github.com/lucascbeyeler/baseline) too. We do not cover any kind of server preparation, like upgrade the system or change the hostname (even put the hostname in /etc/hosts is made by commons). The motive is because all my playbooks will need some kind of preparation before executed, so to not including the same code in every single project, I made a different playbook that will do everything that is considered "common" in each one of my playbooks.

Example Playbook
----------------
```
    - hosts: zimbra
      become: yes
      become_method: sudo
      roles:
         - role: lucascbeyeler.zimbra
           hostname: localhost
           domain: localdomain
           timezone: America/Sao_Paulo
           zmpasswd: 123change
           zmnetwork: 192.168.122.0/24
           zmlogologin: /tmp/login.png
           zmlogoapp: /tmp/app.png
```

License
-------

[![GNU GPL v3.0](http://www.gnu.org/graphics/gplv3-127x51.png)](http://www.gnu.org/licenses/gpl.html)

View official GNU site <http://www.gnu.org/licenses/gpl.html>.

Author Information
------------------

* [Lucas Costa Beyeler](https://github.com/lucascbeyeler) - lucas.costab@outlook.com
