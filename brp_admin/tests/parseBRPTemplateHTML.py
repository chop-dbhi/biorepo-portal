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


def extractUserCredentialInformation(body):
    valid = []
    invalid = []
    validStart = body.find("<ul>", body.find("<h4>"))
    validStop = body.find("</ul>", validStart)
    invalidStart = body.find("<ul>", body.rfind("<h4>"))
    invalidStop = body.find("</ul>", invalidStart)

    if validStart != -1:
        i = body.find("<p>", validStart) + len("<p>")
        while i < validStop and i != 2:
            valid.append(body[i:body.find("</p>", i)])
            i = body.find("<p>", i) + len("<p>")
    if invalidStart != validStart and invalidStart != -1:
        i = body.find("<p>", invalidStart) + len("<p>")
        while i < invalidStop and i != 2:
            invalid.append(body[i:body.find("</p>", i)])
            i = body.find("<p>", i) + len("<p>")
    return[valid, invalid]
