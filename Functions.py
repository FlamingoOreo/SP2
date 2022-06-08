def salt_generator(password) -> str:
    reveresed = password[::-1]
    salt = ''
    for i in reveresed:
        salt += i
        if len(salt) == 4:
            break
    salted = password+salt
    return salted

def salt_remover(salted_password) -> str:
    resolved = salted_password[:1-5]
    return resolved


def passwordrequisite(password):
    error_msg = ''
    special_characters = "!@#$%^&*()-+?_=,<>/"
    passwordHasUpper = False
    passwordHasDigits = False
    passwordHasSymbol = False
    if len(password) < 8:
        passwordIsLength = False
        error_msg += "Too short"
    else:
        passwordIsLength = True
    for i in password:
        if i.isupper():
            passwordHasUpper = True
        elif i.isdigit():
            passwordHasDigits = True
    if passwordHasUpper == False:
        error_msg += ", No Uppercase letters"
    if passwordHasDigits == False:
        error_msg += ', No Digits'
    if any(c in special_characters for c in password):
        passwordHasSymbol = True
    else:
        error_msg += ', No symbols'
    if passwordHasDigits and passwordHasUpper and passwordIsLength and passwordHasSymbol == True:
        return True
    else:
        return error_msg

# print(passwordrequisite("132123d3"))  ## No Uppercase, no symbols
# print(passwordrequisite("dididD!di"))  ## No digits
# print(passwordrequisite("133DEddd3")) ## No symbols
# print(passwordrequisite("133DE!3")) ## Too short
# print(passwordrequisite("1321!3asdasasdsadE3")) ## Valid


