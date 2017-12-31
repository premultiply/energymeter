#!/bin/sh

rrdtool create em.rrd \
	--step '60' \
	'DS:energy0:ABSOLUTE:300:0:184' \
	'DS:power0:GAUGE:300:1:11040' \
	'DS:counter0:COUNTER:300:0:184' \
	'RRA:LAST:0.5:1:7680' \
	'RRA:AVERAGE:0.5:2:64800' \
	'RRA:AVERAGE:0.5:10:52560'
