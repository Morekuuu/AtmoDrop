from flask import Flask, request, send_from_directory
import os

UPLOAD_FOLDER ='/mnt/dane'
app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_csv():
        if 'file' not in request.files:
                return 'Brak pliku', 400

        file = request.files['file']
        filename = file.filename
        path = os.path.join(UPLOAD_FOLDER, filename)

        file.save(path)
        return f'Plik zapisany jako {filename}', 200
@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)