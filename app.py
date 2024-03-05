from flask import Flask, make_response, redirect, render_template, request, Response
import uuid

dog_map = {}
selected_id = '';

def add_dog(name, breed):
    id = str(uuid.uuid4())
    dog = {'id': id, 'name': name, 'breed': breed}
    dog_map[id] = dog
    return dog

add_dog('Comet', 'Whippet')
add_dog('Oscar', 'German Shorthaired Pointer')

# __name__ holds the name of the current module which is "app".
app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/dogs')

@app.route('/dogs')
def all_dogs():
    return render_template('dogs.html')

@app.route('/dogs/<id>')
def one_dog(id):
    dog = dog_map[id]
    return dog # returns JSON

# Deletes the dog with a given id.
@app.route('/dog/<id>', methods=['DELETE'])
def delete_dog(id):
    global dog_map
    del dog_map[id]
    return ''

# Deselects the currently selected dog.
@app.route('/deselect')
def deselect():
    global selected_id
    selected_id = ''
    res = Response('')
    res.headers['HX-Trigger'] = 'selection-change'
    return res

# Gets the proper form for either adding or updating a dog.
@app.route('/form')
def form():
    dog = dog_map.get(selected_id)
    return render_template('form.html', dog=dog)

# Gets table rows for all the dogs.
@app.route('/rows')
def rows():
    sorted_dogs = sorted(dog_map.values(), key=lambda x: x['name'])
    return render_template('dog-rows.html', dogs=sorted_dogs)

# Selects a dog.
@app.route('/select/<id>')
def select(id):
    global selected_id
    selected_id = id;
    res = Response('')
    res.headers['HX-Trigger'] = 'selection-change'
    return res

# Creates a dog.
@app.route('/dog', methods=['POST'])
def create():
    name = request.form.get('name')
    breed = request.form.get('breed')
    new_dog = add_dog(name, breed);
    return render_template('dog-row.html', dog=new_dog, status=201);

# Updates a dog
@app.route('/dog/<id>', methods=['PUT'])
def update(id):
    name = request.form.get('name')
    breed = request.form.get('breed')
    updatedDog = {'id': id, 'name': name, 'breed': breed};

    global dog_map, selected_id
    dog_map[id] = updatedDog;
    selected_id = '';

    res = make_response(
        render_template('dog-row.html', dog=updatedDog, swap=True)
    )
    res.headers['HX-Trigger'] = 'selection-change'
    return res

# Test whether HTML is sanitized.
@app.route('/xss')
def xss():
    name = 'Comet <script>alert("hi")</script>'
    return render_template('xss.html', name=name)