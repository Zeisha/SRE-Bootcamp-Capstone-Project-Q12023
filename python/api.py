from flask import Flask, request, jsonify
from convert import CidrMaskConvert, IpValidate
from methods import Token, Restricted
from os import getenv

app = Flask(__name__)
login = Token()
protected = Restricted()
convert = CidrMaskConvert()
validate = IpValidate()
port = int(getenv("APP_PORT"))


@app.route("/")
def api_default():
    return "OK"


@app.route("/_health")
def api_health():
    return "OK"


@app.route("/login", methods=["POST"])
def user_login():
    username = request.form["username"]
    password = request.form["password"]
    token = login.generate_token(username, password)

    if token is None:
        return "", 401

    return jsonify({"data": token}), 200


@app.route("/cidr-to-mask")
def cidr_to_mask():
    auth_token = request.headers.get("Authorization")
    if not protected.access_data(auth_token):
        return "", 401
    cidr_value = request.args.get("value")
    mask = {
        "function": "cidrToMask",
        "input": cidr_value,
        "output": convert.cidr_to_mask(cidr_value),
    }
    return jsonify(mask)


@app.route("/mask-to-cidr")
def mask_to_cidr():
    auth_token = request.headers.get("Authorization")
    if not protected.access_data(auth_token):
        return "", 401
    mask = request.args.get("value")
    cidr_value = {
        "function": "maskToCidr",
        "input": mask,
        "output": convert.mask_to_cidr(mask),
    }
    return jsonify(cidr_value)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
