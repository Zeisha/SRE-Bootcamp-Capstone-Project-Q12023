from flask import Flask, request, jsonify
from networking import get_cidr_from_mask, get_mask_from_cidr
from auth import Auth
from os import getenv

app = Flask(__name__)
auth = Auth()
port = int(getenv("APP_PORT"))


def is_valid_authorization():
    authorization = request.headers.get("Authorization")
    token = authorization.removeprefix("Bearer ")
    return authorization.startswith("Bearer") and auth.is_valid_token(token)


def json_response(function, input, output):
    return jsonify(
        {
            "function": function,
            "input": input,
            "output": output,
        }
    )


@app.route("/")
def api_default():
    return "OK"


@app.route("/_health")
def api_health():
    return "OK"


@app.route("/login", methods=["POST"])
def user_login():
    """
    usage: http://127.0.0.1:8000/login
    """
    username = request.form["username"]
    password = request.form["password"]
    token = auth.generate_token(username, password)

    if token is None:
        return "", 401

    return jsonify({"data": token}), 200


@app.route("/cidr-to-mask")
def cidr_to_mask():
    """
    usage: http://127.0.0.1:8000/cidr-to-mask?value=8
    """
    cidr = request.args.get("value")
    if is_valid_authorization() and cidr:
        return json_response("cidrToMask", cidr, get_mask_from_cidr(cidr))

    return "", 401


@app.route("/mask-to-cidr")
def mask_to_cidr():
    """
    usage: http://127.0.0.1:8000/mask-to-cidr?value=255.0.0.0
    """
    mask = request.args.get("value")
    if is_valid_authorization() and mask:
        return json_response("maskToCidr", mask, get_cidr_from_mask(mask))

    return "", 401


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=port)
