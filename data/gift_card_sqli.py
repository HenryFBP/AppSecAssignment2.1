# this line:
#         card_query = Card.objects.raw('select id from LegacySite_card where data = \'%s\'' % signature) # XXX sqli
# is vulnerable to sqli.


payload="'; DROP TABLE users; COMMIT;--"
print('select id from LegacySite_card where data = \'%s\'' % payload)