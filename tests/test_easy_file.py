#!/usr/bin/env python

"""Tests for `easy_file` package."""

import pytest


# from easy_file import easy_file
from easy_file import TextFile, JSONFile, YAMLFile


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_JSONFile(response: int) -> list:
    from pathlib import Path

    fname = Path(__file__).parent / "some.json"
    f = JSONFile(fname)
    data = {"key": [1, 2, 3]}
    f.save(data)
    loaded = JSONFile(fname).load()
    assert loaded == data

