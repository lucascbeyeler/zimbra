Zimbra
=========

Non-Official ansible role to install, upgrade and configure Zimbra Collaboration Open Source Edition on Red Hat, CentOS and Ubuntu Server.

The role supports the latest version of Zimbra, **Zimbra 10.1 (Daffodil)**, as well as Zimbra 10.0. Zimbra 8.x is no longer supported.

[![CI](https://github.com/lucascbeyeler/zimbra/actions/workflows/ci.yml/badge.svg)](https://github.com/lucascbeyeler/zimbra/actions/workflows/ci.yml)
[![CircleCI](https://circleci.com/gh/lucascbeyeler/zimbra.svg?style=shield)](https://circleci.com/gh/lucascbeyeler/zimbra)
[![Zimbra Version](https://img.shields.io/badge/Zimbra-10.1%20%7C%2010.0-blue.svg)](https://www.zimbra.com/product/release-notes/)
![Linux Distro](https://img.shields.io/badge/platform-CentOS%20%7C%20Red%20Hat%20%7C%20Ubuntu-blue.svg)
![Branch](https://img.shields.io/badge/Branch-Master-green.svg)
[![Ansible Version](https://img.shields.io/badge/Ansible-2.15-green.svg)](https://www.ansible.com/)

Requirements
------------

* [Ansible](https://github.com/ansible/ansible) 2.15 or higher.
* The `ansible.posix` and `community.general` collections:
  ```
  ansible-galaxy collection install -r requirements.yml
  ```
* A server prepared by [lucascbeyeler.baseline](https://github.com/lucascbeyeler/baseline) (see [Dependencies](#dependencies)).

Supported Zimbra Versions
--------------

| Zimbra | Installer builds | Distributions |
|---|---|---|
| **10.1** (latest, default) | Built from source, or set in **zm_repo** | Ubuntu 20.04 and 22.04, Red Hat / CentOS / Rocky 8 and 9 |
| **10.0** | Built from source, or set in **zm_repo** | Ubuntu 20.04 and 22.04, Red Hat / CentOS / Rocky 8 and 9 |

The distributions are the ones each Zimbra version supports.

Zimbra does not publish the 10.x installers of the Open Source Edition, so the role builds the installer from Zimbra's source code on the server, with Zimbra's own build tool. See [Building Zimbra from source](#building-zimbra-from-source). If you already have the installers (your own build or a mirror), set them in **zm_repo** and the role downloads them instead. See [Installing Zimbra 10.1](#installing-zimbra-101).

Zimbra 8.8.15 and older are no longer supported: the role stops with a message when **zimbra_version** is older than 10.0. To keep using Zimbra 8.8.15, use an older release of this role.

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

* Install Zimbra 10.1 or 10.0, with only the services you choose;
* Upgrade an existing Zimbra installation to a newer version (**zimbra_upgrade**);
* Run many times you want to apply the configuration - installation only occur if the server has no Zimbra installed, every setting is changed only when it differs from what you asked, and Zimbra is restarted only when something changed;
* Build the Zimbra installer from source when you have none;
* Optionally open the ports of the enabled services in firewalld (Red Hat family) or ufw (Ubuntu) (**zimbra_firewall**);
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
* **zimbra_version:** Inform which version of Zimbra you want to install, like **10.1.15** or **10.0.0**. It must be 10.0 or newer, in the form major.minor.patch. Default: **10.1.15**
* **zimbra_download_validate_certs:** Validate the TLS certificate of the server Zimbra is downloaded from. Default: **true**
* **zimbra_rbls:** DNS blocklists the MTA checks before accepting a message. Default: **zen.spamhaus.org** and **bl.spamcop.net**
* **zimbra_rbls_absent:** DNS blocklists removed from the MTA. Default: **dsn.rfc-ignorant.org** and **dnsbl.sorbs.net**, which were shut down and were added by older versions of this role
* **zimbra_kam_url:** Where Kevin McGrail's SpamAssassin rules (KAM.cf) are downloaded from
* **zm_repo:** Variable to inform which repository of Zimbra builds you want to download from. For each version, you need to set **url**, and a dictionary of **builds** according to distribution and distribution major version. The role downloads `<url><build>.tgz`. The distribution is Ansible's `ansible_distribution` in lower case (`ubuntu`, `redhat`, `centos`, `rocky`, `almalinux`, `oraclelinux`...). When it has no build of **zimbra_version** for the server's distribution, the role builds the installer from source. Default: empty
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

Firewall Variables
--------------

With **zimbra_firewall: y**, the role opens the ports of the services you enabled with firewalld (`firewall-cmd`) on Red Hat, CentOS, Rocky and the other distributions of the Red Hat family, and with ufw on Ubuntu. The firewall must already be installed; the role does not install, enable or start it. When firewalld is stopped the ports are saved in its permanent configuration, and when ufw is disabled it keeps the rules, so they apply once the firewall starts. Ports are only opened, never closed.

| Service | Ports |
|---|---|
| **zimbra_mta** | 25 (SMTP), 465 (SMTPS), 587 (Submission) |
| **zimbra_proxy** or **zimbra_store** | 80 (HTTP), 443 (HTTPS), 110 (POP3), 995 (POP3S), 143 (IMAP), 993 (IMAPS) |
| **zimbra_store**, with **zimbra_firewall_admin** | 7071 (admin console) |
| **zimbra_proxy**, with **zimbra_firewall_admin** | 9071 (admin console through the proxy) |

* **zimbra_firewall:** Inform "y" to open the ports of the enabled services in the firewall - default: **n**
* **zimbra_firewall_admin:** Inform "n" to keep the admin console ports (7071 and 9071) closed - default: **y**
* **zimbra_firewall_zone:** firewalld zone the ports are opened in. Ignored by ufw - default: **""** (firewalld's default zone)
* **zimbra_firewall_extra_ports:** Other ports to open, as `port/protocol`, like `389/tcp` for the LDAP of a multi-server setup - default: **[]**

Opening the ports on Red Hat needs the `ansible.posix` collection, which is in `requirements.yml`.

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
* **zimbra_policyd:**  Enable Zimbra PolicyD Service - default: **n**
* **zimbra_zmbackup:**  Install [Zmbackup](https://github.com/lucascbeyeler/zmbackup) - default: **n**

Building Zimbra from source
--------------

When **zm_repo** has no installer of **zimbra_version** for the server's distribution, which is the case with the defaults, the role builds one from source on the server before installing it:

1. Installs the build tools: a Java 8 JDK, Ant, Maven, Ruby, Git, compilers and the packaging tools (**zimbra_source_packages_debian** or **zimbra_source_packages_redhat**);
2. Creates the user **zimbra_source_user**, so the build does not run as root;
3. Downloads [zm-build](https://github.com/Zimbra/zm-build), Zimbra's build tool, at the newest tag up to **zimbra_version** (each component is only tagged in the patches that changed it, so 10.1.15 may use the 10.1.13 tag);
4. Runs zm-build's `build.pl`, which downloads the source of every Zimbra component from GitHub at the newest tag up to **zimbra_version**, the third-party packages from **zimbra_source_thirdparty_server**, and builds the installer:
   ```
   ./build.pl --ant-options -DskipTests=true --git-default-tag=10.1.15,10.1.14,...,10.1.0,10.1.0-GA \
     --build-release-no=10.1.15 --build-release=LIBERTY --build-release-candidate=GA --build-type=FOSS \
     --build-thirdparty-server=files.zimbra.com --no-interactive
   ```
5. Installs Zimbra with the installer it built, like a downloaded one.

The build can take over an hour and needs several GB of free disk, and the server needs to reach GitHub, Maven Central and **zimbra_source_thirdparty_server**. Its log is in `<zimbra_source_dir>/<zimbra_version>/build.log`. The installer is kept in `<zimbra_source_dir>/<zimbra_version>/BUILDS`, so running the playbook again does not build it again; you can delete the folder once Zimbra is installed.

On Red Hat and its derivatives, some build packages may only be in the CodeReady Builder repository (CRB, or PowerTools on 8). If installing them fails, enable it (`dnf config-manager --set-enabled crb`) or change **zimbra_source_packages_redhat**.

To build once and install on many servers, build on one server, copy the `zcs-*.tgz` from `BUILDS` to a web server and set it in **zm_repo** for the others.

* **zimbra_source_repo:** Git repository of zm-build - default: **https://github.com/Zimbra/zm-build.git**
* **zimbra_source_thirdparty_server:** Server the third-party packages are downloaded from - default: **files.zimbra.com**
* **zimbra_source_release:** Release name in the build, only used to name the build folders - default: **LIBERTY**
* **zimbra_source_dir:** Where the sources are downloaded and built, one folder for each version. It is also the home of **zimbra_source_user** - default: **/usr/local/src/zimbra-build**
* **zimbra_source_user:** User that builds Zimbra - default: **zmbuild**
* **zimbra_source_build_timeout:** Seconds the build may take - default: **14400**
* **zimbra_source_packages_debian** / **zimbra_source_packages_redhat:** Packages installed to build Zimbra
* **zimbra_source_java_home:** The Java 8 JDK the build uses - default: **/usr/lib/jvm/java-8-openjdk-amd64** on Ubuntu, **/usr/lib/jvm/java-1.8.0** on Red Hat

Installing Zimbra 10.1
--------------

Set **zimbra_version** to the version you want. With nothing else set, the role builds it from source. To use installers you already have, add their builds to **zm_repo**:

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

Use the version and build names of the installers you have; the ones above are only an example. The role runs the installer, then configures the proxy, the mailbox and the MTA.

Upgrading Zimbra
--------------

To upgrade a server, for example from 10.0 to 10.1:

1. Back up the server (Zmbackup can help) and read Zimbra's release notes and upgrade instructions for the new version, which may require a newer distribution;
2. Set **zimbra_version** to the new version and **zimbra_upgrade: y**. Add its build to **zm_repo**, or leave it out to build it from source;
3. Run the playbook. The role downloads or builds the new installer and runs it over the existing installation. The proxy, mailbox and MTA settings are not reapplied during the upgrade;
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
* **Molecule** runs the role from start to end, twice, in an Ubuntu container. Zimbra itself cannot run in a container, so the scenarios install a fake of it (`molecule/default/files/zcs-fake`) that records what the role asked of Zimbra, and check it in `verify.yml`. The `default` scenario downloads the installer set in **zm_repo**, and the `source` scenario builds it with a fake of zm-build (`molecule/default/files/zm-build`). It needs Docker:
  ```
  pip install -r requirements.txt
  ansible-galaxy collection install -r requirements.yml
  ansible-galaxy collection install community.docker
  molecule test --all
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
           zimbra_firewall: y
```

Installing Zimbra 10.1 from your own installers on a server prepared by baseline:
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
