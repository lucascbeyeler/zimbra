Ansible-Zimbra
=========

Ansible role to install and configure Zimbra Collaboration Open Source Edition in a monoserver environment

Requirements
------------

* [Ansible](https://github.com/ansible/ansible) 2.2.0 or superior. Less than this and you will have problems running Zimbra's Playbook. See ansible-modules-core Bug #4202

Role Variables
--------------

* **hostname:** set the hostname of your server **WITHOUT** the domain;
* **domain:** set the domain for the server and the primary domain for your Zimbra server;
* **zmpasswd:** set the password used for every single service in your Zimbra server, like the admin account and the LDAPServer - **WARNING:** do not put special characters in the password during the install;
* **zmnetwork:** set the network the Zimbra server is;
* **zmlogologin:** Inform the path for your logo (Login Screen) - don't inform and no image will be applied;
* **zmlogoapp:** Inform the path for your logo (Application Screen) - don't inform and no image will be applied;

Dependencies
------------

It's a good idea to apply the role ansible-commons before run this playbook, because we do not cover any kind of server preparation, like updates.


Example Playbook
----------------

    - hosts: servers
      roles:
         - role: lucascbeyeler.zimbra,
           hostname: warudo,
           domain: hollowbastion.com,
           zmpasswd: 123change,
           zmnetwork: 192.168.122.0/24,
           zmlogologin: /tmp/login.png,
           zmlogoapp: /tmp/app.png

License
-------

GNU GENERAL PUBLIC LICENSE

Author Information
------------------

https://github.com/lucascbeyeler
