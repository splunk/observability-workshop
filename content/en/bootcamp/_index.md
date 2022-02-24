---
title: Welcome to the Observability Bootcamp
linkTitle: Observability Bootcamp
weight: 1
cascade:
  - _target:
    type: docs
    hide_summary: true
---
We are going to work in the directory `bootcamp/service/src`.
Your first task: Write a python app to count words in a text file.

*No, wait - we've already done that for you*.

This section will introduce the format for this workshop.

1. First, we will introduce a challenge or task for you to complete, e.g. "Task 1: Service".

1. There will be concepts and references for you to review.

1. We will timebox self-paced content during a live workshop.

1. We use `git` branches to provide important milestones after a task is complete. If you did not complete a specific task, you can use these milestones to proceed to the next task or review the solution.

## Getting started

The task is to write a python app to count words in a text file.
Here is how to get to the milestone that completes this step:

=== "Shell Command"

    ```bash
    git checkout 01service
    ```

This will put you on the first milestone.

In case you have already worked on a milestone, you might see an error like:

=== "Example Output"

    ```bash
    error: Your local changes to the following files would be overwritten by checkout:
        app.py
    Please commit your changes or stash them before you switch branches.
    Aborting
    ```

This is because your work conflicts with changes on the milestone. You have the following options:

1. If you have worked on a task and want to progress to the next one *and DROP all your changes*:

    === "Shell Command"

        ```bash
        git reset --hard && git clean -fdx && git checkout service
        ```

    You will have to re-apply any local changes like settings tokens or names.


1. To preserve your work but move it out of the way, you can use

    === "Shell Command"

        ```bash
        git stash && git checkout service
        ```

    To restore your work, switch to the previous milestone (`main` in this case) and retrieve the stashed changes:

    === "Shell Command"

        ```bash
        git checkout main && git stash pop
        ```

    Sometimes you run into conflicting changes with this approach. We recommend you use the first option in this case.

1. During development changes are recorded by adding and commiting to the repository. This is not necessary for this workshop.

Use the first option and proceed.

To compare two milestones, use

=== "Shell Command"

    ```bash
    git diff main..01service
    ```

To compare what you have with a milestone, , e.g. the milestone `service` use

=== "Shell Command"

    ```bash
    git diff ..01service
    ```

=== "Example Output (excerpt)"

    ```bash
    ...
    diff --git a/bootcamp/service/src/app.py b/bootcamp/service/src/app.py
    index 9bcae83..b7fc141 100644
    --- a/bootcamp/service/src/app.py
    +++ b/bootcamp/service/src/app.py
    @@ -1,10 +1,12 @@
    +import json
     import re
    -from unicodedata import category
    +from flask import Flask, request, Response
    ...
    ```

## Future Tasks

TODO YOUR Idea here? Let us know!

TODO metrics method being traced - how to disable?

```
from opentelemetry.context import attach, detach, set_value
token = attach(set_value("suppress_instrumentation", True))
```

TODO autodetect metrics with k8s labels: `prometheus.io/scrape: true` - run prometheus on separate port `9090`.

TODO [tracing examples][py-trace-ex]

[py-trace-ex]: https://github.com/open-telemetry/opentelemetry-python/blob/main/docs/examples/
