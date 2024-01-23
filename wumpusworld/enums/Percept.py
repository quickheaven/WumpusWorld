class Percept:
    STENCH, BREEZE, GLITTER, SCREAM = range(4)

    def get_by_id(p_id):
        dictio = {v: k for k, v in Percept.__dict__.items() if not k.startswith("__")}
        return dictio.get(p_id)
