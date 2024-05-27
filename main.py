from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS  # Import CORS from flask_cors module
import kociemba
import os
import shutil  # Import shutil for file operations
import solve

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return 'Hello, World! This is a basic Flask endpoint.'

@app.route('/getKey', methods=['POST'])
def get_key():
    # Clear the upload folder before saving new files
    clear_upload_folder()

    keys = ['O', 'Y', 'W', 'G', 'B', 'R']
    image_dict = {}

    for key in keys:
        file = request.files.get(key)
        if not file:
            return jsonify({'error': f'No {key} file selected'})
        if file:
            original_filename = secure_filename(file.filename)  # Get the original filename
            extension = original_filename.rsplit('.', 1)[-1]  # Extract file extension
            filename = f'{key}.{extension}'  # New filename with key and original extension
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_dict[key] = filepath

    #after upload complete run the files i required order to and get the array and then pass the array to kociemba and get the solve and then process it and return
    letters_O = print_and_append("B.jpeg")
    letters_G = print_and_append("O.jpeg")
    letters_W = print_and_append("W.jpeg")
    letters_R = print_and_append("G.jpeg")
    letters_Y = print_and_append("R.jpeg")
    letters_B = print_and_append("Y.jpeg")
    # Appending all arrays in the returning order
    all_letters = letters_O + letters_G + letters_W + letters_R + letters_Y + letters_B

    # Printing as one single string
    cube_string = ''.join(all_letters)
    solve_string = kociemba.solve(cube_string)
    return jsonify(solve_string)

def clear_upload_folder():
    # Remove all files and subdirectories in the upload folder
    for root, dirs, files in os.walk(app.config['UPLOAD_FOLDER'], topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            shutil.rmtree(os.path.join(root, dir))

def print_and_append(file_name):
    letters = solve.get_letters(file_name)
    print(letters)
    if letters[4] == "U" or letters[4] == "D"  or letters[4] == "F":
        adj_letters = [None] * 9
        adj_letters[0] = letters[6]
        adj_letters[1] = letters[7]
        adj_letters[2] = letters[8]
        adj_letters[3] = letters[3]
        adj_letters[4] = letters[4]
        adj_letters[5] = letters[5]
        adj_letters[6] = letters[0]
        adj_letters[7] = letters[1]
        adj_letters[8] = letters[2]

        return adj_letters

    if letters[4] == "R" or letters[4] == "L" or letters[4] == "B":
        adj_letters = [None] * 9
        adj_letters[0] = letters[2]
        adj_letters[1] = letters[1]
        adj_letters[2] = letters[0]
        adj_letters[3] = letters[5]
        adj_letters[4] = letters[4]
        adj_letters[5] = letters[3]
        adj_letters[6] = letters[8]
        adj_letters[7] = letters[7]
        adj_letters[8] = letters[6]

        return adj_letters

if __name__ == '__main__':
    app.run(debug=True)
