from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/calculate", methods=["POST"])
def calculate():
    try:
        magnification = float(request.form.get("magnification", 0))
        actual_size = float(request.form.get("actual_size", 0))

        if magnification == 0:
            return jsonify({"error": "Magnification cannot be zero."}), 400

        image_size = magnification * actual_size
        return jsonify({"result": f"{image_size:.2f} µm"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/calculate", methods=["GET", "PUT", "DELETE", "PATCH"])
def method_not_allowed():
    return jsonify({"error": "Method Not Allowed"}), 405
