def masToken():
    f = open('../token.txt', 'r+', encoding="utf8")
    mas_token = []
    for i in f:
        if ('\n' in i):
            i = i.replace('\n', '')
        mas_token.append(i)
    return mas_token

mas_tokens = masToken()