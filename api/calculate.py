from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins="https://microscope-size-calc.vercel.app")

@app.route('/api/calculate', methods=['POST'])
def calculate():
    try:
        magnification = int(request.form['magnification'])
        mactual = request.form['mactual']
        msize = float(request.form['msize'])
        actual = request.form['actual']

        if mactual == actual:
            raise ValueError("Microscope unit and actual unit must be different.")

        result = convert_size(mactual, actual, msize, magnification)
        return jsonify({"result": result}), 200

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error."}), 500

def convert_size(from_unit: str, to_unit: str, msize: float, magnification: int) -> str:
    units_in_meters = {
        'm': 1,
        'cm': 1e-2,
        'mm': 1e-3,
        'um': 1e-6,
        'nm': 1e-9,
        'pm': 1e-12,
    }

    if from_unit not in units_in_meters or to_unit not in units_in_meters:
        raise ValueError("Unsupported units. Use: 'm', 'cm', 'mm', 'um', 'nm', 'pm'")

    factor = units_in_meters[from_unit] / units_in_meters[to_unit]
    size = (msize / magnification) * factor
    return f"Actual size: {size:.6g} {to_unit}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
