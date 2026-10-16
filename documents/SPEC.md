# Zimbra Role Specification

`lucascbeyeler.zimbra` is a non-official Ansible role that installs,
upgrades and configures **Zimbra Collaboration Open Source Edition (OSE)**
on a single server, with only the Zimbra services the operator selects.

## 1. Scope

**In scope**

* Installing Zimbra OSE 10.0 or 10.1 from an installer archive, downloaded
  from `zm_repo` or built from source with Zimbra's zm-build;
* Upgrading an existing installation to a newer version;
* Post-install configuration: proxy, mailbox, MTA, anti-spam, PolicyD,
  logos;
* Optionally freeing port 53 for `zimbra-dnscache`;
* Optionally opening the ports of the enabled services in firewalld or ufw;
* Optionally installing [Zmbackup](https://github.com/lucascbeyeler/zmbackup).

**Out of scope** (handled by [lucascbeyeler.baseline](https://github.com/lucascbeyeler/baseline))

* System upgrade, base packages, timezone/NTP;
* Hostname and the `127.0.1.1` line in `/etc/hosts`;
* SSH hardening.

Also out of scope: multi-server Zimbra topologies, TLS certificates,
installing or enabling a firewall, DNS records (MX/A) and Zimbra 8.x (use an
older release of the role for it).

## 2. Requirements

| Item | Value |
|---|---|
| Ansible | 2.15 or later (`meta/main.yml` → `min_ansible_version`) |
| Collections | `community.general` (`ini_file`, `ufw`) and `ansible.posix` (`firewalld`), in `requirements.yml` |
| Privileges | `become: true`; the target needs `acl` (or equivalent) so Ansible can become the `zimbra` user |
| Preparation | `lucascbeyeler.baseline` run first with the same `hostname`, `domain` and `timezone` |
| Galaxy name | `lucascbeyeler.zimbra` |

## 3. Supported versions and platforms

| Zimbra | Installer source | Distributions |
|---|---|---|
| 10.1 (latest, default `10.1.15`) | Built from source, or operator-supplied in `zm_repo` | Ubuntu 20.04/22.04, RHEL/CentOS/Rocky 8 and 9 |
| 10.0 | Built from source, or operator-supplied in `zm_repo` | Ubuntu 20.04/22.04, RHEL/CentOS/Rocky 8 and 9 |

Zimbra does not publish OSE 10.x installers. When `zm_repo` has a build of
`zimbra_version` for the host's distribution, the role downloads it;
otherwise it builds the installer from source on the host (§5.2).

Zimbra 8.8.15 and older are not supported: the role fails at the start when
`zimbra_version` is older than 10.0.

## 4. Variables

### 4.1 Boolean convention

Service and feature switches accept `y`/`n`, `yes`/`no`, `true`/`false`,
`on`/`off`, `1`/`0` and real booleans. They are always read through the
role's `zimbra_bool` filter (`filter_plugins/zimbra.py`), because the
`bool` filter of ansible-core 2.19+ no longer accepts `y`/`n`. Any other value
fails with `zimbra_bool: '<value>' is not y, n or a boolean`.

**Rule for contributors:** never use `| bool` on these variables; use
`| zimbra_bool`.

### 4.2 Server identity

| Variable | Default | Description |
|---|---|---|
| `hostname` | `localhost` | Short host name, without the domain |
| `domain` | `localdomain` | Primary mail domain; server name is `{{ hostname }}.{{ domain }}` |
| `zmpasswd` | `!23Change` | Password for the admin account and every internal service (LDAP, keystore…). Avoid special characters |
| `zmnetwork` | `192.168.200.0/24` | Trusted network (CIDR) added to `zimbraMtaMyNetworks`. Must have no host bits set |
| `timezone` | `UTC` | Default user timezone (`zimbraPrefTimeZoneId`) |
| `hosts_lines` | *undefined* | Optional extra lines added to `/etc/hosts` before installing |

### 4.3 Services selected in the installer

| Variable | Default | Package |
|---|---|---|
| `zimbra_ldap` | `y` | zimbra-ldap |
| `zimbra_logger` | `y` | zimbra-logger |
| `zimbra_mta` | `y` | zimbra-mta |
| `zimbra_dnscache` | `n` | zimbra-dnscache |
| `zimbra_snmp` | `n` | zimbra-snmp |
| `zimbra_store` | `y` | zimbra-store |
| `zimbra_apache` | `y` | zimbra-apache |
| `zimbra_spell` | `y` | zimbra-spell |
| `zimbra_memcached` | `y` | zimbra-memcached |
| `zimbra_proxy` | `y` | zimbra-proxy |
| `zimbra_policyd` | `n` | Enables the `cbpolicyd` service after install |
| `zimbra_zmbackup` | `n` | Installs Zmbackup |

The order of `zimbra_packages` in `vars/main.yml` is the order the
installer asks its questions; it must not be changed unless Zimbra's
installer changes.

### 4.4 Installer and upgrade

| Variable | Default | Description |
|---|---|---|
| `zimbra_version` | `10.1.15` | Version to install: 10.0 or newer, as `major.minor.patch` |
| `zm_repo` | `{}` | Installers to download, `{<version>: {url, builds: {<distro>: {<major>: <build>}}}}`. Download URL is `<url><build>.tgz`. `<distro>` is `ansible_distribution` lower-cased (`ubuntu`, `redhat`, `centos`, `rocky`, `almalinux`…). Without a build for the host, the installer is built from source |
| `zimbra_download_validate_certs` | `true` | Validate TLS when downloading the installer |
| `zimbra_upgrade` | `n` | Run the installer over an existing installation |
| `disable_existing_dns_stub_listener` | `n` | Disable systemd-resolved's stub listener (only applied with `zimbra_dnscache`) |

### 4.5 Building from source (only when `zm_repo` has no build)

| Variable | Default | Description |
|---|---|---|
| `zimbra_source_repo` | `https://github.com/Zimbra/zm-build.git` | Git repository of zm-build |
| `zimbra_source_thirdparty_server` | `files.zimbra.com` | Server of the third-party packages (OpenLDAP, Postfix, nginx…) |
| `zimbra_source_release` | `LIBERTY` | Release name passed to `build.pl`; only names the build folders |
| `zimbra_source_dir` | `/usr/local/src/zimbra-build` | Build root, one folder per version; home of the build user |
| `zimbra_source_user` | `zmbuild` | Unprivileged system user that runs the build |
| `zimbra_source_build_timeout` | `14400` | Seconds the build may take (`async`) |
| `zimbra_source_packages_debian` / `zimbra_source_packages_redhat` | Java 8 JDK, Ant, Maven, Ruby, Git, compilers, packaging tools | Build dependencies per family |
| `zimbra_source_java_home` | `/usr/lib/jvm/java-8-openjdk-amd64` (Debian) / `/usr/lib/jvm/java-1.8.0` (Red Hat) | `JAVA_HOME` of the build |

### 4.6 Firewall

| Variable | Default | Description |
|---|---|---|
| `zimbra_firewall` | `n` | Open the ports of the enabled services in firewalld (Red Hat family) or ufw (Ubuntu) |
| `zimbra_firewall_admin` | `y` | Also open the admin console: 7071 (with `zimbra_store`) and 9071 (with `zimbra_proxy`) |
| `zimbra_firewall_zone` | `""` | firewalld zone; empty for the default zone. Ignored by ufw |
| `zimbra_firewall_extra_ports` | `[]` | Other ports, as `port/protocol` (e.g. `389/tcp`) |

### 4.7 Anti-spam

| Variable | Default | Description |
|---|---|---|
| `zimbra_rbls` | `zen.spamhaus.org`, `bl.spamcop.net` | DNS blocklists added as `reject_rbl_client` |
| `zimbra_rbls_absent` | `dsn.rfc-ignorant.org`, `dnsbl.sorbs.net` | Shut-down blocklists removed if present |
| `zimbra_kam_url` | pccc.com `KAM.cf` | Kevin McGrail's SpamAssassin rules |
| `absent` | `postfix`, `sendmail` | Packages removed before install |
| `ubuntu` / `centos` | `razor`, `pyzor` / `pyzor`, `perl-Razor-Agent` | Anti-spam packages per family |

### 4.8 Logos

`zmlogologin` and `zmlogoapp` — local paths to the login and application
banner images. The logo step runs only when **both** are defined.

### 4.9 Zmbackup (only with `zimbra_zmbackup`)

| Variable | Default |
|---|---|
| `zmbackup_repo` | `https://github.com/lucascbeyeler/zmbackup.git` |
| `zmbackup_version` | `"2.0"` (branch/tag/commit with the unattended installer) |
| `zmbackup_src_dir` | `/usr/local/src/zmbackup` |
| `zmbackup_server_address` | `{{ hostname }}.{{ domain }}` (must match the TLS certificate) |
| `zmbackup_admin_user` / `zmbackup_admin_password` | `admin@{{ domain }}` / `{{ zmpasswd }}` |
| `zmbackup_backup_dir` | `/opt/zimbra/backup` |
| `zmbackup_metadata_dir` | `""` (same as the backup dir) |
| `zmbackup_mail_alert` / `zmbackup_mail_sender` | `admin@{{ domain }}` / `root@{{ domain }}` |
| `zmbackup_parallel_process` | `3` |
| `zmbackup_rotate_days` | `30` |
| `zmbackup_lock_backup` | `true` |

These are passed to the installer through `zmbackup_environment`.

### 4.10 Internal variables (`vars/main.yml`)

* `zimbra_server_name` — `{{ hostname }}.{{ domain }}`, used in every `zmprov` call;
* `zimbra_build` — the build for this host from `zm_repo`, empty if none
  (then the installer is built from source);
* `zimbra_source_tags` — the tags a version is built from, newest first
  (`10.1.15, 10.1.14, … 10.1.0, 10.1.0-GA`);
* `zimbra_source_build_dir` — `<zimbra_source_dir>/<zimbra_version>`;
* `zimbra_packages` — the ordered package selection for the installer;
* `zimbra_firewall_ports` — the ports opened by `zimbra_firewall`, from the
  enabled services (`zimbra_firewall_mta_ports`, `zimbra_firewall_mail_ports`,
  7071, 9071) plus `zimbra_firewall_extra_ports`;
* `zimbra_antispam_settings` — `zmlocalconfig` keys set to `true`;
* `zimbra_logo_settings` — domain attributes for the logos.

Legacy names (`hostname`, `domain`, `zmpasswd`, `ubuntu`, …) predate the
`zimbra_` prefix and are kept for compatibility; `.ansible-lint` skips
`var-naming[no-role-prefix]`. **New variables must use the `zimbra_` (or
`zmbackup_`) prefix.**

## 5. Behaviour

### 5.1 Flow (`tasks/main.yml`)

1. **Check the version**: fail when `zimbra_version` is older than 10.0.
   Then **detect** an existing install with `getent passwd zimbra`.
   `zimbra_run_installer` is true when the user does not exist **or**
   `zimbra_upgrade` is set.
2. **DNS stub listener** (`configure/disable_existing_dns_stub_listener.yml`,
   when `zimbra_dnscache` and `disable_existing_dns_stub_listener`): set
   `DNSStubListener=no`, link `/etc/resolv.conf` to
   `/run/systemd/resolve/resolv.conf`, restart systemd-resolved immediately.
3. **Firewall** (`configure/firewall.yml`, when `zimbra_firewall`): open
   `zimbra_firewall_ports` with `ansible.posix.firewalld` (permanent, and
   immediate only when firewalld runs; fails if it is not installed) or
   `community.general.ufw` (rules are kept while ufw is disabled). Ports are
   only opened, never closed, and the firewall is never installed or started.
4. **Dependencies** (`install/dependencies.yml`, when installing): remove
   Postfix/Sendmail; install Razor and Pyzor. On Ubuntu, if
   `apt-cache madison razor` finds nothing, install
   `software-properties-common` and enable the `universe` component.
5. **Zimbra** (`install/zimbra.yml`, when installing):
   1. choose the installer: `<url><build>.tgz` from `zm_repo` when it has a
      build for this distribution, otherwise build one from source
      (`install/source.yml`, §5.2);
   2. add `hosts_lines` to `/etc/hosts` if defined;
   3. unpack the installer into `/usr/local/src/`;
   4. render the keystroke answers and the `zmsetup.pl` configuration into
      `/tmp/zcs` (`root:root`, dir `0700`, files `0600`) — the upgrade
      templates when `zimbra_upgrade`;
   5. run `install.sh -s`, then `zmsetup.pl -c` (notifies *Restart Zimbra*);
   6. delete `/tmp/zcs`, which holds every password.
6. **Ansible temp dir** for the `zimbra` user: `/opt/zimbra/.ansible/tmp`
   (`zimbra:zimbra 0700`), because `/opt/zimbra` is owned by root.
7. **PolicyD** (`install/policyd.yml`): add `cbpolicyd` to
   `zimbraServiceInstalled` and `zimbraServiceEnabled`.
8. **Configuration** — skipped while `zimbra_upgrade` is set:
   * **Proxy** (`zimbra_proxy`): enable admin through the proxy with
     `zmproxyconfig -e -w -C -H`;
   * **Mailbox** (`zimbra_store`): `zimbraReverseProxyMailMode redirect`
     (HTTP→HTTPS) and `zimbraMtaLmtpHostLookup native`;
   * **MTA** (`zimbra_mta`): remove `zimbra_rbls_absent`, add `zimbra_rbls`;
     install `KAM.cf` as `sakam.cf` and `files/sauser.cf` (`zimbra:zimbra
     0440`); enable SpamAssassin rule updates, restarts and compilation;
     initialise Pyzor and Razor (discover/create/register) under
     `/opt/zimbra/data/amavisd`; for PolicyD, install `files/config.php`,
     link the web UI into `htdocs/webui` and add `index.php` to Apache's
     `DirectoryIndex`.
9. **Logos** (`extras/modify-logo.yml`, both logo vars defined): copy the
   images to Jetty's `img/` and set `zimbraSkinLogoURL`,
   `zimbraSkinLogoLoginBanner`, `zimbraSkinLogoAppBanner` on the domain.
10. **Flush handlers** — restart Zimbra now if anything changed.
11. **Zmbackup** (`install/zmbackup.yml`): clone `zmbackup_repo` at
    `zmbackup_version`; run `install-java.sh --unattended` if
    `/usr/local/lib/zmbackup/zmbackup.jar` is missing, or with
    `--force-upgrade` when the clone changed. It runs after the restart
    because it needs Zimbra up; existing Zmbackup configuration is not
    touched.

### 5.2 Building the installer from source (`install/source.yml`)

Runs only when `zm_repo` has no build of `zimbra_version` for the host:

1. assert `zimbra_version` is `major.minor.patch` and the host is Debian or
   Red Hat family;
2. install `zimbra_source_packages_debian` or `zimbra_source_packages_redhat`;
3. create the system user `zimbra_source_user` (home `zimbra_source_dir`)
   and `zimbra_source_build_dir`, owned by it;
4. if `<zimbra_source_build_dir>/BUILDS` already has a `zcs-*.tgz`, skip to
   step 7 — a rerun never builds again;
5. read zm-build's tags with `git ls-remote` and clone it, as the build user,
   at the first of `zimbra_source_tags` it has (fails if none). Zimbra tags
   each component only in the patches that changed it, so 10.1.15 may use
   zm-build 10.1.13;
6. run `build.pl` as the build user, with `ENV_CACHE_CLEAR_FLAG=true` and
   `JAVA_HOME=zimbra_source_java_home`, under `async`
   (`zimbra_source_build_timeout`, polled every 30 s), output in
   `<zimbra_source_build_dir>/build.log`:
   ```
   ./build.pl --ant-options -DskipTests=true
     --git-default-tag=<zimbra_source_tags joined by commas>
     --build-release-no=<zimbra_version> --build-release=<zimbra_source_release>
     --build-release-candidate=GA --build-type=FOSS
     --build-thirdparty-server=<zimbra_source_thirdparty_server>
     --build-destination-base-dir=<zimbra_source_build_dir>/BUILDS
     --no-interactive
   ```
   `build.pl` clones every component next to zm-build at the first of the
   tags it has, and needs GitHub, Maven Central and the third-party server;
7. fail if `BUILDS` has no `zcs-*.tgz`; otherwise use the newest one. Its
   top folder has the archive's name, as with downloaded builds.

The build tools and the build folder stay on the host after the install.

### 5.3 Configuration pattern

Every Zimbra setting follows the same read-then-write pattern:

1. a read task (`zmprov gs|gcf|gd`, `zmlocalconfig`) with
   `changed_when: false` and `check_mode: false`, registered;
2. a write task (`zmprov ms|mcf|md`, `zmlocalconfig -e`) guarded by
   `when: '<attr>: <value>' not in <read>.stdout_lines`, with
   `changed_when: true` and `notify: Restart Zimbra`.

Zimbra commands run from `/opt/zimbra/bin` (or `libexec`) with
`become_user: zimbra`. New settings must follow this pattern.

### 5.4 Handlers

| Handler | Action |
|---|---|
| Restart Zimbra | `zmcontrol restart` as `zimbra`, up to 3 retries 10 s apart |
| Restart systemd-resolved | restart the service |

### 5.5 Upgrade procedure

1. Back up and read Zimbra's release notes;
2. set `zimbra_version` to the new version (add its build to `zm_repo`, or
   leave it out to build it from source), set `zimbra_upgrade: y` and run — the installer runs over the existing
   install and configuration steps are skipped;
3. set `zimbra_upgrade: n` and run again to apply the configuration.

## 6. Guarantees

* **Install once** — the installer only runs when there is no `zimbra` user,
  or when an upgrade is asked for.
* **Idempotent** — settings change only when they differ; a second run
  reports no changes (checked by Molecule's `idempotence` step).
* **Restart only on change** — Zimbra is restarted at most once per run,
  and only when something changed.
* **Fail early** — an unsupported `zimbra_version` (older than 10.0) fails
  before anything changes on the host.
* **Build once** — an installer built from source is kept in
  `zimbra_source_build_dir` and reused by later runs; the build never runs
  as root.
* **Secrets** — installer files with passwords are root-only (`0600`) and
  removed after the install.
* **Firewall only opens** — `zimbra_firewall` adds rules for the enabled
  services and never removes any.

## 7. Testing

| Layer | Location | Command | Needs |
|---|---|---|---|
| Lint | `.ansible-lint` | `ansible-lint` | Python |
| Syntax | `tests/test.yml` | `ansible-playbook -i tests/inventory tests/test.yml --syntax-check` | Checkout folder named `zimbra` and `ansible.cfg` with `roles_path=../` |
| Unit | `tests/unit/main.yml` | `ansible-playbook tests/unit/main.yml` | Ansible only |
| Integration | `molecule/default`, `molecule/source` | `molecule test --all` | Docker |

* **Unit tests** cover `zimbra_bool` (valid and invalid values), build lookup
  per distribution and for missing versions, the source tags, build folder
  and `JAVA_HOME`, the supported versions, the keystrokes, the installer
  configuration and package list, the firewall ports, the default network, RBLs,
  disabled-by-default features, the Zmbackup environment and the logo
  settings.
* **Molecule** runs each scenario in an `ubuntu:jammy` container. Real Zimbra cannot run in
  a container, so `prepare.yml` serves a **fake Zimbra installer**
  (`molecule/default/files/zcs-fake`) and fake KAM rules over HTTP on
  `127.0.0.1:8000`, installs fake `pyzor`/`razor-admin` and `ufw`, creates a
  local Zmbackup git repo with a `2.0` branch and a local zm-build repo with
  a fake `build.pl` (`molecule/default/files/zm-build`) tagged `10.1.13` and
  `10.1.16`, removes `universe` from APT sources
  and seeds the old RBLs. The fake `zmprov`/`zmlocalconfig`/`zmcontrol`/
  `zmproxyconfig`/`zmsetup.pl` keep state in JSON and log every call with its
  user. `verify.yml` asserts on that log and state: only `zmsetup.pl` ran as
  root, one restart, the installer answers and configuration, installer
  files removed, server/domain attributes, file permissions, PolicyD links,
  universe enabled, ufw rules, Zmbackup installed once.
* `molecule/default` installs from `zm_repo`. `molecule/source` uses the same
  prepare, converge and checks with no `zm_repo`, and also checks that
  zm-build was cloned at `10.1.13` for 10.1.15, `build.pl` ran once as
  `zmbuild` with the expected options and environment, and its installer was
  unpacked.

When the role starts calling a new Zimbra command or attribute, extend
`fakezimbra.py` so Molecule can exercise it.

## 8. CI/CD

Both systems run on every push:

* **GitHub Actions** (`.github/workflows/ci.yml`, also on pull requests):
  `lint-and-unit-tests` (lint, syntax, unit) and `molecule` (all scenarios).
* **CircleCI** (`.circleci/config.yml`): `lint` and `molecule` (all
  scenarios).

Publishing to Ansible Galaxy is not automated in this repository.
