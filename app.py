from flask import Flask, Response, request, jsonify, json
from pymongo import MongoClient 
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.exceptions import HTTPException

class APICustomError(HTTPException):
  code = 403
  description = "Custom Error"

app = Flask(__name__) 

# MongoDB connection setup 
client = MongoClient(host='test_mongodb', port=27017, 
                    username='root', password='pass', authSource="admin") 
db = client.todos_db 
todos_collection = db.todos 

@app.get("/api/todos")
def get_todos():
    todo_id = request.args.get('todo_id')
    filter = {} if todo_id is None else {"todo_id": todo_id}
    todos = list(db.todos.find(filter))

    response = Response(
        response = dumps(todos), status=200,  mimetype="application/json")
    return response

@app.post("/api/todos")
def add_todos():
    todo_data = request.json
    if "todo_id" not in todo_data:
        raise APICustomError('Missing todo_id value')
    if "name" not in todo_data:
        raise APICustomError('Missing todo_id value')
    if "description" not in todo_data:
        raise APICustomError('Missing description value')
    
    todos_collection.insert_one(request.json)
    resp = jsonify({"message": "Todo added successfully"})
    resp.status_code = 200
    return resp

@app.delete("/api/todos/<id>")
def delete_todo(id):
    todos_collection.delete_one({'_id': ObjectId(id)})

    resp = jsonify({"message": "Todo deleted successfully"})
    resp.status_code = 200
    return resp 

@app.put("/api/todos/<id>")
def update_todo(id):
    _json = request.json
    todos_collection.update_one({'_id': ObjectId(id)}, {"$set": _json})

    resp = jsonify({"message": "Todo updated successfully"})
    resp.status_code = 200
    return resp


@app.errorhandler(APICustomError)
@app.errorhandler(Exception)
def handle_custom_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == '__main__': 
    app.run(host='0.0.0.0', debug=True) 
