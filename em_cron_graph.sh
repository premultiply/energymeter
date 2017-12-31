#!/bin/sh

rrdtool graph /var/www/html/em_graph.png \
	--imgformat PNG \
	--title 'Energiemessung' \
	--vertical-label 'Wirkleistung [W]' \
	--width 960 --height 505 \
	--start end-16h --step 60 \
	--units-exponent 0 \
	--upper-limit 11040 --lower-limit 0 --rigid \
	'DEF:'d0=em.rrd':energy0:LAST' \
	'DEF:'d1=em.rrd':power0:LAST' \
	'CDEF:cd0=d0,3600,*' \
	'CDEF:cd0sum=d0,1000,/' \
	'CDEF:cd0price=d0,0.0002586,*' \
	'CDEF:cd0avg=d0,900,TREND,3600,*' \
	'VDEF:vd0max=cd0,MAXIMUM' \
	'VDEF:vd0last=cd0,LAST' \
	'VDEF:vd0avg=cd0avg,LAST' \
	'VDEF:vd0total=cd0sum,TOTAL' \
	'VDEF:vd0price=cd0price,TOTAL' \
	'AREA:cd0#0000FFBF:AVG 1 Min' \
	'LINE2:cd0avg#FF0000BF:AVG 15 Min' \
	'LINE1:d1#00FF00BF:PEAK 1 Min' \
	'GPRINT:vd0max:MAX\: %3.lf W' \
	'GPRINT:vd0avg:AVG 15m\: %3.lf W' \
	'GPRINT:vd0last:LAST\: %3.lf W' \
	'GPRINT:vd0total:SUM\: %6.3lf kWh' \
	'GPRINT:vd0price:TOTAL\: %4.2lf EUR' > /dev/null

