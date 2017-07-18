from unittest import TestCase
from spectrum.blocks import ImageBlock


class TestBaseElement(TestCase):

    def test_create(self):
        block = ImageBlock()

        print('this', block.reference)
