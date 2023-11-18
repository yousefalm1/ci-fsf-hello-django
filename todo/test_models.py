from django.test import TestCase
from .models import Item


class TestItemModel(TestCase):

    def test_done_defaults_to_false(self):
        # Create a test Item instance
        item = Item.objects.create(name='Test Todo Item')

        # Check if the 'done' field defaults to False
        self.assertFalse(item.done)

    def test_item_string_method_returns_name(self):
        item = Item.objects.create(name='Test Todo Item')
        self.assertEqual(str(item), 'Test Todo Item')
