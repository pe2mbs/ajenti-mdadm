#!/bin/bash

if [ "$(whoami)" != 'root' ]; then 
	echo you are using a non-privileged account 
	exit 1
fi


ARG1=$1
echo "argument ${ARG1}"

if [[ -n ${ARG1} || "${ARG1}" -ne "" ]]; then 
 	if [ "${ARG1}" == "create" ]; then
		# 4.3 Gb image
		if [ -a /virtual0.vd ]; then 
			echo "Image file /virtual0.vd allready exists"
			exit
		fi 
		echo "Writing image file /virtual0.vd"
		dd if=/dev/zero of=/virtual0.vd count=8M
		if [ -a /virtual0.vd ]; then 
			echo "Image file /virtual1.vd allready exists"
			exit
		fi
		echo "Writing image file /virtual1.vd"
		dd if=/dev/zero of=/virtual1.vd count=8M    
	fi
	if [ "${ARG1}" == "stop" ]; then
		losetup --detach /dev/loop0
		losetup --detach /dev/loop1
	fi
	if [ "${ARG1}" == "show" ]; then
		losetup /dev/loop0
		losetup /dev/loop0
	fi
	if [[ "${ARG1}" == "start" || "${ARG1}" == "create" ]]; then
		losetup /dev/loop0 /virtual0.vd
		losetup /dev/loop1 /virtual1.vd
		partprobe /dev/loop0 >> /dev/null
		partprobe /dev/loop1 >> /dev/null
	fi
	
else
	echo "no command given"
fi
exit
