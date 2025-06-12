from flask import Flask, request, jsonify

app = Flask(__name__)

# Conversion factors to micrometers (µm)
UNIT_TO_UM = {
    "m": 1_000_000,    # meters to µm
    "cm": 10_000,      # centimeters to µm
    "mm": 1_000,       # millimeters to µm
    "um": 1,           # micrometers to µm
    "nm": 0.001,       # nanometers to µm
    "pm": 0.000_001    # picometers to µm
}

@app.route("/api/calculate", methods=["POST"])
def calculate():
    try:
        # Get form data
        magnification = float(request.form.get("magnification", 0))
        msize = float(request.form.get("msize", 0))
        mactual = request.form.get("mactual", "")
        actual = request.form.get("actual", "")

        # Validate inputs
        if magnification == 0:
            return jsonify({"error": "Magnification cannot be zero."}), 400
        if msize == 0:
            return jsonify({"error": "Microscope size cannot be zero."}), 400
        if mactual not in UNIT_TO_UM or actual not in UNIT_TO_UM:
            return jsonify({"error": "Invalid unit selected."}), 400

        # Step 1: Get actual size in input units
        actual_size_in_input_unit = msize / magnification

        # Step 2: Convert actual size to µm
        actual_size_um = actual_size_in_input_unit * UNIT_TO_UM[mactual]

        # Step 3: Convert µm to desired output unit
        result_in_selected_unit = actual_size_um / UNIT_TO_UM[actual]

        return jsonify({"result": f"{result_in_selected_unit:.2f} {actual}"})

    except ValueError:
        return jsonify({"error": "Invalid input. Please enter numeric values."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/calculate", methods=["GET", "PUT", "DELETE", "PATCH"])
def method_not_allowed():
    return jsonify({"error": "Method Not Allowed"}), 405

if __name__ == "__main__":
    app.run()
