from flask import Flask, request, render_template
from math import sqrt
from datetime import datetime

app = Flask('my_distance')
distances = []


def calculate_distance(point_a, point_b):
    """Calcule la distance euclidienne (Pythagore)."""
    return sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)


def parse_point(point_str):
    coords = point_str.split(',')
    return int(coords[0]), int(coords[1])


@app.route('/', methods=['GET', 'POST'])
def html_calculate():
    if request.method == 'GET':
        return render_template('index.html', result=None)

    if request.method == 'POST':
        point_a = parse_point(request.form['apoint'])
        point_b = parse_point(request.form['bpoint'])
        dist = calculate_distance(point_a, point_b)

        result = {
            'requested_at': datetime.now(),
            'result_distance': dist,
            'start_point': point_a,
            'end_point': point_b
        }
        distances.append(result)
        return render_template('index.html', result=result)


@app.route('/api')
def index():
    return {}


@app.route('/api/distances')
def already_calculated():
    result = list(map(lambda x: {
        'requested_at': x['requested_at'],
        'result_distance': x['result_distance'],
        'start_point': x['start_point'],
        'end_point': x['end_point']
    }, distances))
    return result


@app.route('/api/distance', methods=['POST', 'GET', 'PUT'])
def Calculate():
    startPoint = list(map(lambda y: int(y), request.json['start_point'].split(',')[0:2]))
    EndPoint = tuple(map(lambda x: int(x), request.json['end_point'].split(',')[0:2]))

    result_tmp = sqrt((EndPoint[1] - startPoint[1]) ** 2 + (EndPoint[0] - startPoint[0]) ** 2)
    result = {
        'requested_at': datetime.now(),
        'result_distance': result_tmp,
        'start_point': startPoint,
        'end_point': EndPoint
    }
    return result