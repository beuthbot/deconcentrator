#! /bin/bash
exec ansible -i inventory -u root "${@}"
