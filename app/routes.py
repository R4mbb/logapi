from flask import Blueprint, requests, jsonify
from app.services import get_logs, filter_logs

api_blueprint = Blueprint('api', __name__)

# 로그 조회 API
@api_blueprint.route('/logs', methods=['GET'])
def logs():
    logs = get_logs()
    return jsonify(logs)


# 로그 필터링 API
@api_blueprint.route('/logs/filter', method=['GET'])
def filter():
    filter_params = requests.args
    filtered_logs = filter_logs(filter_params)
    return jsonify(filtered_logs)
