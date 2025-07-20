from flask import Blueprint, request, jsonify

blueprint = Blueprint("check", __name__)


@blueprint.route("/front_door", methods=["GET"])
def check_front_door():
    from homecv.analyzers.front_door import check
    from homecv.integrations.hass.client import HomeAssistantClient

    debug = False
    if "debug" in request.args:
        debug = True

    client = HomeAssistantClient()
    detected = check(client, debug)

    if detected:
        message = "Person detected at the door!"
    else:
        message = "No person detected at the door."

    return jsonify({"detected": detected, "message": message}), 200
