# llama2.c Training Workload Plan

## Summary

Use current upstream `karpathy/llama2.c` as the base training workload, then
port only the useful ideas from `marciokugler/llama2.c`: instruction-style
Alpaca and OpenAssistant dataset adapters plus short training profiles.

Do not use the old fork directly for the lab baseline. The fork is valuable
as a reference, but it is older than current upstream and carries dataset,
validation, and hardware-specific assumptions that should be cleaned up during
the port.

References:

- Upstream base: <https://github.com/karpathy/llama2.c>
- Upstream commit inspected: `350e04fe35433e6d2941dce5a1f53308f87058eb`
- Fork reference: <https://github.com/marciokugler/llama2.c>
- Fork commit inspected: `32c8b5c83f535329075d4fc91b6dc09a491a9fbf`

## Goals

- Create a real, instructor-run LLM training workload for the shared GPU
  cluster.
- Make training behavior visible in Splunk Observability Cloud.
- Let students investigate training problems using traces, metrics, logs,
  Kubernetes status, and GPU telemetry.
- Keep the workload bounded enough for the Cisco Live lab environment.
- Preserve the simplicity of `llama2.c` instead of turning it into a larger
  training framework.

## Key Decisions

- Use upstream `karpathy/llama2.c` as the source baseline.
- Treat `marciokugler/llama2.c` as a reference for dataset ideas only.
- Port Alpaca and OpenAssistant ingestion into small, lab-owned patch files.
- Keep the default lab run instructor-owned, not student-launched.
- Keep WandB disabled. Splunk Observability Cloud is the telemetry target.
- Keep ShopMate/NIM available unless the lab later pivots fully to training.

## What To Port From The Fork

Port these ideas:

- `alpaca` instruction/output dataset ingestion.
- `openassistant` role/text/lang filtering for English ready-for-export
  messages.
- Separate scenario profiles for TinyStories, Alpaca, and OpenAssistant.
- Short training runs that create visible GPU, CPU, memory, and data path
  behavior.

Do not port these fork behaviors as-is:

- hard-coded MFU calculation for a 3070 Ti
- commented-out train/validation split
- duplicated Alpaca record handling
- unused `pandas` and `treelib` dependencies
- old export flow where current upstream has newer `export.py`
- old upstream codebase with missing `runq.c`, tests, and docs

## Implementation Shape

Add a lab-owned build context:

```text
training/llama2c/
  README.md
  Dockerfile
  entrypoint.py
  otel_metrics.py
  profiles/
    healthy-tinystories.yaml
    instruction-alpaca.yaml
    instruction-openassistant.yaml
    gpu-oom.yaml
    data-pipeline-stall.yaml
  patches/
    001-add-instruction-datasets.patch
    002-add-lab-profile-runner.patch
  k8s/
    namespace.yaml
    pvc.yaml
    job-template.yaml
```

The image build should:

1. Clone upstream `karpathy/llama2.c` at the pinned commit.
2. Apply lab-owned patch files.
3. Install PyTorch, dataset, and OpenTelemetry dependencies.
4. Compile `run.c` and `runq.c`.
5. Use `entrypoint.py` to choose a profile, run preprocessing if needed,
   run training, parse stdout, and emit OTLP metrics.

## Dataset Adapters

### Alpaca

Use Stanford Alpaca data from:

```text
https://raw.githubusercontent.com/tatsu-lab/stanford_alpaca/main/alpaca_data.json
```

Format each record once:

```text
instruction: <instruction>
input: <input if present>
output: <output>
```

Create a deterministic train/validation split. Use a fixed seed and write
separate pretokenized files for train and validation.

### OpenAssistant

Use the OpenAssistant messages JSONL gzip from Hugging Face with raw/resolve
URLs only.

Filter records to:

```text
tree_state=ready_for_export
lang=en
```

Format records with role context:

```text
role: <role>
text: <message text>
```

Create a deterministic train/validation split. Do not rely on the same file
for both training and validation.

## Workload Profiles

### healthy-tinystories

Purpose:

- prove the training image, GPU scheduling, data cache, and metrics path work

Use current upstream TinyStories flow and a small bounded run.

### instruction-alpaca

Purpose:

- default instructor lab run
- connect the workload story to assistant-style training
- keep the data path simpler than OpenAssistant trees

Use a bounded run, not full convergence.

Recommended starting profile:

```text
dim=288
n_layers=6
n_heads=6
n_kv_heads=6
max_seq_len=512
batch_size=16
gradient_accumulation_steps=8
learning_rate=5e-4
dropout=0.0
max_iters=2000
eval_interval=200
eval_iters=20
compile=False
dtype=float16
```

### instruction-openassistant

Purpose:

- optional extension for more realistic conversational instruction data
- useful for data-pipeline and longer-sequence pressure

Keep this out of the default path until the Alpaca profile is validated.

### gpu-oom

Purpose:

- intentionally fail with GPU memory pressure

Increase sequence length, batch size, or model size until the job reliably
fails on the target `g5.4xlarge` A10G node.

### data-pipeline-stall

Purpose:

- show a training run blocked before meaningful GPU work begins

Trigger by using a missing, empty, or unmounted dataset cache.

## Kubernetes Design

Add an instructor-owned `training` namespace.

Default job behavior:

- `restartPolicy: Never`
- `backoffLimit: 0` for clear failure signals
- `nvidia.com/gpu: 1`
- PVC mount for dataset and checkpoint cache
- labels:
  - `app=llama2c-training`
  - `service.name=llama2c-training`
  - `workload.type=training`
  - `training.dataset=<dataset>`
  - `training.profile=<profile>`
  - `scenario.name=<scenario>`

If NIM already uses one GPU, this job should use the second GPU. If no GPU is
available, the Pending state becomes the scheduling investigation scenario.

## Observability

The entrypoint wrapper should parse training stdout and emit OTLP metrics:

```text
ai.training.iteration
ai.training.loss
ai.training.validation_loss
ai.training.learning_rate
ai.training.step_duration_ms
ai.training.tokens_per_iter
ai.training.tokens_processed
ai.training.mfu_pct
ai.training.failure
```

Required attributes:

```text
service.name=llama2c-training
workload.type=training
training.framework=pytorch
training.repo=karpathy/llama2.c
training.dataset=alpaca|openassistant|tinystories
training.profile=<profile>
training.run_id=<unique run id>
k8s.namespace.name=training
k8s.job.name=<job name>
scenario.name=<scenario>
```

Correlate those metrics with existing instructor-collected signals:

```text
DCGM_FI_DEV_GPU_UTIL
DCGM_FI_DEV_FB_USED
DCGM_FI_DEV_FB_FREE
DCGM_FI_DEV_MEM_COPY_UTIL
DCGM_FI_DEV_POWER_USAGE
k8s.pod.phase
k8s.container.restarts
container.cpu.utilization
container.memory.usage
```

## Splunk Investigation Runbook

Create:

```text
observability/training-investigation-runbook.md
```

Student investigation flow:

1. Find the active training run by `service.name=llama2c-training`.
2. Confirm iterations are increasing.
3. Confirm loss is finite and generally moving in the expected direction.
4. Check step duration and tokens processed.
5. Correlate the same time window with GPU utilization and GPU memory.
6. Check Kubernetes pod status, events, and restarts.
7. Decide whether the issue is healthy training, no GPU scheduled, GPU OOM,
   data pipeline failure, or CPU/data bottleneck.

Evidence table:

```text
training.run_id:
training.profile:
current pod phase:
latest iteration:
latest loss:
step duration:
GPU utilization:
GPU memory used:
Kubernetes event or failure:
likely cause:
```

## Test Plan

Local and image tests:

- Unit test Alpaca adapter with a tiny JSON fixture.
- Unit test OpenAssistant adapter with a tiny JSONL gzip fixture.
- Run a 10-iteration CPU smoke test for each dataset profile.
- Build the image and confirm `run.c` and `runq.c` compile.
- Confirm the wrapper parses `loss`, `lr`, `dt`, and `mfu`.

Kubernetes tests:

- Run `healthy-tinystories` for at least 50 iterations.
- Run `instruction-alpaca` for at least 50 iterations.
- Confirm metrics reach Splunk with the required attributes.
- Confirm GPU metrics and Kubernetes pod data correlate by time window.
- Run each failure scenario once and capture expected evidence.

Acceptance criteria:

- Instructor can start one training run with a single command or manifest.
- Students can identify healthy training in Splunk.
- Students can diagnose GPU scheduling failure.
- Students can diagnose GPU OOM.
- Students can diagnose missing data cache.
- The workload does not require student AWS, NVIDIA, registry, or cluster-admin
  access.

## Assumptions

- The training workload is instructor-run only.
- Students investigate the workload in Splunk Observability Cloud.
- The training job uses one GPU by default.
- Full model quality is not the goal; observable training behavior is the goal.
- The cluster remains the existing EKS GPU lab unless the infrastructure plan
  changes later.
