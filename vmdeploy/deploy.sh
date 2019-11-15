#! /bin/bash
exec ansible-playbook -i inventory -u root setup.yml ${@}
