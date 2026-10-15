#!/usr/bin/env python3
"""A fake of the Zimbra commands the role runs, for the Molecule tests.

The command is picked by the name it is called with (zmprov, zmlocalconfig,
zmcontrol, zmproxyconfig or zmsetup.pl). LDAP and localconfig are kept in a
JSON file, and every call is logged with the user that made it.
"""
import json
import os
import pwd
import shutil
import sys
import time

STATE = '/opt/zimbra/.fake-state.json'
CALLS = '/opt/zimbra/log/fake-calls.log'
SEED = '/etc/fake-zimbra/seed.json'
LOCALCONFIG_DEFAULTS = {
    'antispam_enable_rule_updates': 'false',
    'antispam_enable_restarts': 'false',
    'antispam_enable_rule_compilation': 'false',
}


def user():
    return pwd.getpwuid(os.geteuid()).pw_name


def give_to_zimbra(path):
    if os.geteuid() == 0:
        zimbra = pwd.getpwnam('zimbra')
        os.chown(path, zimbra.pw_uid, zimbra.pw_gid)


def log_call(command, args):
    with open(CALLS, 'a') as calls:
        calls.write(json.dumps({'command': command, 'args': args, 'user': user(),
                                'time': time.time()}) + '\n')
    give_to_zimbra(CALLS)


def load():
    if not os.path.exists(STATE):
        return {'servers': {}, 'domains': {}, 'config': {}, 'localconfig': {}}
    with open(STATE) as state:
        return json.load(state)


def save(state):
    with open(STATE, 'w') as out:
        json.dump(state, out, indent=2, sort_keys=True)
    give_to_zimbra(STATE)


def fail(message, code=1):
    print(message, file=sys.stderr)
    sys.exit(code)


def require_zimbra_user(command):
    if user() != 'zimbra':
        fail(f'{command} must be run as zimbra, not {user()}')


def modify(entry, pairs):
    if len(pairs) % 2:
        fail('ERROR: zmprov: attribute without a value')
    for name, value in zip(pairs[::2], pairs[1::2]):
        if name.startswith('+'):
            values = entry.setdefault(name[1:], [])
            if value not in values:
                values.append(value)
        elif name.startswith('-'):
            values = entry.get(name[1:], [])
            if value in values:
                values.remove(value)
        else:
            entry[name] = [value]


def show(name, entry, attrs):
    print(f'# name {name}')
    for attr in attrs or sorted(entry):
        for value in entry.get(attr, []):
            print(f'{attr}: {value}')


def find(state, kind, name):
    if name not in state[kind]:
        fail(f'ERROR: account.NO_SUCH_{kind.upper()[:-1]} ({name})', 2)
    return state[kind][name]


def zmprov(args):
    require_zimbra_user('zmprov')
    state = load()
    command, rest = args[0], args[1:]
    if command == 'ms':
        modify(find(state, 'servers', rest[0]), rest[1:])
    elif command == 'md':
        modify(find(state, 'domains', rest[0]), rest[1:])
    elif command == 'mcf':
        modify(state['config'], rest)
    elif command == 'gs':
        show(rest[0], find(state, 'servers', rest[0]), rest[1:])
    elif command == 'gd':
        show(rest[0], find(state, 'domains', rest[0]), rest[1:])
    elif command == 'gcf':
        show('config', state['config'], rest)
    else:
        fail(f'fake zmprov does not know {command}')
    save(state)


def zmlocalconfig(args):
    require_zimbra_user('zmlocalconfig')
    state = load()
    localconfig = dict(LOCALCONFIG_DEFAULTS, **state['localconfig'])
    if args and args[0] == '-e':
        for setting in args[1:]:
            key, value = setting.split('=', 1)
            state['localconfig'][key] = value
        save(state)
    else:
        for key in args:
            print(f'{key} = {localconfig.get(key, "")}')


def zmcontrol(args):
    require_zimbra_user('zmcontrol')
    if args != ['restart']:
        fail(f'fake zmcontrol does not know {args}')
    open('/opt/zimbra/log/fake-running', 'w').close()


def zmproxyconfig(args):
    require_zimbra_user('zmproxyconfig')
    if args[:3] != ['-e', '-w', '-C'] or args[3] != '-H':
        fail(f'fake zmproxyconfig does not know {args}')
    state = load()
    modify(find(state, 'servers', args[4]), ['zimbraReverseProxyAdminEnabled', 'TRUE'])
    save(state)


def zmsetup(args):
    if user() != 'root':
        fail('zmsetup.pl must be run as root')
    if args[0] != '-c':
        fail(f'fake zmsetup.pl does not know {args}')
    shutil.copy(args[1], '/opt/zimbra/log/zmsetup-config')
    give_to_zimbra('/opt/zimbra/log/zmsetup-config')
    with open(args[1]) as config_file:
        config = dict(line.split('=', 1) for line in config_file.read().splitlines() if '=' in line)
    config = {key: value.strip('"') for key, value in config.items()}
    state = load()
    server = state['servers'].setdefault(config['HOSTNAME'], {})
    state['domains'].setdefault(config['CREATEDOMAIN'], {})
    # Settings an earlier version of the role left behind
    if os.path.exists(SEED):
        with open(SEED) as seed:
            for attr, values in json.load(seed).get('server', {}).items():
                server[attr] = list(values)
    save(state)
    open('/opt/zimbra/log/fake-running', 'w').close()
    give_to_zimbra('/opt/zimbra/log/fake-running')


COMMANDS = {
    'zmprov': zmprov,
    'zmlocalconfig': zmlocalconfig,
    'zmcontrol': zmcontrol,
    'zmproxyconfig': zmproxyconfig,
    'zmsetup.pl': zmsetup,
}

if __name__ == '__main__':
    name = os.path.basename(sys.argv[0])
    log_call(name, sys.argv[1:])
    COMMANDS[name](sys.argv[1:])
