from flask import Flask, request, jsonify
import sys

app = Flask(__name__)

def convert_size(from_unit: str, to_unit: str) -> float:
    """
    Returns the factor to multiply a value by to convert from `from_unit` to `to_unit`.
    Supported units: 'm', 'cm', 'mm', 'um', 'nm', 'pm'
    """
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
        raise ValueError("Unsupported units. Use: 'm', 'cm', 'mm', 'um', 'nm', 'pm'")

    factor = units_in_meters[from_unit] / units_in_meters[to_unit]
    return factor

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        magnification = int(request.form['magnification'])
        mactual = request.form['mactual']
        msize = int(request.form['msize'])
        actual = request.form['actual']

        if mactual == actual:
            return jsonify({'error': "Units must be different"})

        # Convert sizes
        factor = convert_size(mactual, actual)
        size = (msize / magnification) * factor
        result = f"Actual size: {size} {actual}"

        return jsonify({'result': result})
    except ValueError as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
