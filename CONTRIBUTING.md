# Contributing to the Observability Workshop

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

## Optimising images

Install `optipng` e.g. `brew install optipng` and then run the following command in the `docs/images` directory:

```bash
find . -type f -iname "*.png" -exec optipng -nb -nc {} \;
```

## How to create a new tagged release

1. On GitHub, navigate to the main page of the repository.

2. Under your repository name, click Actions.

3. In the left sidebar, click Deploy Workshop.

4. Above the list of workflow runs, select Run workflow dropdown and click Run workflow

Then the release will run through the CI/CD pipeline and be available shortly after.

## How to set up CI/CD with GitHub Actions

1. Create a Workflow file called `main.yml` in `.github/workflows`

```yaml
name: Deploy Workshop

# Controls when the action will run. Triggers manually
on: workflow_dispatch

jobs:
  build:
    name: Deploy O11y Workshop
    runs-on: ubuntu-latest
    steps:
      - name: Checkout master
        uses: actions/checkout@v2
        with:
          fetch-depth: 0

      - name: Set up Python 3.7
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Bumpversion and deploy using mike
        run: |
          git config user.name "${GITHUB_ACTOR}"
          git config user.email "${GITHUB_ACTOR}@users.noreply.github.com"
          git pull
          FLAVOUR=minor
          TAG=$(bumpversion --list "$FLAVOUR" | awk -F= '/new_version=/ { print $2 }')
          awk "/Latest versions of the workshop are:/ { print; print \"- [v$TAG](https://signalfx.github.io/observability-workshop/v$TAG/)\";next }1" README.md |
          awk "NR==1,/Latest versions of the workshop are:/{c=3} c&&c-- " > README.new.md
          mv README.new.md README.md
          git fetch --tags origin
          git add README.md
          git commit --amend -m "Releasing v$TAG"
          git tag -a "v$TAG" -m "Version $TAG"
          git push --follow-tags origin master || { echo 'Push failed. git pull --rebase from upstream and attempt another release.'; exit 1; }
          mike deploy --push --update-aliases "v$TAG" latest
          mike set-default --push latest
```
