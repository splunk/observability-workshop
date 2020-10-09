# Readme

When working on the workshop, we advise that you review your changes locally before committing them. Use the `mkdocs serve` command to live preview your changes (as you type) on your local machine.

## Cloning the repo and installing dependencies

```bash
git clone https://github.com/signalfx/observability-workshop.git
cd ~/observability-workshop
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

The documentation built from your current branch is then accessible through your favorite browser at <http://0.0.0.0:8123>.

## How to create a new tagged release

Use the script

```
./ci/prepare-release.sh
```

It takes a single optional argument, the type of release. It defaults to a minor release. To issue a major release:

```bash
./.ci/prepare-release.sh major
```

This will automatically perform the following changes (DO NOT MANUALLY PERFORM THESE STEPS):

1. Determine the new version by bumping the major or minor version.

1. Use `bumpversion --list minor` (by default, or `bumpversion --list major` if requested, see above) to update the version number in various places and commit the changes.

1. Update [README.md](../README.md) and prepend the version to the list of available versions. The list has the two latest versions.

1. Retrieve all remote tags. This will spot tag conflicts early and prevent accidentially pushing tags deleted on the remote.

1. Amend the commit created by `bumpversion` with these change and a message like "`Releasing v4.2`":

    ```bash
    git add README.md && git commit -amend -m 'Releasing v4.2'
    ```

1. Tag the release:

    ```bash
    git tag -a v4.2 -m "Version 4.2"
    ```

1. Push the branch and the tag

    ```bash
    git push --follow-tags origin master
    ```

Then the release will run through the Travis CI/CD pipeline and be available shortly after.
