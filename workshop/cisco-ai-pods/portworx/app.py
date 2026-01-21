from flask import Flask, Response
import time
import random

app = Flask(__name__)

# ----- Customize these labels to match what your dashboards/queries expect -----
LABELS_NODE = {
    "cluster": "ocp-pxclus-32430549-ad99-4839-bf9b-d6beb8ddc2d6",
    "clusterUUID": "e870909b-6150-4d72-87cb-a012630e42ae",
    "node": "worker2.flashstack.local",
    "nodeID": "f63312a2-0884-4878-be4e-51935613aa80",
}

LABELS_VOL = {
    "cluster": "ocp-pxclus-32430549-ad99-4839-bf9b-d6beb8ddc2d6",
    "clusterUUID": "e870909b-6150-4d72-87cb-a012630e42ae",
    "namespace": "milvus",
    "node": "worker2.flashstack.local",
    "nodeID": "f63312a2-0884-4878-be4e-51935613aa80",
    "pvc": "milvus-deployment",
    "repl": "2",
    "sharedv4": "true",
    "sharedv4_mount_options": "vers=3.0,nolock",
    "sharedv4_svc_type": "ClusterIP",
    "volumebindingmode": "immediate",
    "volumeid": "882117008603900433",
    "volumename": "pvc-f7175eb5-6f01-4adc-b4b9-6c16329cabaf",
}

# ----- Helpers -----
def fmt_labels(d: dict) -> str:
    # Prometheus text format: key="value",...
    items = [f'{k}="{str(v)}"' for k, v in d.items()]
    return "{" + ",".join(items) + "}" if items else ""

def line(metric: str, labels: dict, value) -> str:
    return f"{metric}{fmt_labels(labels)} {value}"

@app.get("/metrics")
def metrics():
    # You can keep values static, or change them per request.
    # Here we do small random variations to simulate a live system.
    cpu_percent = round(random.uniform(0.0, 2.0), 3)
    disk_total = 2.199023255552e12
    disk_used = float(random.randint(1, 4)) * 1.0e11  # ~100-400GB
    nodes_online = 3
    nodes_offline = 0

    # Volume metrics (match sample types: gauge/counter)
    vol_read_latency = round(random.uniform(0.0003, 0.0015), 6)
    vol_write_latency = round(random.uniform(0.0002, 0.0010), 6)

    # Counters should be monotonically increasing; keep in-memory state.
    # Simple approach: approximate with time-based counters.
    now = time.time()
    reads_total = int(now)  # monotonically increasing
    writes_total = int(now) // 2

    read_throughput = random.randint(0, 50000)   # bytes/sec
    write_throughput = random.randint(0, 50000)  # bytes/sec

    out = []
    # ----- Node/cluster metrics -----
    out += [
        "# HELP px_cluster_cpu_percent Percentage of CPU Used",
        "# TYPE px_cluster_cpu_percent gauge",
        line("px_cluster_cpu_percent", LABELS_NODE, cpu_percent),
        "",
        "# HELP px_cluster_disk_total_bytes Total storage space in bytes for this node",
        "# TYPE px_cluster_disk_total_bytes gauge",
        line("px_cluster_disk_total_bytes", LABELS_NODE, f"{disk_total:.12g}"),
        "",
        "# HELP px_cluster_disk_utilized_bytes Utilized storage space in bytes for this node",
        "# TYPE px_cluster_disk_utilized_bytes gauge",
        line("px_cluster_disk_utilized_bytes", LABELS_NODE, f"{disk_used:.12g}"),
        "",
        "# HELP px_cluster_status_nodes_offline Number of offline nodes in the cluster (includes storage and storageless)",
        "# TYPE px_cluster_status_nodes_offline gauge",
        line("px_cluster_status_nodes_offline", LABELS_NODE, nodes_offline),
        "",
        "# HELP px_cluster_status_nodes_online Number of online nodes in the cluster (includes storage and storageless)",
        "# TYPE px_cluster_status_nodes_online gauge",
        line("px_cluster_status_nodes_online", LABELS_NODE, nodes_online),
        "",
    ]

    # ----- Volume metrics -----
    out += [
        "# HELP px_volume_read_latency_seconds Average time spent per successfully completed read operation in seconds for this volume",
        "# TYPE px_volume_read_latency_seconds gauge",
        line("px_volume_read_latency_seconds", LABELS_VOL, vol_read_latency),
        "",
        "# HELP px_volume_reads_total Total number of successfully completed read operations for this volume",
        "# TYPE px_volume_reads_total counter",
        line("px_volume_reads_total", LABELS_VOL, reads_total),
        "",
        "# HELP px_volume_readthroughput Number of bytes read per second during this interval for this volume",
        "# TYPE px_volume_readthroughput gauge",
        line("px_volume_readthroughput", LABELS_VOL, read_throughput),
        "",
        "# HELP px_volume_write_latency_seconds Average time spent per successfully completed write operation in seconds for this volume",
        "# TYPE px_volume_write_latency_seconds gauge",
        line("px_volume_write_latency_seconds", LABELS_VOL, vol_write_latency),
        "",
        "# HELP px_volume_writes_total Total number of successfully completed write operations for this volume",
        "# TYPE px_volume_writes_total counter",
        line("px_volume_writes_total", LABELS_VOL, writes_total),
        "",
        "# HELP px_volume_writethroughput Number of bytes written per second during this interval for this volume",
        "# TYPE px_volume_writethroughput gauge",
        line("px_volume_writethroughput", LABELS_VOL, write_throughput),
        "",
    ]

    body = "\n".join(out) + "\n"
    return Response(body, mimetype="text/plain; version=0.0.4; charset=utf-8")

if __name__ == "__main__":
    # Expose on all interfaces so Prometheus can scrape it
    app.run(host="0.0.0.0", port=17001)