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


