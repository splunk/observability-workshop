# Readme

When working on the workshop, we advise that you review your changes locally before committing them. Use the `mkdocs serve` command to live preview your changes (as you type) on your local machine.

## Cloning the repo and installing dependencies

```bash
cd ~
git clone https://github.com/signalfx/observability-workshop.git
cd observability-workshop
```

We recommend that you set up a virtualenv and install dependencies into it:

```bash
python3 -m venv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

## Running the docs server

In most cases, the default settings with `mkdocs serve` work well, and mkdocs is available at <http://localhost:8000>. Otherwise you can use `0.0.0.0` for the IP address so mkdocs listens on all interfaces and define the port you want to listen on e.g. `8123`:

```bash
mkdocs serve -a 0.0.0.0:8123
```

The documentation built from your current branch is then accessible through your favorite browser at <http://localhost:8123>.

## How to create a new tagged release

1. On GitHub, navigate to the main page of the repository.

2. Under your repository name, click Actions.

3. In the left sidebar, click Deploy Workshop.

5. Above the list of workflow runs, select Run workflow dropdown and click Run workflow

Then the release will run through the CI/CD pipeline and be available shortly after.

## How to set up CI/CD with GitHub Actions

TODO @Rob Castley
