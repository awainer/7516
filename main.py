import scanner
scanner = scanner.Scanner("ejemplos/BIEN-00.PL0") 

token = scanner.next_token()
while token:
    print token
    token = scanner.next_token()