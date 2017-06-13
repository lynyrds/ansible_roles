# Ansible roles

## Defaults
`defaults` role holds common handlers for other roles, has no tasks and should be included in all playbooks by default.

## Patch
`patch` role makes use of `package` module.
This role will 
* patch the node(s) to whatever latest packages available on the enabled repositories
* reboot if either kernel or glibc or ntpdate were patched
* wait until the node(s) will become reachable via ssh


### Prerequisites
* Ansible >= 2.1

### Example playbook
```yaml
---
- hosts: all
  become: True
  roles:
    - defaults
    - patch
```
