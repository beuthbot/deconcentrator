#! /bin/sh

FILES="secret.key postgres.passwd"
ACTION="$(basename ${0})"

case ${ACTION} in
	build)
		docker-compose -f docker-compose.yml -f docker-compose.build.yml -f docker-compose.develop.yml build; 
		;;

	prepare)
		for file in ${FILES}; do
			[ -f "${file}" ] && continue
			pwgen -s 80 1 > ${file}
		done
		;;

	run)
		./build
		./prepare
		docker-compose -f docker-compose.yml -f docker-compose.build.yml -f docker-compose.develop.yml run ${@}
		;;

	up)
		./prepare
		docker-compose -f docker-compose.yml -f docker-compose.build.yml -f docker-compose.develop.yml up ${@}
		;;

	down)
		docker-compose -f docker-compose.yml -f docker-compose.build.yml -f docker-compose.develop.yml down -v
		;;

	cleanup)
		./down
		rm -vf ${FILES}
		;;

	*)
		echo "Don't treat me like that! '${ACTION}' unknown" >&2
		exit 1
		;;
esac
