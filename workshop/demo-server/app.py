from kubernetes import client, config
from flask import Flask, json, jsonify, request
from os import path
import yaml
import pandas as pd

app = Flask(__name__)

config.load_kube_config()

core_v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()


@app.route('/pods', methods=['GET'])
def get_pods():
    result = core_v1.list_pod_for_all_namespaces(_preload_content=False)
    pods = json.loads(result.data)
    df = pd.DataFrame(columns=["Namespace", "Name", "Status", "Pod IP"])

    for r in pods['items']:
        row = (r["metadata"]["namespace"], r["metadata"]["name"], r["status"]["phase"], r["status"]["podIP"])
        df.loc[len(df)] = row

    return df.to_dict(orient='records')


@app.route('/health', methods=['GET'])
def health():
    return "OK"


@app.route('/apply_deployment', methods=['GET'])
def deployment():
    filename = request.args.get('type', default = 'deployment.yaml', type = str)
    namespace = request.args.get('namespace', default = 'default', type = str)
    with open(path.join(path.dirname(__file__), filename)) as f:
        deployment = yaml.safe_load(f)
        resp = apps_v1.create_namespaced_deployment(
            body=deployment, namespace=namespace, _preload_content=False)
        return resp.json() 


@app.route('/delete_deployment', methods=['GET'])
def delete_deployment():
    filename = request.args.get('type', default = 'deployment.yaml', type = str)
    namespace = request.args.get('namespace', default = 'default', type = str)
    resp = apps_v1.delete_namespaced_deployment(name="nginx-deployment", namespace=namespace, _preload_content=False)
    return resp.json()

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5001, debug=True)