#!/bin/bash

sudo service lldpd start

while true; do
	sudo lldpcli show neighbors
	sleep 5
done

sudo service lldpd stop