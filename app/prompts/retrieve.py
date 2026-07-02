BNS_QUERY = """
Reported incident:
{offence}

Find the core BNS offence section that directly defines the main criminal act in the incident.

Prioritize:
- the basic offence section
- the section title matching the main offence
- the legal definition of the offence
- the punishment for that same offence

Do not prioritize aggravated, organised, abetment, attempt, conspiracy, negligent conduct, weapon, poison, explosive, forgery, or special-form sections unless those facts are clearly present in the incident.
"""

BNSS_QUERY = """
Reported incident:
{offence}

Find only BNSS procedural sections relevant after an offence is reported.

Prioritize:
- FIR or complaint procedure
- police investigation
- search or recovery of stolen/property-related evidence, if relevant
- jurisdiction or place of trial
- cognizance by Magistrate

Do not retrieve unrelated arrest, trial, appeal, repeal, savings, or punishment table sections unless directly needed.
"""