def incrementation(id_incrementation):
    if id_incrementation == "INT":
        return "INT AUTO_INCREMENT"
    elif id_incrementation == "BIGINT":
        return "BIGINT AUTO_INCREMENT"
    elif id_incrementation == "Aucune":
        return ""
    return id_incrementation
