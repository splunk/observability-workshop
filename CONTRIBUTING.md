# Contributing Guidelines

Thank you for your interest in contributing to our repository! Whether it's a bug report, new feature, or question, we greatly value feedback and contributions from our community. Read through this document before submitting any issues or pull requests to ensure we have all the necessary information to effectively respond to your bug report or contribution.

In addition to this document, review our [Code of Conduct](CODE_OF_CONDUCT.md). For any code of conduct questions or comments, send an email to [oss@splunk.com](oss@splunk.com).

## Contributor License Agreement

Before contributing, you must sign the [Splunk Contributor License Agreement (CLA)](https://www.splunk.com/en_us/form/contributions.html).

## Contributing to the Observability Workshop

When working on the workshop, we advise that you review your changes locally before committing them, although we prefer Pull Requests. Use the `hugo server` command to live preview your changes (as you type) on your local machine.

## Install Go & Hugo

``` bash
cd ~
```

``` bash
brew install go
```

``` bash
brew install hugo
```

## Install yq

You will also need to install `yq` if it is not already installed on your system.

``` bash
brew install yq
```

## Cloning the repository

``` bash
git clone https://github.com/splunk/observability-workshop.git
```

``` bash
cd observability-workshop
```

``` bash
hugo server
```

## Running the docs server

In most cases, the default settings with `hugo server` work well, and Hugo is available at `http://localhost:1313`. If you need to change the port, you can do so by passing the `--port` flag e.g. `hugo server --port=1314`. The documentation built from your current branch is then accessible through your favorite browser at e.g. `http://localhost:1314`.

## Create Content

The workshop uses the Hugo Relearn Theme. Documentation on how to use the theme can be found [here](https://mcshelby.github.io/hugo-theme-relearn/cont/index.html).

Additional documentation for the shortcodes used in the theme can be found [here](https://mcshelby.github.io/hugo-theme-relearn/shortcodes/index.html).

## Optimising images

Install `optipng`:

``` bash
brew install optipng
```

and then run the following command in the `content` directory:

``` bash
find . -type f -iname "*.png" -exec optipng -nb -nc {} \;
```

## Test release build locally

Build a local version with:

``` bash
hugo server --buildDrafts --buildFuture
```

This will start a local development server at [http://localhost:1313](http://localhost:1313).

To test a production build locally:

``` bash
hugo --minify --destination "public" --baseURL "http://localhost:8000/observability-workshop"
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

6. Click **Run workflow**.

The release will run through the CI/CD pipeline and be deployed to `https://splunk.github.io/observability-workshop/` shortly after.

