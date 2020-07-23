Keymonger
=========

[![Build Status](https://travis-ci.com/vantaworks/python-keymonger.svg?branch=master)](https://travis-ci.com/vantaworks/python-keymonger)

A very simple SSH keymanagement utility. In a nutshell, you provide it with a config that maps user with SSH keys available though GitHub or GitLab, and it will manage that user's authorized keys accordingly.

This is project is currently in a early beta stage; however, if that doesn't scare you off, then below is the quickest way to get started.

```
git@github.com:vantaworks/python-keymonger.git
make install
$EDITOR /etc/keymonger.conf
keymonger -c /etc/keymonger.conf
```

### Example config files

##### All in one
/etc/keymonger.conf
```
[global]
set_permissions=yes
verbose_logging=yes
idempotency_check=yes

[user]
; can take a comma delimited list without spaces for multiple sources
key_sources = https://github.com/user.keys
; this destination is optional since keymonger will guess this.
key_destination = /home/user/.ssh/authorized_keys
```

##### Using keymonger.d config imports
/etc/keymonger.conf
```
[global]
set_permissions=yes
verbose_logging=yes
idempotency_check=yes
include_config=/etc/keymonger.d/*.conf
```

/etc/keymonger.d/user.conf
```
[user]
key_sources = https://github.com/user.keys
key_destination = /home/user/.ssh/authorized_keys
```


Example config files are in the `examples/` directory to get you started.