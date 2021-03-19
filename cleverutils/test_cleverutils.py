# Tests for cleverutils
import pytest
from cleverdict import CleverDict
from cleverutils import *

test_dict = {k:str(k).zfill(8) for k in range(23)}
test_cleverdict = CleverDict(test_dict)
test_list = list(test_dict.values())
test_tuple = tuple(test_dict.values())


def generate_all_batches(generator):
    results = CleverDict({"output": []})
    while True:
        try:
            results.output += [next(generator)]
        except StopIteration:
            results.count = len(results.output)
            results.types = {type(x) for x in results.output}
            results.batch_sizes = {len(x) for x in results.output}
            return results


class Test_Batches:
    def test_positive(self):
        """
        Lists of batches should be yielded with the desired item types and
        desired max. batch size for lists, tuples, dicts, and cleverdicts
        """
        for test in (test_list, test_tuple, test_dict, test_cleverdict):
            for batch_size in range(1, len(test)):
                b = to_batches(test, batch_size)
                results = generate_all_batches(b)
                assert len(results.types) == 1
                assert isinstance(test, results.types.pop())
                assert max(results.batch_sizes) == batch_size

    def test_negative(self):
        """
        Invalid batch sizes should fail elegantly.
        Test data has 23 items.
        """
        for test in (test_list, test_tuple, test_dict, test_cleverdict):
            expected_errors = {0: ValueError,
                               -1: ValueError,
                               24: ValueError,
                               "text": TypeError,
                               -24: ValueError}
            for batch_size, error in expected_errors.items():
                with pytest.raises(error):
                    print(batch_size)
                    b = to_batches(test, batch_size)
                    results = generate_all_batches(b)

class Test_timer:
    def test_timer(self, caplog):
        @timer
        def example():
            time.sleep(1)
        with caplog.at_level(logging.INFO):
            example()
        assert "Function 'example' took 1." in caplog.text

class Test_Converters:
    def test_yt_time(self):
        assert yt_time("P1W2DT6H21M32S") == 22892

    def test_format_bytes(self):
        assert format_bytes(1,"b") == '8 b'
        assert format_bytes(1,"bits") == '8 bits'
        assert format_bytes(1024, "kilobyte") == "1 Kilobyte"
        assert format_bytes(1024, "kB") == "1 KB"
        assert format_bytes(7141000, "mb") == '54 Mb'
        assert format_bytes(7141000, "mib") == '54 Mib'
        assert format_bytes(7141000, "Mb") == '54 Mb'
        assert format_bytes(7141000, "MB") == '7 MB'
        assert format_bytes(7141000, "mebibytes") == '7 Mebibytes'
        assert format_bytes(7141000, "gb") == '0 Gb'
        assert format_bytes(1000000, "kB") == '977 KB'
        assert format_bytes(1000000, "kB", SI=True) == '1,000 KB'
        assert format_bytes(1000000, "kb") == '7,812 Kb'
        assert format_bytes(1000000, "kb", SI=True) == '8,000 Kb'
        assert format_bytes(125000, "kb") == '977 Kb'
        assert format_bytes(125000, "kb", SI=True) == '1,000 Kb'
        assert format_bytes(125*1024, "kb") == '1,000 Kb'
        assert format_bytes(125*1024, "kb", SI=True) == '1,024 Kb'

    def test_get_path_size(self):
        def first_item(paths):
            return [x for x in paths if not x.name.startswith(".")][0]
        dirp = first_item([x for x in Path().glob("*") if x.is_dir()])
        filep = first_item([x for x in dirp.glob("*") if x.is_file()])
        assert dirp.is_dir()
        assert filep.is_file()
        assert filep in dirp.glob("*")
        assert get_path_size(filep) > 0
        assert get_path_size(dirp) > 0
        assert get_path_size(dirp, recursive=True) > get_path_size(dirp)
        assert get_path_size(dirp, recursive=True) > get_path_size(dirp)

