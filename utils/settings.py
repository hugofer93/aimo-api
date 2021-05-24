from bottle import load


def load_module_as_dict(path: str) -> dict:
    """Load values from a Python module as dict.
    Based on bootle source code.

    Args:
        path (str): Python module name.

    Returns:
        dict: Settings.
    """
    config_obj = load(path)
    obj = {key: getattr(config_obj, key) for key in dir(config_obj)
           if key.isupper()}
    return obj
