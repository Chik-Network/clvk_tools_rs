"""
These tests check that the `clvkc` utility methods
continue to work with the `include` keyword, and produce
the expected output. It's not intended to be a complete
test of the compiler, just the `clvkc` api.
"""

from tempfile import TemporaryDirectory

from clvk_tools import clvkc


INCLUDE_CODE = "((defconstant FOO 6001))"
MAIN_CODE = """(mod (VALUE) (include "include.clvk") (+ VALUE FOO))"""
EXPECTED_HEX_OUTPUT = "ff10ff02ffff0182177180"

# `EXPECTED_HEX_OUTPUT` disassembles to "(+ 2 (q . 6001))"


def test_compile_clvk_text():
    with TemporaryDirectory() as include_dir:
        include_path = f"{include_dir}/include.clvk"
        with open(include_path, "w") as f:
            f.write(INCLUDE_CODE)
        output = clvkc.compile_clvk_text(MAIN_CODE, search_paths=[include_dir])
        assert repr(output) == f"SExp({EXPECTED_HEX_OUTPUT})"


def test_compile_clvk():
    with TemporaryDirectory() as include_dir:
        with TemporaryDirectory() as source_dir:
            with open(f"{include_dir}/include.clvk", "w") as f:
                f.write(INCLUDE_CODE)
            main_path = f"{source_dir}/main.clvk"
            main_output = f"{source_dir}/main.hex"
            with open(main_path, "w") as f:
                f.write(MAIN_CODE)
            output = clvkc.compile_clvk(
                main_path, main_output, search_paths=[include_dir]
            )
            t = open(output).read()
            assert t == f"{EXPECTED_HEX_OUTPUT}\n"
