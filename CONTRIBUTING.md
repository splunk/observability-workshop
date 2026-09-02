# Contributing Guidelines

Thank you for your interest in contributing to this repository. Whether it is a bug report, new feature, or question, we value feedback and contributions from the community. Read this document before submitting an issue or pull request so that we have the information needed to review it.

In addition to this document, review our [Code of Conduct](CODE_OF_CONDUCT.md). For code of conduct questions or comments, email [oss@splunk.com](mailto:oss@splunk.com).

## Contributor License Agreement

Before contributing, you must sign the [Splunk Contributor License Agreement (CLA)](https://www.splunk.com/en_us/form/contributions.html).

## Contributing to the Observability Workshop

Review your changes locally and submit them from a branch using a pull request. Use `hugo server` to preview content changes as you work.

## Install the development tools

The site requires Go because the theme is provided as a Hugo module. It also requires Hugo Extended 0.161.1 or later, as configured in `hugo.toml`. On macOS, install both tools with Homebrew:

``` bash
brew install go hugo
```

For other operating systems, follow the official [Go installation](https://go.dev/doc/install) and [Hugo installation](https://gohugo.io/installation/) instructions and select the extended edition of Hugo.

The release workflow installs `yq` itself, so it is not required for local authoring or builds.

## Cloning the repository

``` bash
git clone https://github.com/splunk/observability-workshop.git
cd observability-workshop
go mod download
hugo server
```

## Running the docs server

In most cases, the default settings work well and Hugo is available at `http://localhost:1313`. To use another port, run `hugo server --port 1314`. Draft and future-dated content can be included with `hugo server --buildDrafts --buildFuture`.

## Create Content

The workshop uses the [hugo-theme-splunk-workshop](https://splunk.github.io/hugo-theme-splunk-workshop/) theme. See the [authoring docs](https://splunk.github.io/hugo-theme-splunk-workshop/docs/authoring/) for content conventions.

For the shortcodes used in the theme, see the [shortcodes reference](https://splunk.github.io/hugo-theme-splunk-workshop/docs/shortcodes/).

## Optimising images

Install `optipng`:

``` bash
brew install optipng
```

Then run the following command in the `content` directory. It runs one optimization process per CPU core on macOS:

``` bash
find . -type f -iname "*.png" -print0 | xargs -0 -P "$(sysctl -n hw.ncpu)" -n 1 optipng -nb -nc
```

On Linux, replace `$(sysctl -n hw.ncpu)` with `$(nproc)`.

## Test release build locally

Build a local version with:

``` bash
hugo server --buildDrafts --buildFuture
```

This will start a local development server at [http://localhost:1313](http://localhost:1313).

To test a production build locally:

``` bash
hugo --minify --destination "public" --baseURL "http://localhost:8000/observability-workshop" --noChmod
```

Then serve it with [devd][devd] (install with `brew install devd`):

``` bash
devd /observability-workshop/=./public /=./public
```

and visit [http://localhost:8000/](http://localhost:8000/) to inspect the site.

[devd]: https://github.com/cortesi/devd

## How to create a new tagged release

1. On GitHub, navigate to the main page of the repository.

2. Under your repository name, click **Actions**.

3. In the left sidebar, click **Deploy Workshop to GitHub Pages**.

4. Above the list of workflow runs, select **Run workflow** dropdown.

5. Choose the release type:

   - **minor** - for incremental updates (e.g., 6.13 → 6.14)
   - **major** - for breaking changes (e.g., 6.14 → 7.0)

6. Enter a meaningful, mandatory release reason. It is recorded in the workflow summary, release commit, tag, and GitHub release.

7. Click **Run workflow**.

The release will run through the CI/CD pipeline and be deployed to `https://splunk.github.io/observability-workshop/` shortly after.
