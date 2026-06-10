from __future__ import annotations

import re
import shutil
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile


ROOT = Path("/Users/mkuglerr/code2/codex_projects/ai-pods")
TEMPLATE = ROOT / "deliverables" / "CiscoLive2026-template.pptx"
OUTPUT = ROOT / "deliverables" / "CLUS-LTROBS-2001-workshop-deck.pptx"

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}

for prefix, uri in NS.items():
    ET.register_namespace(prefix if prefix != "pr" else "", uri)


KEEP_SLIDES = [8, 13, 22, 57, 47, 50, 54, 58, 43, 69]

SLIDE_TEXT = {
    8: [
        "CLUS-LTROBS-2001",
        "From Deployment to Deep Insights: Mastering AI/ML with Cisco AI Pods & Splunk",
        "Workshop delivery model\nShared AWS EKS cluster, one namespace per student",
        "EKS-based Cisco Live lab\nTerraform-managed instructor infrastructure",
        "Session ID: CLUS-LTROBS-2001",
    ],
    13: [
        "Agenda",
        "1. Shared lab architecture and student workflow\n2. What the lab team pre-stages\n3. Collector deployment and configuration\n4. GPU and AI workload dashboards\n5. Troubleshooting and analysis in Splunk\n6. Scale and delivery considerations",
        "Session ID: CLUS-LTROBS-2001",
    ],
    22: [
        "Workshop goals",
        "What this lab teaches",
        "Instrument workloads",
        "Collect telemetry",
        "Analyze in Splunk",
        "Session ID: CLUS-LTROBS-2001",
    ],
    57: [
        "Workshop model",
        "One shared cluster, real student setup",
        "Each student gets namespace-scoped Kubernetes access to a dedicated namespace in the shared EKS cluster. Shared GPU and AI services stay centrally managed. Students still do the hands-on monitoring work by deploying and updating their own namespace-scoped Splunk OpenTelemetry Collector, validating ingest, and analyzing dashboards in Splunk Observability Cloud.",
        "Session ID: CLUS-LTROBS-2001",
    ],
    47: [
        "Ownership model",
        "Shared by lab team",
        "AWS EKS cluster, GPU nodes, Kubernetes operators, NIM models, cluster-wide infrastructure collection, and the Splunk organization are pre-staged once for the event.",
        "Done by each student",
        "Students connect to EKS with namespace-scoped credentials, work in their namespace, deploy or update their collector, configure receivers and exporters, validate telemetry, and investigate a bounded agent-loop token burn scenario.",
        "Session ID: CLUS-LTROBS-2001",
    ],
    50: [
        "Telemetry layers",
        "GPU and platform",
        "GPU utilization, memory pressure, node health, Kubernetes state, and shared AI service status show whether the infrastructure is healthy and where saturation begins.",
        "Application and model",
        "Request rate, latency, queue depth, token generation, traces, and service health show how the AI workload behaves from the user point of view.",
        "Correlation and insight",
        "Students learn to connect symptom to signal: a latency spike should line up with queue growth, GPU pressure, or application errors rather than isolated random charts.",
        "Session ID: CLUS-LTROBS-2001",
    ],
    54: [
        "Student workflow",
        "In each namespace",
        "Access and verify\nConfirm your namespace, services, credentials, and baseline health before changing collector config.",
        "Configure and collect\nDeploy or update the Splunk OTel Collector and enable the receivers and exporters required for the workshop.",
        "Analyze and explain\nUse dashboards and traces to identify what changed, what signal matters, and what the likely root cause is.",
        "Session ID: CLUS-LTROBS-2001",
    ],
    58: [
        "Student setup",
        "What every attendee needs",
        "Per student",
        "One namespace-scoped Kubernetes identity, one namespace, one collector deployment, access to Splunk Observability Cloud, and the workshop files for the lab.",
        "Session ID: CLUS-LTROBS-2001",
    ],
    43: [
        "Instructor checklist",
        "Pre-create student identities and namespaces. Validate kubectl, Helm, kubeconfig, Splunk access tokens, and realm settings. Run a scale test for 40 collectors before the event. Prepare a reset path for namespaces and a live dashboard view for the instructor team.",
        "Session ID: CLUS-LTROBS-2001",
    ],
    69: [
        "Questions?",
    ],
}


def slide_xml_path(num: int) -> str:
    return f"ppt/slides/slide{num}.xml"


def all_text_shapes(root: ET.Element) -> list[ET.Element]:
    shapes = []
    for sp in root.findall(".//p:sp", NS):
        texts = [t for t in sp.findall(".//a:t", NS)]
        if texts:
            shapes.append(sp)
    return shapes


def replace_shape_text(shape: ET.Element, new_text: str) -> None:
    text_nodes = shape.findall(".//a:t", NS)
    if not text_nodes:
        return
    text_nodes[0].text = new_text
    for node in text_nodes[1:]:
        node.text = ""


def update_slide_text(path: Path, slide_num: int) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    shapes = all_text_shapes(root)
    expected = SLIDE_TEXT[slide_num]
    if len(shapes) != len(expected):
        raise ValueError(
            f"slide {slide_num}: expected {len(expected)} text shapes, found {len(shapes)}"
        )
    for shape, text in zip(shapes, expected):
        replace_shape_text(shape, text)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def reorder_presentation(path: Path) -> None:
    rels_tree = ET.parse(path / "ppt" / "_rels" / "presentation.xml.rels")
    rels_root = rels_tree.getroot()

    rid_by_slide = {}
    for rel in rels_root.findall("pr:Relationship", NS):
        target = rel.attrib.get("Target", "")
        match = re.search(r"slides/slide(\d+)\.xml$", target)
        if match:
            rid_by_slide[int(match.group(1))] = rel.attrib["Id"]

    pres_tree = ET.parse(path / "ppt" / "presentation.xml")
    pres_root = pres_tree.getroot()
    sld_id_lst = pres_root.find("p:sldIdLst", NS)
    if sld_id_lst is None:
        raise ValueError("presentation.xml missing p:sldIdLst")

    old_elems = list(sld_id_lst)
    elem_by_rid = {elem.attrib[f'{{{NS["r"]}}}id']: elem for elem in old_elems}

    for elem in old_elems:
        sld_id_lst.remove(elem)

    for index, slide_num in enumerate(KEEP_SLIDES, start=1):
        rid = rid_by_slide[slide_num]
        elem = elem_by_rid[rid]
        elem.attrib["id"] = str(256 + index)
        sld_id_lst.append(elem)

    pres_tree.write(path / "ppt" / "presentation.xml", encoding="utf-8", xml_declaration=True)


def build_deck() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        unpacked = tmpdir_path / "pptx"
        unpacked.mkdir()

        with ZipFile(TEMPLATE) as src:
            src.extractall(unpacked)

        for slide_num in KEEP_SLIDES:
            update_slide_text(unpacked / slide_xml_path(slide_num), slide_num)

        reorder_presentation(unpacked)

        with ZipFile(OUTPUT, "w") as dst:
            for file in sorted(unpacked.rglob("*")):
                if file.is_file():
                    dst.write(file, file.relative_to(unpacked).as_posix())


if __name__ == "__main__":
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    build_deck()
    print(OUTPUT)
