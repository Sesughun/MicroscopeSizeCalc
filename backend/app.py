from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to convert size
def convert_size(from_unit: str, to_unit: str) -> float:
    units_in_meters = {
        'm': 1,
        'cm': 1e-2,
        'mm': 1e-3,
        'um': 1e-6,
        'nm': 1e-9,
        'pm': 1e-12,
    }
    if from_unit == to_unit:
        raise ValueError("Units must be different")
    if from_unit not in units_in_meters or to_unit not in units_in_meters:
        raise ValueError("Unsupported units")
    return units_in_meters[from_unit] / units_in_meters[to_unit]

@app.route('/')
def index():
    return render_template('index.html')  # Renders the frontend

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Extracting form data
        magnification = int(request.form['magnification'])
        mactual = request.form['mactual']
        msize = int(request.form['msize'])
        actual = request.form['actual']

        # Convert and calculate actual size
        if mactual != actual:
            factor = convert_size(mactual, actual)
        else:
            return jsonify({'error': 'Units must be different.'})

        size = (msize / magnification) * factor
        return jsonify({'result': f"Actual size: {size} {actual}"})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
