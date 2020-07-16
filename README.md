Keymonger
=========

[![Build Status](https://travis-ci.com/vantaworks/python-keymonger.svg?branch=master)](https://travis-ci.com/vantaworks/python-keymonger)

A very simple SSH keymanagement utility. In a nutshell, you provide it with a config that maps user with SSH keys available though GitHub or GitLab, and it does the rest.

This is project is currently in a early beta stage; however, if that doesn't scare you off, then below is the quickest way to get started.

```
git@github.com:vantaworks/python-keymonger.git
make install
$EDITOR config.json
keymonger -v
```

Example config files are in the `examples/` directory to get you started.