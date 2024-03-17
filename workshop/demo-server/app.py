#from kubernetes import client, config, utils
from flask import Flask, json, jsonify, request
from os import path
import yaml
import pandas as pd
import kr8s
from kr8s.objects import objects_from_files
import kr8s.asyncio
import os
import subprocess
app = Flask(__name__)

#config.load_kube_config()

#core_v1 = client.CoreV1Api()
#apps_v1 = client.AppsV1Api()
#api = client.ApiClient()

def otel_collector_init():
    get_chart = subprocess.check_output(["helm", "repo", "add", "splunk-otel-collector-chart", "https://signalfx.github.io/splunk-otel-collector-chart"])
    helm_update = subprocess.check_output(["helm", "repo", "update"])
    print(get_chart)
    print(helm_update)


@app.route('start_collector', methods=['GET'])
def start_collector():
    start = subprocess.check_output
@app.route('/pods', methods=['GET'])
def get_pods():
    df = pd.DataFrame(columns=["Namespace", "Name", "Status", "HostIP"])
    pods = kr8s.get("pods", namespace=kr8s.ALL)
    for pod in pods:
        print(pod.raw)
        row = (pod.raw["metadata"]["namespace"], pod.raw["metadata"]["name"], pod.raw["status"]["phase"], pod.raw["status"]["hostIP"])
        df.loc[len(df)] = row

    
    return df.to_dict(orient='records')


@app.route('/health', methods=['GET'])
def health():
    return "OK"


@app.route('/apply_deployment', methods=['GET'])
def deployment():
    try:
        deployment = "deployment.yaml"
        #resp = apps_v1.create_namespaced_deployment(
        #    body=deployment, namespace=namespace, _preload_content=False)
        #resp = utils.create_from_yaml(api, deployment, namespace="default")
        #print(resp)
        resources = objects_from_files(deployment)
        for r in resources:
            print(r)
            r.create()
        return "200"
    except Exception as e:
        return str(e)

@app.route('/delete_deployment', methods=['GET'])
def delete_deployment():
    try:
        deployment = "deployment.yaml"
        resources = objects_from_files(deployment)
        for r in resources:
            print(r)
            r.delete()
        return "200"
    except Exception as e:
        return str(e)
    #filename = request.args.get('type', default = 'deployment.yaml', type = str)
    #namespace = request.args.get('namespace', default = 'default', type = str)
    #resp = apps_v1.delete_namespaced_deployment(name="nginx-deployment", namespace=namespace, _preload_content=False)
    #return resp

if __name__ == '__main__':
    otel_collector_init()
    app.run(host="0.0.0.0", port=8083, debug=True)