
"""
A collection of high level functions, classes, and methods tailored to the author's current level and style of Python coding.
"""
import time
import json
from pathlib import Path
import inspect
from itertools import islice

def get_time(time_format="numeric"):
    """ Returns the local time in a predefined format """
    if time_format == "numeric":
        # 12 digit, all numeric.  Useful as a concise timestamp
        return time.strftime("%Y%m%d%H%M", time.localtime())

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
    fields_dict = {k: self.get(k) for k in self.get_aliases()}
    if never_save:
        fields_dict = {k: v for k,v in fields_dict.items() if k not in never_save}
    # JSON can't serialise Path objects, so convert to str
    for k,v in fields_dict.items():
        if isinstance(v, Path):
            fields_dict[k] = str(v)
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
        print()
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

def list_batches(data, **kwargs):
    """ Yields a sublist with batch_size values.

    kwargs:
    batch_size : Maximum size of any sublist returned; last sublist may be less.
    browsers: Number of browers, to run; Calculate batch_size accordingly

    x = list_batches(data)
    try:
        while True:
            sublist = next(x)
            do_stuff(sublist)
    except StopIteration:
        pass
    finally:
        del iterator
    """
    batch_size = kwargs.get("batch_size")
    if not batch_size:
        batch_size = len(data) // (kwargs.get("browsers") or 5)
        if len(data) % batch_size:  # positive remainder
            batch_size+=1
    it = iter(data)
    for i in range(0, len(data), batch_size):
        yield (x for x in islice(it, batch_size))

def dict_batches(data, batch_size=10):
    """ Yields a subdictionary with batch_size keys.

    x = dict_batches(data)
    try:
        while True:
            subdict = next(x)
            do_stuff(subdict)
    except StopIteration:
        pass
    finally:
        del iterator
    """
    it = iter(data)
    for i in range(0, len(data), batch_size):
        yield {k:data[k] for k in islice(it, batch_size)}

