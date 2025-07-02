def incrementation(id_incrementation):
    if id_incrementation in ("SERIAL", "BIGSERIAL"):
        return f"{id_incrementation}"
    elif id_incrementation == "Aucune":
        return ""
