#!/bin/bash
# A fake of the Zimbra installer (install.sh -s), for the Molecule tests. It
# saves the answers it reads and installs fakezimbra.py as the Zimbra commands.
set -euo pipefail

[ "${1:-}" = "-s" ] || { echo "install.sh must be run with -s" >&2; exit 1; }
[ "$(id -un)" = "root" ] || { echo "install.sh must be run as root" >&2; exit 1; }
here=$(cd "$(dirname "$0")" && pwd)

getent passwd zimbra >/dev/null || useradd --system --home-dir /opt/zimbra --shell /bin/bash zimbra

mkdir -p /opt/zimbra/{bin,libexec,log,conf,fake} \
  /opt/zimbra/data/spamassassin/localrules /opt/zimbra/data/amavisd \
  /opt/zimbra/data/httpd/htdocs /opt/zimbra/common/share/webui/includes \
  /opt/zimbra/jetty/webapps/zimbra/img

install -m 0755 "$here/fakezimbra.py" /opt/zimbra/fake/fakezimbra.py
for command in zmprov zmlocalconfig zmcontrol; do
  ln -sf /opt/zimbra/fake/fakezimbra.py "/opt/zimbra/bin/$command"
done
for command in zmproxyconfig zmsetup.pl; do
  ln -sf /opt/zimbra/fake/fakezimbra.py "/opt/zimbra/libexec/$command"
done

echo 'export PATH=/opt/zimbra/bin:$PATH' > /opt/zimbra/.bashrc
printf '<IfModule dir_module>\n    DirectoryIndex index.html index.html.var\n</IfModule>\n' > /opt/zimbra/conf/httpd.conf

cat > /opt/zimbra/log/install-keystrokes
stat -c '%n %a %U' /tmp/zcs /tmp/zcs/installZimbra-keystrokes /tmp/zcs/installZimbraScript \
  > /opt/zimbra/log/install-files

chown -R zimbra:zimbra /opt/zimbra
