"""
Test cases for methods related to citations.
"""

import unittest
from unittest import mock
import urllib.error

import stdpopsim


class mocked_response():
    """
    This exists solely to mock out the response from the
    urllib.request call so that we can test the bibtex
    retrieval. The enter and exit methods are for calling
    it as a context manager."""
    def __init__(self, code, text):
        self.code = code
        self.text = text

    def __enter__(self):
        return(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def read(self):
        return(self.text)

    def close(self):
        pass


class TestFetchBibtex(unittest.TestCase):
    """
    Test the fetching of bibtex files."""
    def test_get_bibtex_success(self):
        # Tests a success
        citation = stdpopsim.Citation(doi="DOI", author="Authors", year="2000")
        with mock.patch(
                'urllib.request.urlopen',
                return_value=mocked_response(
                    code=200, text=b'test')):
            with mock.patch('urllib.request.Request'):
                bib = citation.fetch_bibtex()
                self.assertEqual(bib, 'test')

    def test_get_bibtex_bad_connection(self):
        # Tests an invalid URL
        # Asserts that it raises a value error.
        citation = stdpopsim.Citation(doi='DOI', author="Authors", year="2000")
        with self.assertRaises(ValueError):
            citation.fetch_bibtex()

    def test_get_bibtex_404(self):
        # Tests a 404
        citation = stdpopsim.Citation(doi='http://doi.org/url-does-not-exist',
                                      author="Authors", year="2000")
        with self.assertRaises(urllib.error.HTTPError):
            citation.fetch_bibtex()
