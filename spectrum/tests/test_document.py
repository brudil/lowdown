from unittest import TestCase
from spectrum.document import SpectrumDocument
from spectrum.subtypes import ArticleSubtype


class TestDocument(TestCase):
    def test_setup_document(self):
        document = SpectrumDocument()
        print(document.subtype)
        document.subtype = ArticleSubtype()
        print(document.subtype)
        print(document.to_json())
