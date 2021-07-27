from flask import Flask
from flask import render_template
from src.static_tests import read_file
from src.data_collection.data_loader import DataLoader

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/chart')
def get_data():
    obj_ref = read_file.FileRead()
    data_loader = DataLoader()

    # Load the data from history
    # data = obj_ref.get_data('20210723', 'TSLA')
    data = data_loader.get_candles_data()

    return app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run(debug=True)
