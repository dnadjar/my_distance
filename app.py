from flask import Flask, request, render_template, jsonify
from math import sqrt
from datetime import datetime

app = Flask('my_distance')
distances = []


def calculate_distance(point_a, point_b):
    return sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)


def parse_point(point_str):
    coords = point_str.split(',')
    return int(coords[0]), int(coords[1])


@app.route('/', methods=['GET', 'POST'])
def html_calculate():
    if request.method == 'GET':
        return render_template('index.html', result=None)

    if request.method == 'POST':
        try:
            point_a = parse_point(request.form['apoint'])
            point_b = parse_point(request.form['bpoint'])
            dist = calculate_distance(point_a, point_b)

            result = {
                'requested_at': datetime.now().isoformat(),
                'result_distance': dist,
                'start_point': point_a,
                'end_point': point_b
            }
            distances.append(result)
            return render_template('index.html', result=result)
        except (ValueError, IndexError):
            return render_template('index.html', result={"error": "Format invalide"})


@app.route('/api/distances', methods=['GET'])
def get_distances():
    return jsonify(distances)


@app.route('/api/distance', methods=['POST'])
def calculate_distance_api():
    data = request.get_json()
    if not data or 'start_point' not in data or 'end_point' not in data:
        return jsonify({"error": "Données manquantes"}), 400

    try:
        point_a = parse_point(data['start_point'])
        point_b = parse_point(data['end_point'])
        dist = calculate_distance(point_a, point_b)

        result = {
            'requested_at': datetime.now().isoformat(),
            'result_distance': dist,
            'start_point': point_a,
            'end_point': point_b
        }
        return jsonify(result), 200
    except (ValueError, IndexError, TypeError):
        return jsonify({"error": "Format invalide"}), 400