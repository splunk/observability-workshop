# Contributing Guidelines

Thank you for your interest in contributing to this repository. Whether it is a bug report, new feature, or question, we value feedback and contributions from the community. Read this document before submitting an issue or pull request so that we have the information needed to review it.

In addition to this document, review our [Code of Conduct](CODE_OF_CONDUCT.md). For code of conduct questions or comments, email [oss@splunk.com](mailto:oss@splunk.com).

## Contributor License Agreement

Before contributing, you must sign the [Splunk Contributor License Agreement (CLA)](https://www.splunk.com/en_us/form/contributions.html).

## Contributing to the Observability Workshop

Review your changes locally and submit them from a branch using a pull request. Use `hugo server` to preview content changes as you work.

## Reporting a problem with a page

Every workshop page has a **Report an issue** link. It opens a GitHub issue using the [page issue template](https://github.com/splunk/observability-workshop/issues/new?template=page-issue.yml), with the page title and link already filled in. Describe what is wrong, what you expected, and add steps or screenshots if they help.

## Install the development tools

The site requires Go because the theme is provided as a Hugo module. It also requires Hugo Extended 0.161.1 or later, as configured in `hugo.toml`. On macOS, install both tools with Homebrew:

``` bash
brew install go hugo
```

For other operating systems, follow the official [Go installation](https://go.dev/doc/install) and [Hugo installation](https://gohugo.io/installation/) instructions and select the extended edition of Hugo.

The release workflow installs `yq` itself, so it is not required for local authoring or builds.

To work with screenshots, also install the WebP tools (see [Images](#images)):

``` bash
brew install webp
```

## Cloning the repository

``` bash
git clone https://github.com/splunk/observability-workshop.git
cd observability-workshop
go mod download
```

## Previewing your changes

Start the local server with:

``` bash
hugo server --renderToMemory
```

The site is available at [http://localhost:1313](http://localhost:1313) and reloads as you save. Useful options:

| Option | Effect |
| --- | --- |
| `--renderToMemory` | Serves pages from memory instead of writing the whole site (over 500 MB, mostly screenshots) to `public/`. Together with the development config below, this roughly halves start-up time. |
| `--buildDrafts` (`-D`) | Includes pages with `draft: true`. |
| `--buildFuture` | Includes pages with a future `date`. |
| `--port 1314` | Uses another port. |

`hugo server` also reads `config/development/hugo.toml`, which turns off Git info locally. Looking up the Git history of every page is only needed for the "last updated" dates on the published site, so production builds are unaffected.

## Create Content

The workshop uses the [hugo-theme-splunk-workshop](https://splunk.github.io/hugo-theme-splunk-workshop/) theme. See the [authoring docs](https://splunk.github.io/hugo-theme-splunk-workshop/docs/authoring/) for content conventions.

For the shortcodes used in the theme, see the [shortcodes reference](https://splunk.github.io/hugo-theme-splunk-workshop/docs/shortcodes/).

For knowledge checks with a single correct answer, use the [quiz shortcode](https://splunk.github.io/hugo-theme-splunk-workshop/docs/shortcodes/02-structure/#quiz) rather than Questions/Answers tabs. Readers get immediate feedback, and the answer stays hidden until they choose. Open-ended discussion questions can stay as plain text.

## Images

Screenshots are stored as **WebP**, which is much smaller than PNG. Capture or export a PNG, then convert it with one of the scripts in [`scripts/`](scripts/README.md). Both scripts need `cwebp` from the WebP tools, convert PNG to WebP, update the Markdown links to match, and list images that no page uses.

| Task | Script |
| --- | --- |
| Capture, retake or review a module's screenshots one by one | `python3 scripts/retake-screenshots.py`. See the [screenshot helper guide](scripts/screenshots/README.md). |
| Convert every PNG in a module from the same menu | `python3 scripts/retake-screenshots.py -w` |
| Batch convert PNGs in any folder | `python3 scripts/png-to-webp.py`. See the [PNG to WebP guide](scripts/README.md#png-to-webp). |

Preview a batch conversion before writing any files:

``` bash
python3 scripts/png-to-webp.py --dry-run content/en/splunk4rookies/observability-cloud-2027
```

Then run it again without `--dry-run`. Converted PNGs are deleted unless you pass `--keep`.

## Test a production build locally

`hugo server` is enough for most changes. To check the minified site the release workflow publishes, build it and serve the output:

``` bash
hugo --minify --destination "public" --baseURL "http://localhost:8000/" --noChmod
python3 -m http.server 8000 --directory public
```

Visit [http://localhost:8000/](http://localhost:8000/) to inspect the site, and press `Ctrl+C` to stop the server.

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
