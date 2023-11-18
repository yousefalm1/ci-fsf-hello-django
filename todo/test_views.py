from django.test import TestCase
from .models import Item


class TestViews(TestCase):

    # Test that the 'get_todo_list' view returns a response with status code 200 and the correct template
    def test_get_todo_list(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/todo_list.html')

    def test_get_add_item_page(self):
        response = self.client.get('/add', follow=True)

    # Assert that the response is a redirect (status code 301 or 302)
        self.assertTrue(response.redirect_chain)

    # Verify that the final URL matches the expected redirection
        self.assertEqual(response.redirect_chain[-1][0], '/add/')

    # Verify that the final response has status code 200
        self.assertEqual(response.status_code, 200)

    # Verify that the expected template is used
        self.assertTemplateUsed(response, 'todo/add_item.html')

    # Test that the 'edit' view returns a response with status code 200, the correct template, and edits an item
    def test_get_edit_item_page(self):
        # Create a test Item instance
        item = Item.objects.create(name='Test Todo Item')
        # Send a GET request to the 'edit' view with the item's ID as a parameter
        response = self.client.get(f'/edit/{item.id}/')
        # Check if the response has status code 200 and uses the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/edit_item.html')

    # Test that the 'add' view successfully adds an item
    def test_can_add_item(self):
        # Send a POST request to the 'add' view with form data
        response = self.client.post('/add/', {'name': 'Test Added Item'})
        # Check if the response redirects to the 'get_todo_list' view
        self.assertRedirects(response, '/')

    # Test that the 'delete' view successfully deletes an item
    def test_can_delete_item(self):
        # Create a test Item instance
        item = Item.objects.create(name='Test Todo Item')
        # Send a GET request to the 'delete' view with the item's ID as a parameter
        response = self.client.get(f'/delete/{item.id}/')
        # Check if the response redirects to the 'get_todo_list' view
        self.assertRedirects(response, '/')
        # Check if the item has been successfully deleted from the database
        existing_items = Item.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)

    # Test that the 'toggle' view successfully toggles the 'done' field of an item
    def test_can_toggle_item(self):
        # Create a test Item instance with 'done' set to True
        item = Item.objects.create(name='Test Todo Item', done=True)
        # Send a GET request to the 'toggle' view with the item's ID as a parameter
        response = self.client.get(f'/toggle/{item.id}/')
        # Check if the response redirects to the 'get_todo_list' view
        self.assertRedirects(response, '/')
        # Check if the 'done' field of the item has been toggled to False
        updated_item = Item.objects.get(id=item.id)
        self.assertFalse(updated_item.done)

    def test_can_edit_item(self):
        # Create a test item
        item = Item.objects.create(name='test Todo Item')

        # Use the 'edit' view to update the item
        response = self.client.post(
            f'/edit/{item.id}/', {'name': 'Updated Name'})

        # Check if the response redirects to the 'get_todo_list' view
        self.assertRedirects(response, '/')

        # Retrieve the updated item from the database
        updated_item = Item.objects.get(id=item.id)

        # Check if the updated item has the correct name
        self.assertEqual(updated_item.name, 'Updated Name')
