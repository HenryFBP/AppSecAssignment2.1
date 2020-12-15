from os import system

CARD_PARSER='giftcardreader'

# user input
card_fname='.gft; gedit potato.txt; echo "look ma!"; echo "" '

card_file_path = f'/tmp/{card_fname}_0_parser.gftcrd' # XXX path manipulation

command = "./{} 2 {} > tmp_file".format(CARD_PARSER,card_file_path)

print(command)

system(command)