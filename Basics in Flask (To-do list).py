To-do list using Flask


## create the basic skeleton of flask. Only then, modify it.
from flask import Flask, jsonify, request

app = Flask(__name__)

##Initial Data in the To Do List
### This key-value pairs data - usually comes from MongoDB , any NoSQL Databases 
items = [
    {"id": 1, "name": "Item 1", "description": "This is the item 1"},
    {"id": 2, "name": "Item 2", "description": "This is the item 2"}
]

@app.route('/')
def home():
    return "Welcome to the To-Do list app"

## GET : Retrieve all the items - GET API
@app.route('/items', methods = ['GET'])
def get_items():
    return jsonify(items) # returns all the elements in the form of JSON (view is like a python dictionary) format.

## GET : Retrieve a specific item by ID. - GET API
@app.route('/items/<int:item_id>', methods = ['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"]==item_id), None) ## Only outputs one dictionary item or None
    if item is None:
        return jsonify({"error": "item is not found"})
    return jsonify(item)

## POST : Create a new task - POST API
@app.route('/items', methods = ['POST'])
def create_item():
    if not request.json or not 'name' in request.json:
        return jsonify({"error": "item not found"})
    new_item = {
        "id" : items[-1]["id"] + 1 if items else 1, ## Conditional expression
        "name" : request.json['name'],
        "description" : request.json["description"]
    }
    items.append(new_item)
    return jsonify(new_item) ## shows you which item has been added.


# Put : Update an Existing item - PUT API
@app.route('/items/<int:item_id>', methods = ['PUT'])
def update_item(item_id):
    item = next((item for item in items if item["id"]==item_id), None)
    if item is None:
        return jsonify({"error" : "Item not found"})
    item['name'] = request.json.get('name', item['name']) ## updating item['name'] with the json text provided by user
    item['description'] = request.json.get('description', item['description']) ## updating item['description'] with the json text provided by user
    return jsonify(item)

# DELETE : Delete an item - DELETE API
@app.route('/items/<int:item_id>', methods = ['DELETE'])
def delete_item(item_id):
    global items # Declares that you're modifying the items global variable, not creating a new local one inside the function.
    items = [item for item in items if item["id"] != item_id] # Builds a new list that includes all items except the one with the matching id.
    return jsonify({"result": "Item deleted"})                      ## Remove the item with id == item_id from the global items list



if __name__ == '__main__':
    app.run(debug=True)
