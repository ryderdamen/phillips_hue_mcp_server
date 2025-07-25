from flask import Flask, jsonify, request, render_template
from lights import lights, groups

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/mock/lights')
def api_mock_lights():
    return jsonify(lights)

@app.route('/api/<username>/lights', methods=['GET'])
def get_lights(username):
    return jsonify(lights)

@app.route('/api/<username>/lights/<light_id>', methods=['GET'])
def get_light(username, light_id):
    return jsonify(lights.get(light_id, {}))

@app.route('/api/<username>/lights/<light_id>/state', methods=['PUT'])
def set_light_state(username, light_id):
    data = request.get_json(force=True)
    if light_id in lights:
        lights[light_id]['state'].update(data)
        return jsonify([{"success": True}])
    return jsonify([{"error": "Light not found"}]), 404

@app.route('/api/<username>/groups', methods=['GET'])
def get_groups(username):
    return jsonify(groups)

@app.route('/api/<username>/groups/<group_id>', methods=['GET'])
def get_group(username, group_id):
    return jsonify(groups.get(group_id, {}))

@app.route('/api/<username>/groups/<group_id>/action', methods=['PUT'])
def set_group_action(username, group_id):
    data = request.get_json(force=True)
    group = groups.get(group_id)
    if group:
        group['action'].update(data)
        # Also update all lights in the group
        for lid in group['lights']:
            lights[lid]['state'].update(data)
        return jsonify([{"success": True}])
    return jsonify([{"error": "Group not found"}]), 404

@app.route('/api/mock/groups_lights')
def api_mock_groups_lights():
    from lights import groups, lights
    return jsonify({"groups": groups, "lights": lights})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 