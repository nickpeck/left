
def make_props(context: dict, *keys):
    return {k: context[k] for k in keys}

