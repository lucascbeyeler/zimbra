"""Filters for the zimbra role."""

from ansible.errors import AnsibleFilterError

_TRUE = frozenset(('y', 'yes', 'true', 'on', '1'))
_FALSE = frozenset(('n', 'no', 'false', 'off', '0'))


def zimbra_bool(value):
    """Convert the role's y/n variables, yes/no and booleans to a boolean.

    The bool filter of ansible-core 2.19+ no longer accepts y and n.
    """
    if isinstance(value, bool):
        return value
    text = str(value).strip().lower()
    if text in _TRUE:
        return True
    if text in _FALSE:
        return False
    raise AnsibleFilterError(f"zimbra_bool: {value!r} is not y, n or a boolean")


class FilterModule:
    def filters(self):
        return {'zimbra_bool': zimbra_bool}
