from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm


def get_todo_list(request):
    # Retrieve all to-do items from the database
    items = Item.objects.all()

    # Create a context dictionary containing the list of to-do items
    context = {
        'items': items
    }
    # Render the 'todo/todo_list.html' template with the context data
    return render(request, 'todo/todo_list.html', context)


def add_item(request):
    # Check if the form is submitted using the POST method
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = ItemForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect the user to the 'get_todo_list' view after adding the item
            return redirect('get_todo_list')

    # If the form is not submitted with POST, create an empty form
    form = ItemForm()
    # Create a context dictionary with the form
    context = {
        'form': form
    }
    # Render the 'add_item.html' template with the form
    return render(request, 'todo/add_item.html', context)


def edit_item(request, item_id):
    # Retrieve the item from the database or return a 404 error if not found
    item = get_object_or_404(Item, id=item_id)

    # Check if the form is submitted using the POST method
    if request.method == 'POST':
        # Populate the form with the POST data and the instance data from the database
        form = ItemForm(request.POST, instance=item)

        # Check if the form is valid
        if form.is_valid():
            # Save the form data to the database
            form.save()
            # Redirect the user to the 'get_todo_list' view after editing the item
            return redirect('get_todo_list')

    # If the request method is not POST (e.g., GET), create a form instance with the item's data
    form = ItemForm(instance=item)

    # Create a context dictionary with the form
    context = {
        'form': form
    }

    # Render the 'edit_item.html' template with the form
    return render(request, 'todo/edit_item.html', context)


def toggle_item(request, item_id):
    # Retrieve the item from the database or return a 404 error if not found
    item = get_object_or_404(Item, id=item_id)

    # Toggle the 'done' field
    item.done = not item.done

    # Save the changes to the database
    item.save()

    # Redirect the user to the 'get_todo_list' view
    return redirect('get_todo_list')


def delete_item(request, item_id):
    # Retrieve the item from the database or return a 404 error if not found
    item = get_object_or_404(Item, id=item_id)

    # Delete the item from the database
    item.delete()

    # Redirect the user to the 'get_todo_list' view
    return redirect('get_todo_list')
