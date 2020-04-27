# Readme

When working on the workshop, it is advised that you review your changes locally before committing them. The `mkdocs serve` command can be used to live preview your changes (as you type) on your local machine.

## Cloning the repo and installing dependencies

```bash
git clone https://github.com/signalfx/app-dev-workshop.git
cd ~/app-dev-workshop
```

We recommend that you set up a virtualenv and install dependencies into it:

```bash
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Running the docs server

In most cases, the default settings with `mkdocs serve` work well, and mkdocs is available at <http://127.0.0.1:8000/>. Otherwise you can use `0.0.0.0` for the IP address so mkdocs listens on all interfaces and define the port you want to listen on e.g. `8123`:

```bash
mkdocs serve -a 0.0.0.0:8123
```

After these commands, the current branch is accessible through your favorite browser at <http://localhost:8123>

## How to create a new tagged release

Use the script `./ci/prepare-release.sh`. It takes a single optional argument, the type of release. It defaults to a minor release. To perform a major release:

```bash
./.ci/prepare-release.sh major
```

This will perform the following changes (DO NOT MANUALLY PERFORM THESE STEPS):

1. Determine the new version by bumping the major or minor version.

1. Update the `version` list in `mkdocs.yml` with the name of the release tag, e.g. `v4.2`.

1. Update [README.md](../README.md) and prepend the version to the list of available versions.

1. Catch up with any remote tags not present locally. This will prevent accidentially pushing tags deleted on the remote.

1. Commit these change with a message like `Releasing v4.2`:

    ```bash
    git add mkdocs.yml README.md && git commit -m 'Releasing v4.2'
    ```

1. Tag the release:

    ```bash
    git tag -a v4.2 -m "Version 4.2"
    ```

1. Push the branch and the tag

    ```bash
    git push --follow-tags origin master
    ```

