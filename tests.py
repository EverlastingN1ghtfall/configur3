import pytest
from main import *


def test_basic():
    with open("tests_compare/test_basic1.txt", 'r', encoding='utf-8') as f:
        data = f.read()
    with open("tests_compare/basic.json", 'r', encoding='utf-8') as f:
        cmp_with = f.read()
    test = Solution(data)
    test.export_to_json("tests_compare/test1.json")
    with open("tests_compare/test1.json", 'r', encoding='utf-8') as f:
        exported = f.read()
    assert exported == cmp_with

def test_consts():
    with open("tests_compare/test_consts.txt", 'r', encoding='utf-8') as f:
        data = f.read()
    with open("tests_compare/consts.json", 'r', encoding='utf-8') as f:
        cmp_with = f.read()
    test = Solution(data)
    test.export_to_json("tests_compare/test2.json")
    with open("tests_compare/test2.json", 'r', encoding='utf-8') as f:
        exported = f.read()
    assert exported == cmp_with

def test_nested():
    with open("tests_compare/test_nested.txt", 'r', encoding='utf-8') as f:
        data = f.read()
    with open("tests_compare/nested.json", 'r', encoding='utf-8') as f:
        cmp_with = f.read()
    test = Solution(data)
    test.export_to_json("tests_compare/test3.json")
    with open("tests_compare/test3.json", 'r', encoding='utf-8') as f:
        exported = f.read()
    assert exported == cmp_with

def test_mases():
    with open("tests_compare/test_hard_mases.txt", 'r', encoding='utf-8') as f:
        data = f.read()
    with open("tests_compare/hard_mases.json", 'r', encoding='utf-8') as f:
        cmp_with = f.read()
    test = Solution(data)
    test.export_to_json("tests_compare/test4.json")
    with open("tests_compare/test4.json", 'r', encoding='utf-8') as f:
        exported = f.read()
    assert exported == cmp_with