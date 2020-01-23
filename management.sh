#! /bin/bash

FILES="secret.key postgres.passwd"
ACTION="$(basename ${0})"
SELF="$(realpath ${ACTION})"

if [ "management.sh" == "${ACTION}" ]; then
	ACTION="${1}"
	shift
fi

function dc() {
	exec docker-compose -f docker-compose.yml -f docker-compose.build.yml -f docker-compose.develop.yml ${@}
}

case "${ACTION}" in
	prepare)
		for file in ${FILES}; do
			[ -f "${file}" ] && continue
			pwgen -s 80 1 > ${file}
		done
		;;

	cleanup)
		set -e
		${SELF} down -v
		exec rm -vf ${FILES}
		;;

	*)
		set -ex
		dc ${ACTION} ${@}

esac
