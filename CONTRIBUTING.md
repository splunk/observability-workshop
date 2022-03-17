# Contributing to the Observability Workshop

When working on the workshop, we advise that you review your changes locally before committing them. Use the `hugo server` command to live preview your changes (as you type) on your local machine.

## Install Hugo

```bash
cd ~
brew install hugo
```

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

## Test release build locally

Build a release with

```bash
./.github/ci/build_site
```

The output will be in `./site/vdev`.

To run a webserver that mimics GitHub Pages, install [devd][devd], e.g. with `brew install devd`.

Then run

```bash
devd /observability-workshop/vdev/=./site/vdev /=./site/vdev
```

and visit [http://localhost:8000/](http://localhost:8000/) to inspect the site.

[devd]: https://github.com/cortesi/devd

## How to create a new tagged release

1. On GitHub, navigate to the main page of the repository.

2. Under your repository name, click Actions.

3. In the left sidebar, click Deploy Workshop.

4. Above the list of workflow runs, select Run workflow dropdown and click Run workflow

Then the release will run through the CI/CD pipeline and be available shortly after.
