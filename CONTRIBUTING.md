# Contributing to the Observability Workshop

When working on the workshop, we advise that you review your changes locally before committing them. Use the `hugo server` command to live preview your changes (as you type) on your local machine.

## Cloning the repo and installing dependencies

```bash
cd ~
git clone https://github.com/signalfx/observability-workshop.git
cd observability-workshop
git submodule update --init --recursive
```

## Running the docs server

In most cases, the default settings with `hugo server` work well, and Hugo is available at <http://localhost:1313>. If you need to change the port, you can do so by passing the `--port` flag e.g. `hugo server --port=1314`.

The documentation built from your current branch is then accessible through your favorite browser at <http://localhost:1314>.

## Optimising images

Install `optipng` e.g. `brew install optipng` and then run the following command in the `static/images` directory:

```bash
find . -type f -iname "*.png" -exec optipng -nb -nc {} \;
```

## How to create a new tagged release

1. On GitHub, navigate to the main page of the repository.

2. Under your repository name, click Actions.

3. In the left sidebar, click Deploy Workshop.

4. Above the list of workflow runs, select Run workflow dropdown and click Run workflow

Then the release will run through the CI/CD pipeline and be available shortly after.
