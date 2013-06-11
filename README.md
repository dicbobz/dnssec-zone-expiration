dnssec-zone-expiration
======================

Python based nagios check to alert when <n> number of days are left before the DNSSEC zone RRSIG expires.

Takes 3 required parameters

--domain/-d domain.tld  -- This is specifing the zone to query when we resolve the dnssec record
--warn/-w value  -- Number of day until RRSIG key expires to alert w/ WARNING state.
--crit/-c value  -- Number of day until RRSIG key expires to alert w/ CRITCAL state.

This script is written to handle multiple records returned from the query.  In turn the alert will
fire off if any zones key expiration expire within the waring and critical threshold.

The nameserver is hardcode for ease and I'm lazy
