from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]


class MkDocsConfigLoader(yaml.SafeLoader):
    pass


def construct_python_name(loader: MkDocsConfigLoader, suffix: str, node: yaml.Node) -> str:
    return suffix


MkDocsConfigLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:", construct_python_name
)


@dataclass(frozen=True)
class WorkshopSite:
    name: str
    config_path: Path

    @property
    def config(self) -> dict[str, Any]:
        return yaml.load(
            self.config_path.read_text(encoding="utf-8"),
            Loader=MkDocsConfigLoader,
        )

    @property
    def docs_dir(self) -> Path:
        return REPO_ROOT / self.config["docs_dir"]


@dataclass(frozen=True)
class ShellCommand:
    site: WorkshopSite
    path: Path
    line: int
    language: str
    text: str
    tool: str

    @property
    def location(self) -> str:
        return f"{self.path.relative_to(REPO_ROOT)}:{self.line}"


WORKSHOP_SITES = (
    WorkshopSite("shopmate", REPO_ROOT / "mkdocs.yml"),
    WorkshopSite("ticketmate", REPO_ROOT / "mkdocs-ticketmate.yml"),
)

FORBIDDEN_STUDENT_TEXT = (
    "Use this framing during the lab",
    "Do not tell students",
    "Then connect it to production",
    "This distinction helps students",
    "full physical Cisco AI POD",
)

JWT_PATTERN = re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b")

SHELL_FENCE_LANGUAGES = {
    "bash",
    "console",
    "powershell",
    "pwsh",
    "sh",
    "shell",
    "zsh",
}
KUBE_COMMAND_TOOLS = ("kubectl", "helm", "envsubst")
GENERATED_STUDENT_FILES = {
    "shopmate-ai.yaml",
    "student-collector-values.yaml",
    "ticketmate-ai.yaml",
}
BUILT_IN_COLLECTOR_PROCESSORS = {"batch", "memory_limiter"}
BUILT_IN_COLLECTOR_EXPORTERS = {"otlp_http"}


def source_yaml_files() -> tuple[Path, ...]:
    roots = [
        REPO_ROOT,
        REPO_ROOT / "workshop",
        REPO_ROOT / "workshop-ticketmate",
        REPO_ROOT / "infra",
    ]
    files: set[Path] = set()
    for root in roots:
        files.update(root.glob("*.yml"))
        files.update(root.glob("*.yaml"))
        if root != REPO_ROOT:
            files.update(root.rglob("*.yml"))
            files.update(root.rglob("*.yaml"))
    return tuple(
        sorted(
            path
            for path in files
            if "site" not in path.relative_to(REPO_ROOT).parts
            and "site-ticketmate" not in path.relative_to(REPO_ROOT).parts
        )
    )


SOURCE_YAML_FILES = source_yaml_files()


def nav_entries(nav: list[Any]) -> list[str]:
    entries: list[str] = []
    for item in nav:
        if isinstance(item, str):
            entries.append(item)
        elif isinstance(item, dict):
            for value in item.values():
                if isinstance(value, str):
                    entries.append(value)
                elif isinstance(value, list):
                    entries.extend(nav_entries(value))
    return entries


def fenced_code_blocks(markdown: str) -> list[tuple[str, int, list[str]]]:
    blocks: list[tuple[str, int, list[str]]] = []
    in_fence = False
    language = ""
    start_line = 0
    lines: list[str] = []

    for line_number, line in enumerate(markdown.splitlines(), start=1):
        fence_match = re.match(r"^\s*```([^`]*)\s*$", line)
        if fence_match:
            if not in_fence:
                in_fence = True
                language = (fence_match.group(1).split() or [""])[0].lower()
                start_line = line_number + 1
                lines = []
            else:
                blocks.append((language, start_line, lines))
                in_fence = False
            continue

        if in_fence:
            lines.append(line)

    return blocks


def strip_shell_prompt(line: str) -> str:
    return re.sub(r"^(?:\$|PS>|>)\s+", "", line.strip())


def logical_shell_lines(lines: list[str], start_line: int, language: str) -> list[tuple[int, str]]:
    logical_lines: list[tuple[int, str]] = []
    current: list[str] = []
    current_line = start_line
    continuation_marker = "`" if language in {"powershell", "pwsh"} else "\\"

    for offset, raw_line in enumerate(lines):
        line = strip_shell_prompt(raw_line)
        if not line or line.startswith("#"):
            continue

        if not current:
            current_line = start_line + offset

        continues = line.endswith(continuation_marker)
        if continues:
            line = line[: -len(continuation_marker)].rstrip()

        current.append(line)
        if continues:
            continue

        logical_lines.append((current_line, " ".join(current)))
        current = []

    if current:
        logical_lines.append((current_line, " ".join(current)))

    return logical_lines


def command_tool(command: str) -> str | None:
    command = command.strip()
    for tool in KUBE_COMMAND_TOOLS:
        if command == tool or command.startswith(f"{tool} "):
            return tool
    return None


def iter_kube_shell_commands() -> list[ShellCommand]:
    commands: list[ShellCommand] = []
    for site in WORKSHOP_SITES:
        for markdown_file in site.docs_dir.glob("*.md"):
            markdown = markdown_file.read_text(encoding="utf-8")
            for language, start_line, block_lines in fenced_code_blocks(markdown):
                if language not in SHELL_FENCE_LANGUAGES:
                    continue
                for line, command in logical_shell_lines(block_lines, start_line, language):
                    tool = command_tool(command)
                    if tool:
                        commands.append(
                            ShellCommand(
                                site=site,
                                path=markdown_file,
                                line=line,
                                language=language,
                                text=command,
                                tool=tool,
                            )
                        )
    return commands


def markdown_links(markdown: str) -> list[str]:
    links: list[str] = []
    for pattern in (
        r"(?<!!)\[[^\]]+\]\(([^)]+)\)",
        r"!\[[^\]]*\]\(([^)]+)\)",
    ):
        links.extend(match.group(1).strip() for match in re.finditer(pattern, markdown))
    return links


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and ">" in target:
        return target[1 : target.index(">")]
    return target.split()[0]


def is_external_link(target: str) -> bool:
    return bool(re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE))


def source_path_for_site_link(site: WorkshopSite, source: Path, target: str) -> Path | None:
    target = normalize_link_target(target)
    if not target or target.startswith("#") or is_external_link(target):
        return None

    path_part = target.split("#", 1)[0]
    if not path_part:
        return None

    if path_part.startswith("/"):
        return REPO_ROOT / path_part.lstrip("/")

    return (source.parent / path_part).resolve()


def load_yaml_documents(path: Path) -> list[Any]:
    with path.open("r", encoding="utf-8") as handle:
        return [doc for doc in yaml.safe_load_all(handle) if doc is not None]


def load_source_yaml_documents(path: Path) -> list[Any]:
    loader = MkDocsConfigLoader if path.name.startswith("mkdocs") else yaml.SafeLoader
    with path.open("r", encoding="utf-8") as handle:
        return [doc for doc in yaml.load_all(handle, Loader=loader) if doc is not None]


def load_server_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def has_student_namespace(command: str) -> bool:
    return bool(
        re.search(
            r"(?<!\S)(?:-n|--namespace)(?:=|\s+)(?:\"?\$STUDENT_NAMESPACE\"?|\$env:STUDENT_NAMESPACE)",
            command,
        )
    )


def kubectl_command_requires_namespace(command: str) -> bool:
    pieces = command.split()
    if len(pieces) < 2:
        return False
    return pieces[1] not in {"config", "version"}


def helm_command_requires_namespace(command: str) -> bool:
    pieces = command.split()
    if len(pieces) < 2:
        return False
    return pieces[1] not in {"repo", "search", "version"}


def command_file_references(command: str) -> list[str]:
    refs: list[str] = []
    refs.extend(
        match.group("path")
        for match in re.finditer(
            r"(?<!\S)(?:-f|--filename|--values)(?:=|\s+)(?P<path>[^\s|\\]+)",
            command,
        )
    )
    refs.extend(
        match.group("path")
        for match in re.finditer(r"(?<!\S)envsubst\s+<\s*(?P<path>[^\s>]+)", command)
    )
    return [ref.strip("\"'") for ref in refs]


def resolves_for_student_workdir(command: ShellCommand, ref: str) -> bool:
    if ref in {"-", "/dev/stdin"} or "$" in ref:
        return True

    ref_path = Path(ref)
    if ref_path.name in GENERATED_STUDENT_FILES:
        return True

    candidates = [
        command.path.parent / ref_path,
        command.site.docs_dir / ref_path,
        command.site.docs_dir / "lab-files" / ref_path.name,
        REPO_ROOT / ref_path,
    ]
    return any(candidate.exists() for candidate in candidates)


def env_entries(container: dict[str, Any]) -> list[dict[str, Any]]:
    return container.get("env") or []


def containers_for_deployment(deployment: dict[str, Any]) -> list[dict[str, Any]]:
    return deployment["spec"]["template"]["spec"].get("containers") or []


def container_port_names(deployment: dict[str, Any]) -> set[str]:
    names: set[str] = set()
    for container in containers_for_deployment(deployment):
        for port in container.get("ports") or []:
            if "name" in port:
                names.add(port["name"])
    return names


def container_port_numbers(deployment: dict[str, Any]) -> set[int]:
    numbers: set[int] = set()
    for container in containers_for_deployment(deployment):
        for port in container.get("ports") or []:
            if "containerPort" in port:
                numbers.add(port["containerPort"])
    return numbers


def document_id(path: Path, index: int, doc: dict[str, Any]) -> str:
    rel_path = path.relative_to(REPO_ROOT)
    kind = doc.get("kind", "unknown")
    name = doc.get("metadata", {}).get("name", "unnamed")
    return f"{rel_path} document {index + 1} ({kind}/{name})"


def collector_value_files() -> tuple[Path, ...]:
    return tuple(
        path
        for path in SOURCE_YAML_FILES
        if "collector-values" in path.name
        or path.name == "collector-observability-snippet.yaml"
    )


@pytest.mark.parametrize("site", WORKSHOP_SITES, ids=lambda site: site.name)
def test_mkdocs_site_builds_strictly(site: WorkshopSite, tmp_path: Path) -> None:
    subprocess.run(
        [
            sys.executable,
            "-m",
            "mkdocs",
            "build",
            "--strict",
            "-f",
            str(site.config_path),
            "--site-dir",
            str(tmp_path / site.name),
        ],
        cwd=REPO_ROOT,
        check=True,
    )


@pytest.mark.parametrize("site", WORKSHOP_SITES, ids=lambda site: site.name)
def test_all_workshop_pages_are_in_navigation(site: WorkshopSite) -> None:
    nav_pages = {Path(entry) for entry in nav_entries(site.config["nav"])}
    markdown_pages = {path.relative_to(site.docs_dir) for path in site.docs_dir.glob("*.md")}

    assert markdown_pages <= nav_pages

    for page in nav_pages:
        assert (site.docs_dir / page).is_file(), f"{site.name} nav references missing page {page}"


@pytest.mark.parametrize("site", WORKSHOP_SITES, ids=lambda site: site.name)
def test_student_pages_do_not_include_instructor_only_notes(site: WorkshopSite) -> None:
    failures: list[str] = []
    for markdown_file in site.docs_dir.glob("*.md"):
        text = markdown_file.read_text(encoding="utf-8")
        for forbidden in FORBIDDEN_STUDENT_TEXT:
            if forbidden in text:
                failures.append(f"{markdown_file.relative_to(REPO_ROOT)} contains {forbidden!r}")

    assert failures == []


@pytest.mark.parametrize("site", WORKSHOP_SITES, ids=lambda site: site.name)
def test_internal_workshop_links_resolve(site: WorkshopSite) -> None:
    failures: list[str] = []
    for markdown_file in site.docs_dir.glob("*.md"):
        text = markdown_file.read_text(encoding="utf-8")
        for raw_target in markdown_links(text):
            resolved = source_path_for_site_link(site, markdown_file, raw_target)
            if resolved is None:
                continue
            if not resolved.exists():
                failures.append(
                    f"{markdown_file.relative_to(REPO_ROOT)} links to missing {raw_target!r}"
                )

    assert failures == []


def test_workshop_kube_commands_are_extracted_from_shell_blocks() -> None:
    commands = iter_kube_shell_commands()
    command_text = "\n".join(command.text for command in commands)

    assert commands
    assert "kubectl apply" in command_text
    assert "helm upgrade --install" in command_text
    assert "envsubst <" in command_text


def test_kubectl_commands_are_student_namespace_scoped() -> None:
    failures = [
        f"{command.location}: {command.text}"
        for command in iter_kube_shell_commands()
        if command.tool == "kubectl"
        and kubectl_command_requires_namespace(command.text)
        and not has_student_namespace(command.text)
    ]

    assert failures == []


def test_helm_release_commands_are_student_namespace_scoped() -> None:
    failures = [
        f"{command.location}: {command.text}"
        for command in iter_kube_shell_commands()
        if command.tool == "helm"
        and helm_command_requires_namespace(command.text)
        and not has_student_namespace(command.text)
    ]

    assert failures == []


def test_kube_commands_avoid_cluster_wide_destructive_flags() -> None:
    failures: list[str] = []
    for command in iter_kube_shell_commands():
        if "--all-namespaces" in command.text:
            failures.append(f"{command.location}: uses --all-namespaces")
        if command.tool == "kubectl" and re.search(r"\bkubectl\s+delete\b", command.text):
            if re.search(r"(?<!\S)--all(?:\s|$|=)", command.text):
                failures.append(f"{command.location}: delete uses --all")

    assert failures == []


def test_kube_command_file_references_resolve() -> None:
    failures: list[str] = []
    for command in iter_kube_shell_commands():
        for ref in command_file_references(command.text):
            if not resolves_for_student_workdir(command, ref):
                failures.append(f"{command.location}: {command.text} references missing {ref!r}")

    assert failures == []


def test_kube_commands_do_not_use_unresolved_angle_placeholders() -> None:
    placeholder_pattern = re.compile(r"<[A-Z0-9_-]+>")
    failures = [
        f"{command.location}: {command.text}"
        for command in iter_kube_shell_commands()
        if placeholder_pattern.search(command.text)
    ]

    assert failures == []


@pytest.mark.parametrize(
    "path",
    SOURCE_YAML_FILES,
    ids=lambda path: str(path.relative_to(REPO_ROOT)),
)
def test_source_yaml_files_parse(path: Path) -> None:
    assert load_source_yaml_documents(path), f"{path.relative_to(REPO_ROOT)} did not contain YAML documents"


@pytest.mark.parametrize(
    "path",
    SOURCE_YAML_FILES,
    ids=lambda path: str(path.relative_to(REPO_ROOT)),
)
def test_kubernetes_manifest_documents_have_required_identity(path: Path) -> None:
    failures: list[str] = []
    for index, doc in enumerate(load_source_yaml_documents(path)):
        if not isinstance(doc, dict) or "kind" not in doc:
            continue
        if doc["kind"] == "Config":
            continue
        metadata = doc.get("metadata")
        if not doc.get("apiVersion"):
            failures.append(f"{document_id(path, index, doc)} is missing apiVersion")
        if not isinstance(metadata, dict):
            failures.append(f"{document_id(path, index, doc)} is missing metadata")
            continue
        if not metadata.get("name"):
            failures.append(f"{document_id(path, index, doc)} is missing metadata.name")

    assert failures == []


@pytest.mark.parametrize(
    "path",
    SOURCE_YAML_FILES,
    ids=lambda path: str(path.relative_to(REPO_ROOT)),
)
def test_deployment_selectors_env_and_probes_are_consistent(path: Path) -> None:
    failures: list[str] = []
    for index, doc in enumerate(load_source_yaml_documents(path)):
        if not isinstance(doc, dict) or doc.get("kind") != "Deployment":
            continue
        doc_name = document_id(path, index, doc)
        selector = doc["spec"].get("selector", {}).get("matchLabels") or {}
        pod_labels = doc["spec"]["template"].get("metadata", {}).get("labels") or {}
        if selector.items() - pod_labels.items():
            failures.append(f"{doc_name} selector labels are not present on the pod template")

        port_names = container_port_names(doc)
        port_numbers = container_port_numbers(doc)
        for container in containers_for_deployment(doc):
            env_names = [entry.get("name") for entry in env_entries(container) if "name" in entry]
            if len(env_names) != len(set(env_names)):
                failures.append(f"{doc_name} container {container.get('name')} has duplicate env vars")
            resources = container.get("resources") or {}
            if not resources.get("requests") or not resources.get("limits"):
                failures.append(f"{doc_name} container {container.get('name')} is missing resource requests or limits")
            for probe_name in ("readinessProbe", "livenessProbe"):
                probe = container.get(probe_name)
                if not probe:
                    failures.append(f"{doc_name} container {container.get('name')} is missing {probe_name}")
                    continue
                port = probe.get("httpGet", {}).get("port")
                if isinstance(port, str) and port not in port_names:
                    failures.append(f"{doc_name} {probe_name} references unknown port name {port!r}")
                if isinstance(port, int) and port not in port_numbers:
                    failures.append(f"{doc_name} {probe_name} references unknown port number {port}")

    assert failures == []


@pytest.mark.parametrize(
    "path",
    SOURCE_YAML_FILES,
    ids=lambda path: str(path.relative_to(REPO_ROOT)),
)
def test_services_select_matching_deployments_and_ports(path: Path) -> None:
    docs = [
        doc
        for doc in load_source_yaml_documents(path)
        if isinstance(doc, dict) and "kind" in doc
    ]
    deployments = [
        doc
        for doc in docs
        if doc.get("kind") == "Deployment"
    ]
    failures: list[str] = []

    for index, service in enumerate(docs):
        if service.get("kind") != "Service":
            continue
        doc_name = document_id(path, index, service)
        metadata = service.get("metadata", {})
        namespace = metadata.get("namespace")
        selector = service.get("spec", {}).get("selector") or {}
        if not selector:
            failures.append(f"{doc_name} is missing spec.selector")
            continue

        matching_deployments = []
        for deployment in deployments:
            deployment_namespace = deployment.get("metadata", {}).get("namespace")
            pod_labels = deployment["spec"]["template"].get("metadata", {}).get("labels") or {}
            if deployment_namespace == namespace and selector.items() <= pod_labels.items():
                matching_deployments.append(deployment)

        if not matching_deployments:
            failures.append(f"{doc_name} selector does not match a Deployment in the same file")
            continue

        target_names = set().union(*(container_port_names(deployment) for deployment in matching_deployments))
        target_numbers = set().union(*(container_port_numbers(deployment) for deployment in matching_deployments))
        for port in service.get("spec", {}).get("ports") or []:
            target_port = port.get("targetPort", port.get("port"))
            if isinstance(target_port, str) and target_port not in target_names:
                failures.append(f"{doc_name} targetPort {target_port!r} does not match a container port name")
            if isinstance(target_port, int) and target_port not in target_numbers:
                failures.append(f"{doc_name} targetPort {target_port} does not match a container port number")

    assert failures == []


@pytest.mark.parametrize(
    "path",
    collector_value_files(),
    ids=lambda path: str(path.relative_to(REPO_ROOT)),
)
def test_collector_values_reference_defined_pipeline_components(path: Path) -> None:
    config = load_source_yaml_documents(path)[0].get("gateway", {}).get("config")
    assert config, f"{path.relative_to(REPO_ROOT)} is missing gateway.config"

    receivers = set(config.get("receivers") or {})
    processors = set(config.get("processors") or {}) | BUILT_IN_COLLECTOR_PROCESSORS
    exporters = set(config.get("exporters") or {}) | BUILT_IN_COLLECTOR_EXPORTERS
    pipelines = config.get("service", {}).get("pipelines") or {}
    failures: list[str] = []

    for pipeline_name, pipeline in pipelines.items():
        for receiver in pipeline.get("receivers") or []:
            if receiver not in receivers:
                failures.append(f"{path.relative_to(REPO_ROOT)} pipeline {pipeline_name} references missing receiver {receiver}")
        for processor in pipeline.get("processors") or []:
            if processor not in processors:
                failures.append(f"{path.relative_to(REPO_ROOT)} pipeline {pipeline_name} references missing processor {processor}")
        for exporter in pipeline.get("exporters") or []:
            if exporter not in exporters:
                failures.append(f"{path.relative_to(REPO_ROOT)} pipeline {pipeline_name} references missing exporter {exporter}")

    assert failures == []


def test_student_kubeconfig_contexts_are_namespace_scoped() -> None:
    kubeconfig_path = REPO_ROOT / "workshop/lab-files/student-kubeconfig.yaml"
    kubeconfig = load_source_yaml_documents(kubeconfig_path)[0]
    context_names = {context["name"] for context in kubeconfig["contexts"]}
    user_names = {user["name"] for user in kubeconfig["users"]}
    cluster_names = {cluster["name"] for cluster in kubeconfig["clusters"]}
    failures: list[str] = []

    if kubeconfig["current-context"] not in context_names:
        failures.append("current-context does not match a named context")

    for context in kubeconfig["contexts"]:
        name = context["name"]
        details = context["context"]
        if details.get("namespace") != name:
            failures.append(f"context {name} namespace does not match its context name")
        if details.get("user") not in user_names:
            failures.append(f"context {name} references missing user {details.get('user')}")
        if details.get("cluster") not in cluster_names:
            failures.append(f"context {name} references missing cluster {details.get('cluster')}")

    assert failures == []


def test_student_kubeconfig_does_not_commit_bearer_token() -> None:
    kubeconfig_path = REPO_ROOT / "workshop/lab-files/student-kubeconfig.yaml"
    kubeconfig = load_source_yaml_documents(kubeconfig_path)[0]
    failures: list[str] = []

    for user in kubeconfig.get("users", []):
        token = user.get("user", {}).get("token", "")
        if JWT_PATTERN.search(token):
            failures.append(f"{kubeconfig_path.relative_to(REPO_ROOT)} user {user.get('name')} contains a JWT token")
        if token and not token.startswith("REPLACE_WITH_"):
            failures.append(f"{kubeconfig_path.relative_to(REPO_ROOT)} user {user.get('name')} token is not a placeholder")

    assert failures == []


@pytest.mark.parametrize(
    ("path", "deployment_name", "expected_env"),
    [
        (
            REPO_ROOT / "workshop/lab-files/shopmate-ai.yaml",
            "shopmate-ai",
            {
                "OTEL_SERVICE_NAME": "shopmate-ai",
                "OTEL_EXPORTER_OTLP_ENDPOINT": "http://student-collector:4318",
                "OTEL_EXPORTER_OTLP_PROTOCOL": "http/protobuf",
                "OTEL_INSTRUMENTATION_GENAI_EMITTERS": "span_metric",
            },
        ),
        (
            REPO_ROOT / "workshop-ticketmate/lab-files/ticketmate-ai.yaml",
            "ticketmate-ai",
            {
                "OTEL_SERVICE_NAME": "ticketmate-ai",
                "OTEL_EXPORTER_OTLP_ENDPOINT": "http://student-collector:4318",
                "OTEL_EXPORTER_OTLP_PROTOCOL": "http/protobuf",
                "OTEL_INSTRUMENTATION_GENAI_EMITTERS": "span_metric",
            },
        ),
    ],
    ids=lambda item: item.name if isinstance(item, Path) else str(item),
)
def test_app_manifests_match_student_runtime_contract(
    path: Path, deployment_name: str, expected_env: dict[str, str]
) -> None:
    docs = load_yaml_documents(path)
    deployment = next(
        doc
        for doc in docs
        if doc.get("kind") == "Deployment" and doc["metadata"]["name"] == deployment_name
    )
    service = next(
        doc
        for doc in docs
        if doc.get("kind") == "Service" and doc["metadata"]["name"] == deployment_name
    )
    container = deployment["spec"]["template"]["spec"]["containers"][0]
    env = {entry["name"]: entry.get("value") for entry in container["env"] if "value" in entry}

    assert container["ports"][0]["containerPort"] == 8080
    assert container["readinessProbe"]["httpGet"]["path"] == "/healthz"
    assert container["livenessProbe"]["httpGet"]["path"] == "/healthz"
    assert service["spec"]["ports"][0]["port"] == 8080
    assert service["spec"]["ports"][0]["targetPort"] == "http"
    assert env | expected_env == env
    assert "deployment.environment" in env["OTEL_RESOURCE_ATTRIBUTES"]


@pytest.mark.parametrize(
    "path",
    [
        REPO_ROOT / "workshop/lab-files/collector-observability-snippet.yaml",
        REPO_ROOT / "workshop/lab-files/student-collector-values-gpu-nim-reference.yaml",
        REPO_ROOT / "workshop-ticketmate/lab-files/ticketmate-collector-values.yaml",
    ],
    ids=lambda path: str(path.relative_to(REPO_ROOT)),
)
def test_student_collector_values_keep_gpu_nim_pipeline_separate(path: Path) -> None:
    config = load_yaml_documents(path)[0]["gateway"]["config"]

    assert config["exporters"]["signalfx"]["send_otlp_histograms"] is True
    assert "prometheus/gpu_nim" in config["receivers"]
    assert "filter/gpu_nim_allowlist" in config["processors"]

    pipelines = config["service"]["pipelines"]
    assert pipelines["metrics"]["receivers"] == ["otlp"]
    assert "filter/gpu_nim_allowlist" not in pipelines["metrics"]["processors"]
    assert pipelines["metrics/gpu_nim"]["receivers"] == ["prometheus/gpu_nim"]
    assert "filter/gpu_nim_allowlist" in pipelines["metrics/gpu_nim"]["processors"]


def test_shopmate_data_path_produces_grounded_recommendations() -> None:
    shopmate = load_server_module("shopmate_server_under_test", REPO_ROOT / "shopmate-sports/server.py")

    matches = shopmate.catalog_matches("I need wide trail shoes under $170", limit=3)
    reply = shopmate.compose_grounded_reply("I need wide trail shoes under $170 and pickup options")

    assert matches
    assert all("name" in product and "price" in product for product in matches)
    assert "Best matches from the demo catalog" in reply
    assert "Inventory examples" in reply
    assert "Practical next step" in reply


def test_ticketmate_data_path_produces_grounded_event_context() -> None:
    ticketmate = load_server_module("ticketmate_server_under_test", REPO_ROOT / "ticketmate-ai/server.py")

    search_payload = json.loads(ticketmate.search_events_data("jazz tickets in Chicago"))
    first_event = search_payload["matches"][0]
    price_payload = json.loads(ticketmate.estimate_total_price_data(first_event["id"], quantity=2))
    policy_payload = json.loads(ticketmate.lookup_venue_policy_data(first_event["venue"], "refund"))

    assert first_event["id"]
    assert first_event["lowest_total_per_ticket"] > 0
    assert price_payload["estimated_total"] == price_payload["total_per_ticket"] * 2
    assert "Workshop estimate only" in price_payload["note"]
    assert policy_payload["venue"] == first_event["venue"]
