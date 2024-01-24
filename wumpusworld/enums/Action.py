class Action:
    FORWARD, TURN_LEFT, TURN_RIGHT, SHOOT, GRAB, CLIMB = range(6)

    def get_by_id(p_id) :
        dictio = {v: k for k, v in Action.__dict__.items() if not k.startswith("__")}
        return dictio.get(p_id)

    def get_by_value(p_value) :
        dictio = {k: v for k, v in Action.__dict__.items() if not k.startswith("__")}
        return dictio.get(p_value)