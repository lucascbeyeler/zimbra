Zimbra
=========

Non-Official ansible role to install, upgrade and configure Zimbra Collaboration Open Source Edition on Red Hat, CentOS and Ubuntu Server.

The role supports the latest version of Zimbra, **Zimbra 10.1 (Daffodil)**, as well as Zimbra 10.0 and 8.8.15.

[![CI](https://github.com/lucascbeyeler/zimbra/actions/workflows/ci.yml/badge.svg)](https://github.com/lucascbeyeler/zimbra/actions/workflows/ci.yml)
[![CircleCI](https://circleci.com/gh/lucascbeyeler/zimbra.svg?style=shield)](https://circleci.com/gh/lucascbeyeler/zimbra)
[![Zimbra Version](https://img.shields.io/badge/Zimbra-10.1%20%7C%2010.0%20%7C%208.8.15-blue.svg)](https://www.zimbra.com/product/release-notes/)
![Linux Distro](https://img.shields.io/badge/platform-CentOS%20%7C%20Red%20Hat%20%7C%20Ubuntu-blue.svg)
![Branch](https://img.shields.io/badge/Branch-Master-green.svg)
[![Ansible Version](https://img.shields.io/badge/Ansible-2.15-green.svg)](https://www.ansible.com/)

Requirements
------------

* [Ansible](https://github.com/ansible/ansible) 2.15 or higher.
* The `community.general` collection:
  ```
  ansible-galaxy collection install -r requirements.yml
  ```
* A server prepared by [lucascbeyeler.baseline](https://github.com/lucascbeyeler/baseline) (see [Dependencies](#dependencies)).

Supported Zimbra Versions
--------------

| Zimbra | Installer builds | Distributions |
|---|---|---|
| **10.1** (latest) | Set in **zm_repo** | Ubuntu 20.04 and 22.04, Red Hat / CentOS / Rocky 8 and 9 |
| **10.0** | Set in **zm_repo** | Ubuntu 20.04 and 22.04, Red Hat / CentOS / Rocky 8 and 9 |
| **8.8.15** (default) | Included in the role | Ubuntu 14.04 to 20.04, Red Hat / CentOS 6 to 8 |

The distributions are the ones each Zimbra version supports; the role runs on any of them as long as **zm_repo** has a build for it.

Zimbra only publishes the 8.8.15 installers of the Open Source Edition on files.zimbra.com, so they are the only builds the role knows out of the box. To install Zimbra 10.0 or 10.1, set **zimbra_version** to the version you want and point **zm_repo** to where your 10.x installers are (your own build or a mirror). See [Installing Zimbra 10.1](#installing-zimbra-101).

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

* Install Zimbra 10.1, 10.0 or 8.8.15, with only the services you choose;
* Upgrade an existing Zimbra installation to a newer version (**zimbra_upgrade**);
* Run many times you want to apply the configuration - installation only occur if the server has no Zimbra installed, every setting is changed only when it differs from what you asked, and Zimbra is restarted only when something changed;
* Fail with a clear message before downloading anything when **zm_repo** has no installer for your distribution;
* Optionally disable the systemd-resolved DNS stub listener, so zimbra-dnscache can use port 53;
* Configure the MTA's DNS blocklists (RBLs), and remove the ones that were shut down;
* Configuring SpamAssassin, Pyzor, Razor and Kevin McGrail's KAM rules;
* Configure a logo for your server - **WARNING**: [Read this article for more details about the logo](https://blog.zimbra.com/2015/09/change-login-app-logo-open-source-network-edition/);
* Enable PolicyD service and web admin;
* Proxy Admin;
* HTTP to HTTPS redirect;
* LMTP Host Lookup in Native mode;
* Customize your Zimbra OSE server;
* Optionally install [Zmbackup](https://github.com/lucascbeyeler/zmbackup) to backup and restore mailboxes and accounts;


Role Variables
--------------

* **hostname:** set the hostname of your server **WITHOUT** the domain;
* **domain:** set the domain for the server and the primary domain for your Zimbra server;
* **zmpasswd:** set the password used for every single service in your Zimbra server, like the admin account and the LDAPServer - **WARNING:** do not put special characters in the password during the install;
* **zmnetwork:** set the network the Zimbra server is, in CIDR notation (like 192.168.122.0/24);
* **zmlogologin:** Inform the path for your logo (Login Screen) - don't inform and no image will be applied;
* **zmlogoapp:** Inform the path for your logo (Application Screen) - don't inform and no image will be applied;
* **timezone:** inform the timezone the playbook should set in your server;
* **zimbra_version:** Inform which version of Zimbra you want to install, like **10.1.15** or **8.8.15**. It must be a key of **zm_repo**. Default: **8.8.15**
* **zimbra_download_validate_certs:** Validate the TLS certificate of the server Zimbra is downloaded from. Default: **true**
* **zimbra_rbls:** DNS blocklists the MTA checks before accepting a message. Default: **zen.spamhaus.org** and **bl.spamcop.net**
* **zimbra_rbls_absent:** DNS blocklists removed from the MTA. Default: **dsn.rfc-ignorant.org** and **dnsbl.sorbs.net**, which were shut down and were added by older versions of this role
* **zimbra_kam_url:** Where Kevin McGrail's SpamAssassin rules (KAM.cf) are downloaded from
* **zm_repo:** Variable to inform which repository of Zimbra builds you want to download from. For each version, you need to set **url**, and a dictionary of **builds** according to distribution and distribution major version. The role downloads `<url><build>.tgz`. The distribution is Ansible's `ansible_distribution` in lower case (`ubuntu`, `redhat`, `centos`, `rocky`, `almalinux`, `oraclelinux`...). The default has the 8.8.15 builds. When you set it, keep the 8.8.15 entry if you still need it, because your value replaces the default.
Example:
```
zm_repo:
  10.1.15:
    url: https://example.repositorio.zimbra
    builds:
      ubuntu:
        20: zcs-10.1.15_GA_0425.UBUNTU20_64...
        22: zcs-10.1.15_GA_0425.UBUNTU22_64....
      redhat:
        8: ...
        9: ...
      centos:
        8: ...
        9: ...
```
* **disable_existing_dns_stub_listener:** Inform "y" to disable the systemd-resolved DNS stub listener and free up port 53. Default: **n**

* **zimbra_upgrade:** Inform "y" to upgrade an existing Zimbra installation. Zimbra will be upgraded to **zimbra_version** version. See [Upgrading Zimbra](#upgrading-zimbra). Default: **n**

Service Variables - Inform "y" or "n"
--------------

The "y"/"n" variables also accept "yes"/"no" and booleans (true/false).

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
* **zimbra_chat:**  Enable Zimbra Chat - **Zimbra 8.8.15 only** - default: **n**
* **zimbra_drive:**  Enable Zimbra ownCloud Drive - **Zimbra 8.8.15 only** - default: **n**
* **zimbra_imapd:** Enable Zimbra IMAPD Solo Service **BETA** - **Zimbra 8.8.15 only** - default: **n**
* **zimbra_policyd:**  Enable Zimbra PolicyD Service - default: **n**
* **zimbra_zmbackup:**  Install [Zmbackup](https://github.com/lucascbeyeler/zmbackup) - default: **n**

The installers of Zimbra 10.x do not have Chat, Drive and IMAPD, so **zimbra_chat**, **zimbra_drive** and **zimbra_imapd** are ignored when **zimbra_version** is not 8.8.15.

Installing Zimbra 10.1
--------------

Set **zimbra_version** and add the 10.1 builds to **zm_repo**:

```
zimbra_version: 10.1.15
zm_repo:
  10.1.15:
    url: https://downloads.example.com/zimbra/10.1.15/
    builds:
      ubuntu:
        22: zcs-10.1.15_GA_0425.UBUNTU22_64.20250624000000
      rocky:
        9: zcs-10.1.15_GA_0425.RHEL9_64.20250624000000
```

Use the version and build names of the installers you have; the ones above are only an example. The role runs the installer, then configures the proxy, the mailbox and the MTA the same way it does for 8.8.15.

Upgrading Zimbra
--------------

To upgrade a server, for example from 8.8.15 or 10.0 to 10.1:

1. Back up the server (Zmbackup can help) and read Zimbra's release notes and upgrade instructions for the new version, which may require a newer distribution;
2. Set **zimbra_version** to the new version, make sure **zm_repo** has its build for your distribution, and set **zimbra_upgrade: y**;
3. Run the playbook. The role downloads the new installer and runs it over the existing installation. The proxy, mailbox and MTA settings are not reapplied during the upgrade;
4. Set **zimbra_upgrade** back to **n**, so the next runs do not run the installer again, and run the playbook once more to apply the configuration.

Zmbackup Variables - only used when zimbra_zmbackup is "y"
--------------

Zmbackup is downloaded from Git and installed with its unattended installer (`install-java.sh --unattended`) once Zimbra is installed and running. It installs a Java 17 JDK when one is missing and builds Zmbackup on the server, so the server needs internet access, and the distribution must provide a Java 17 JDK package (openjdk-17-jdk or java-17-openjdk-devel). If Zmbackup is already installed, it is upgraded only when the downloaded source changes (for example, after you change **zmbackup_version**). Its configuration is left as it is.

* **zmbackup_repo:** Git repository Zmbackup is downloaded from - default: **https://github.com/lucascbeyeler/zmbackup.git**
* **zmbackup_version:** Branch, tag or commit of Zmbackup to install. It must include the unattended installer - default: **2.0**
* **zmbackup_src_dir:** Where the Zmbackup source is downloaded and built - default: **/usr/local/src/zmbackup**
* **zmbackup_server_address:** Zimbra server name Zmbackup connects to. It must match the server's TLS certificate - default: **{{ hostname }}.{{ domain }}**
* **zmbackup_admin_user:** Zimbra admin account Zmbackup uses to export and restore mailboxes - default: **admin@{{ domain }}**
* **zmbackup_admin_password:** Password of **zmbackup_admin_user** - default: **{{ zmpasswd }}**
* **zmbackup_backup_dir:** Where the backups are stored - default: **/opt/zimbra/backup**
* **zmbackup_metadata_dir:** Local directory for Zmbackup's metadata database and lock file. Recommended when **zmbackup_backup_dir** is a network share - default: **""** (same as **zmbackup_backup_dir**)
* **zmbackup_mail_alert:** Account that receives Zmbackup's alerts - default: **admin@{{ domain }}**
* **zmbackup_mail_sender:** Account Zmbackup sends its alerts from - default: **root@{{ domain }}**
* **zmbackup_parallel_process:** Number of accounts backed up at the same time - default: **3**
* **zmbackup_rotate_days:** Number of days backups are kept - default: **30**
* **zmbackup_lock_backup:** Allow only one backup session per type per day - default: **true**

When Zimbra uses its self-signed certificate, set `caCertificatePath` in `/etc/zmbackup/zmbackup.yaml` before the first backup (see the Zmbackup README).

Testing
------------

GitHub Actions and CircleCI run ansible-lint, a syntax check, the unit tests and Molecule on every push. The role has two kinds of tests:

* **Unit tests** (`tests/unit/main.yml`) render the role's variables and templates (installer answers, installer configuration, Zmbackup settings) with mocked facts. They need neither a server nor Docker:
  ```
  ansible-playbook tests/unit/main.yml
  ```
* **Molecule** (`molecule/default`) runs the role from start to end, twice, in an Ubuntu container. Zimbra itself cannot run in a container, so the scenario installs a fake of it (`molecule/default/files/zcs-fake`) that records what the role asked of Zimbra, and checks it in `verify.yml`. It needs Docker:
  ```
  pip install -r requirements.txt
  ansible-galaxy collection install -r requirements.yml
  ansible-galaxy collection install community.docker
  molecule test
  ```

Dependencies
------------

To run this playbook, you will need to run [lucascbeyeler.baseline](https://github.com/lucascbeyeler/baseline) too. We do not cover any kind of server preparation, like upgrade the system or change the hostname (even put the hostname in /etc/hosts is made by baseline). The motive is because all my playbooks will need some kind of preparation before executed, so to not including the same code in every single project, I made a different playbook that will do everything that is considered "common" in each one of my playbooks.

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
           zimbra_zmbackup: y
```

Installing Zimbra 10.1 on a server prepared by baseline:
```
    - hosts: zimbra
      become: yes
      become_method: sudo
      roles:
         - role: lucascbeyeler.baseline
           hostname: mail
           domain: example.com
           timezone: America/Sao_Paulo
         - role: lucascbeyeler.zimbra
           hostname: mail
           domain: example.com
           timezone: America/Sao_Paulo
           zmpasswd: 123change
           zmnetwork: 192.168.122.0/24
           zimbra_version: 10.1.15
           zm_repo:
             10.1.15:
               url: https://downloads.example.com/zimbra/10.1.15/
               builds:
                 ubuntu:
                   22: zcs-10.1.15_GA_0425.UBUNTU22_64.20250624000000
```

License
-------

[![GNU GPL v3.0](http://www.gnu.org/graphics/gplv3-127x51.png)](http://www.gnu.org/licenses/gpl.html)

View official GNU site <http://www.gnu.org/licenses/gpl.html>.

Author Information
------------------

* [Lucas Costa Beyeler](https://github.com/lucascbeyeler) - lucas.costab@outlook.com
