class CellState:
    STENCH, BREEZE, GLITTER, SCREAM = range(4)

    def get_by_id(p_id: int):
        dictio = {v: k for k, v in CellState.__dict__.items() if not k.startswith("__")}
        return dictio.get(p_id)
