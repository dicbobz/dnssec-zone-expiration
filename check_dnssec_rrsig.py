#!/usr/bin/python
#Author: rbryce@mozilla.com
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import dns.flags
import dns.resolver
import dns.rdatatype
import dns.rdataclass
import argparse
import datetime, time
import sys
#setup argparse
parser = argparse.ArgumentParser(description="Command Line Arguments go here")
parser.add_argument('--domain','-d', action='store', type=str, nargs=1, required=True, help='The domain of the record you wish to query')
parser.add_argument('--warn','-w', action='store', type=int, nargs=1, required=True, help='Number of days to warn')
parser.add_argument('--crit','-c', action='store', type=int, nargs=1, required=True, help='Number of days to critical')
parser.add_argument('--nsrv','-d', action='store', nargs=1, required=False, help='Optional NS Server', default=[8.8.8.8])
args = parser.parse_args()
wt = args.warn[0]
ct = args.crit[0]
name_server = args.nsrv[0]
#Parameters
domain_name = dns.name.from_text(args.domain[0]) #Take from argument
crit = 0
warn = 0
ok = 0
#Setup Resolver
rdtype = dns.rdatatype.DNSKEY
resolver = dns.resolver.Resolver()
resolver.use_edns(0,dns.flags.DO,4096)
resolver.nameservers = ([name_server])


# Get dns RRSIG
def get_rrsig():
	try:
        	response = resolver.query(domain_name, rdtype, dns.rdataclass.IN,True).response
        	rrsig = response.find_rrset(response.answer, domain_name, dns.rdataclass.IN, dns.rdatatype.RRSIG, rdtype)
		return rrsig
                
	except dns.resolver.NoAnswer:
        	print 'no answer returned' 
        	sys.exit(3)
	except dns.resolver.NXDOMAIN:
        	print 'NXDOMAIN'
        	sys.exit(3)

def comp_days(date):
	from time import mktime
	from datetime import datetime
	l = time.strptime(date, '%Y%d%m%H%M%S')
	now = datetime.now()
	later = datetime.fromtimestamp(mktime(l))
	then = later - now # Find time till expiration in datetime format
        day = then.days 
	days = int(day)
	return days

def set_status(days):
	global crit,warn,ok
	if int(days) <= ct:
		crit = crit + 1
	if int(days) <= wt and int(days) >= ct:
		warn = warn + 1
	else:
		ok = ok + 1
	return crit, warn, ok
def alert_nagios(crit,warn):
	if crit > 0:
		print "CRITICAL: %d days until a RRSIG expires for %s" % (dd, args.domain[0])
		sys.exit(1)
	if warn > 0:
		print "WARNING: %d days until a RRSIG expires for %s" % (dd, args.domain[0])
		sys.exit(2)
	else:
                print "Ok: %d days until a RRSIG expires for %s" % (dd, args.domain[0])
                sys.exit(0)

if __name__ == '__main__':
	rrsig = get_rrsig()
	for lines in rrsig:
		line = str(lines)
                ss = line.split()  #split out datestamp
		date = ss[4]
		dd = comp_days(date)
		set_status(dd)
	alert_nagios(crit,warn)
