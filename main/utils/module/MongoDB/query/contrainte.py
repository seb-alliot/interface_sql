def contrainte(contrainte):
    if contrainte == " DEFAULT ":
        return " DEFAULT NULL"
    elif contrainte and contrainte != "Aucune":
        return f' {contrainte} '
    else:
        return ""
