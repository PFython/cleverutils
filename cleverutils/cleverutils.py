
"""
A collection of high level functions, classes, and methods tailored to the author's current level and style of Python coding.
"""
import time
import json
from pathlib import Path
import inspect
from itertools import islice
import datetime
from pprint import pprint
try:
    from cleverdict import CleverDict
except:
    # When cleverdict isn't installed but is on PYTHONPATH:
    from cleverdict.cleverdict import CleverDict
from cleverdict.cleverdict import get_app_dir
import os
import logging
import re

INSTALL_PATH = Path(__file__).parent.parent
ICON_PATH = (Path(__file__).parent).with_name("cleverutils.ico")

def get_time(time_format="numeric"):
    """ Returns the local time in a predefined format """
    if time_format == "numeric":
        # 12 digit, all numeric.  Useful as a concise timestamp
        return time.strftime("%Y%m%d%H%M", time.localtime())


def timer(func):
    """
    Wrapper to start the clock, run func(), then stop the clock. Simples.
    Designed to work as a decorator... just put @timer in the line above the
    original function.
    """
    def wrapper(*args, **kwargs):
        file_path = Path(get_app_dir("cleverutils")) / "timer_logs.txt"
        try:
            os.makedirs(file_path.parent)
        except FileExistsError:
            pass
        if not file_path.is_file():
            file_path.touch()
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s|%(levelname)s|%(message)s', filename=file_path,)
        # List of available options here:
        # https://docs.python.org/3/library/logging.html#logrecord-attributes
        print(f"\n ⓘ  Timings logged to:\n    {file_path}")
        start = time.perf_counter()
        data = func(*args, **kwargs)
        logging.info(f"Function {func.__name__!r} took {round(time.perf_counter()-start,2)} seconds to complete.")
        return (data)
    return wrapper

def list_batches(data, batch_size=10):
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

    Returns
    -------
    A generator object of lists.
    """
    # it = iter(data)
    # for i in range(0, len(data), batch_size):
    #     yield [x for x in islice(it, batch_size)]
    for i in range(0, len(data), batch_size):
        yield(data[i:i + batch_size])


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

    Returns
    -------
    A generator object of dicts.
    """
    it = iter(data)
    for i in range(0, len(data), batch_size):
        yield {k:data[k] for k in islice(it, batch_size)}

def to_batches(data, batch_size):
    """
    Calls dict_batches or list_batches respectively to return a generator object
    containing a batches of a given size or less.

    Parameters
    ----------

    data: dict | list | set | tuple
        The source data to be divided into batches.
    batch_size: int
        The maximum number of items for each batch to contain.
        NB the final batch size may be less than batch_size if not divisible.

    Returns
    -------
    A generator object of dicts or iterables respectively.
    """
    if not isinstance(batch_size, int):
        raise TypeError("batch_size must be an integer")
    if not batch_size > 0:
        raise ValueError("batch_size must be positive")
    if batch_size > len(data):
        raise ValueError(f"batch_size must be <= len(data) i.e. {len(data)}")
    function_dispatch = {dict: dict_batches,
                            CleverDict: dict_batches,
                            list: list_batches,
                            tuple: list_batches}
    return function_dispatch[type(data)](data, batch_size)


def convert_to_dict(obj):
    """
    A function takes in a custom object and returns a dictionary representation of the object.
    This dict representation includes meta data such as the object's module and class names required for serialisation to/from JSON.
    """

    #  Populate the dictionary with object meta data
    obj_dict = {
        "__class__": obj.__class__.__name__,
        "__module__": obj.__module__
    }

    #  Populate the dictionary with object properties
    obj_dict.update(obj.__dict__)

    return obj_dict


def convert_to_json(obj):
    """
    Converts a non-serialisable custom object into JSON by creating a simple
    dict with metadata that IS serialisable, and then using default= argument.
    """
    json.dumps(obj, default=convert_to_dict,indent=4, sort_keys=True)



def dict_to_obj(our_dict):
    """
    Function that takes in a dict and returns a custom object associated with the dict.
    This function makes use of the "__module__" and "__class__" metadata in the dictionary
    to know which object type to create.

    Use object_hook= keyword to run this function with json.loads:

    json.loads(our_dict, object_hook=dict_to_obj)
    """
    if "__class__" in our_dict:
        # Pop ensures we remove metadata from the dict to leave only the instance arguments
        class_name = our_dict.pop("__class__")

        # Get the module name from the dict and import it
        module_name = our_dict.pop("__module__")

        # We use the built in __import__ function since the module name is not yet known at runtime
        module = __import__(module_name)

        # Get the class from the module
        class_ = getattr(module,class_name)

        # Use dictionary unpacking to initialize the object
        obj = class_(**our_dict)
    else:
        obj = our_dict
    return obj

def yt_time(duration):
    """
    Converts YouTube duration (ISO 8061)
    into Seconds

    see http://en.wikipedia.org/wiki/ISO_8601#Durations
    """
    ISO_8601 = re.compile(
        'P'   # designates a period
        '(?:(?P<years>\d+)Y)?'   # years
        '(?:(?P<months>\d+)M)?'  # months
        '(?:(?P<weeks>\d+)W)?'   # weeks
        '(?:(?P<days>\d+)D)?'    # days
        '(?:T' # time part must begin with a T
        '(?:(?P<hours>\d+)H)?'   # hours
        '(?:(?P<minutes>\d+)M)?' # minutes
        '(?:(?P<seconds>\d+)S)?' # seconds
        ')?')   # end of time part
    # Convert regex matches into a short list of time units
    units = list(ISO_8601.match(duration).groups()[-3:])
    # Put list in ascending order & remove 'None' types
    units = list(reversed([int(x) if x != None else 0 for x in units]))
    # Do the maths
    return sum([x*60**units.index(x) for x in units])
