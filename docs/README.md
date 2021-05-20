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

Use the script

```bash
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

1. Retrieve all remote tags. This will spot tag conflicts early and prevent accidentally pushing tags deleted on the remote.

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

## How to set up CI/CD with Travis

1. Create a personal access token on [GitHub][GHToken] with the [following scopes: read:org, repo, user:email, write:repo_hook][1]. Use this token to login:

    ```bash
    travis login -u a-staebler --org --github-token TOKEN
    ```

1. Generate a deploy key pair without passphrase:

    ```bash
    ssh-keygen -t rsa -b 4096 -C "astaebler@signalfx.com" -f o11y-workshop-deploy-key
    ```

1. Add the public key `o11y-workshop-deploy-key.pub` as a deploy key with "Allow write access" to the [repository][2].

1. Encrypt the private key:

    ```bash
    travis encrypt-file --no-interactive -f -R signalfx/observability-workshop --org o11y-workshop-deploy-key --add after_success
    ```

    Typical output:

    ```bash
    ❯ travis encrypt-file --no-interactive -f -R signalfx/observability-workshop --org o11y-workshop-deploy-key --add after_success

    encrypting o11y-workshop-deploy-key for signalfx/observability-workshop
    storing result as o11y-workshop-deploy-key.enc
    storing secure env variables for decryption

    Make sure to add o11y-workshop-deploy-key.enc to the git repository.
    Make sure not to add o11y-workshop-deploy-key to the git repository.
    Commit all changes to your .travis.yml.
    ```

1. Move the key pair `o11y-workshop-deploy-key` and `o11y-workshop-deploy-key.pub` out of the repo and keep it in a safe place, e.g. your `~/.ssh` folder.

    ```bash
    mv o11y-workshop-deploy-key o11y-workshop-deploy-key.pub ~/.ssh
    ```

1. Add and commit encrypted private key in `o11y-workshop-deploy-key.enc` to version control:

    ```bash
    git add o11y-workshop-deploy-key.enc && git commit -m "Adding gh-pages deploy key"
    ```

1. Review `travis.yml` and confirm that env.global.secure has encrypted payload and that the openssl command has been added to the after_success stage. Add and commit the changes:

    ```bash
    git add .travis.yml && git commit -m "travis: use gh-pages deploy key"
    ```

1. Review the [travis settings][3] and confirm the environment variables `encrypted.*_iv` and `encrypted.*_key` have been added by the encrypt-file command.

[1]: https://docs.travis-ci.com/user/github-oauth-scopes/#travis-ci-for-private-projects
[2]: https://github.com/signalfx/observability-workshop/settings/keys
[3]: https://travis-ci.org/github/signalfx/observability-workshop/settings
[GHToken]: https://github.com/settings/tokens
