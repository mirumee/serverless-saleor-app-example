def obfuscate(token):
    return token[0] + ("*" * (len(token) - 2)) + token[-1]
