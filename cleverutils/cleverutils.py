
"""
A collection of high level functions, classes, and methods based on the CleverDict data class and tailored to the author's current level and style of Python coding.
"""
import time

def to_json(self, never_save = False, **kwargs):
    """
    Additional CleverDict method to serialise its data to JSON.

    >>> setattr(CleverDict, "to_json", to_json)

    KWARGS
    never_save: Exclude field in CleverDict.never_save if True eg passwords
    file: Save to file if True or filepath

    * Will probably be incorporated into future versions of CleverDict,
    * at which point this function will be redundant.
    """
    # .get_aliases finds attributes created after __init__:
    fields_dict = {key: self.get(key) for key in self.get_aliases()}
    if never_save:
        fields_dict = {k:v for k,v in fields_dict if k not in never_save}
    json_str = json.dumps(fields_dict, indent=4)
    path = kwargs.get("file")
    if path:
        path = Path(path)
        with path.open("w") as file:
            file.write(json_str)
        frame = inspect.currentframe().f_back.f_locals
        ids = [k for k, v in frame.items() if v is self]
        id = ids[0] if len(ids) == 1 else "/".join(ids)
        print(f"\n ⓘ  Saved '{id}' in JSON format to:\n    {path.absolute()}")
    return json_str

def timer(func):
    """
    Wrapper to start the clock, runs func(), then stop the clock. Simples.
    Designed to work as a decorator... just put @timer in the line above the
    original function.
    """
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        data = func(*args, **kwargs)
        print(f"\n ⏱  Function {func.__name__!r} took {round(time.perf_counter()-start,2)} seconds to complete.\n")
        return (data)
    return wrapper
