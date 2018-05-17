def extractErrors(body):
    if not hasErrorTag(body):
        return "no errors"
    returnString = ""
    bod = str(body)
    i = 0
    escaped = False
    while i < len(bod) and i != -1:
        i = bod.find("</strong> ", i)
        if i != -1:
            i += len("</strong> ")
        c = bod[i]
        while c != '<' and i < len(bod) and i != -1:
            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True
            else:
                returnString += c
            i += 1
            c = bod[i]

    return trimTrailingWhitespace(returnString)


def hasErrorTag(body):
    result = body.find("<strong>")
    if(result == -1):
        return False
    return True


def trimTrailingWhitespace(body):
    return body[:body.rfind('.')+1]
