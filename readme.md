# Bevos

Github release tool.

Using a github api token that has push access to your repository to push. This
uses the requests module to make calls to the github api to make a release
(tag some version and get download links for the source) and upload artifacts
related to the repository.

## Install
    make
    source env/bin/activate

## Run

You can run `bevos --help` to see commands, or in particular `bevos release --help`.
In general to perform a release in organization `foo` and repository `bar`:

    bevos release foo bar --tag v1.2.3 --description "some description" --token-path path/to/file

### Version Bump

Instead of specifying an exact tag version, you can instead provide the option
`--bump=component`, where `component` is one of `major`, `minor`, `patch` as
from [semantic versioning](http://semver.org/). One of `--bump` or `--tag`
must be specified. If `--bump` is supplied bevos will look for the latest
release and bump whichever component specified, according to how semver works.

For example, if the latest version is v1.2.6, and you `--bump=patch` you will
release v1.2.7. Bumping minor would give v1.3.0, and bumping major will give
v2.0.0.

### Dry Run

You can make a "draft" release by specifying the `--dry-run` option. This will
create a "draft" release in Github that can then be deleted if a mistake is made.

### Artifact

Specify the `--artifact path/to/file` option to have bevos upload the file to
Github as a part of the release. This file becomes available for download from
the release website on Github.

### Token Path

In order to access the Github api, it needs an authentication token. You can
generate one in your Github account at your "Personal Access Tokens" page in
your account settings. See also Github's getting started guide on
[authentication](https://developer.github.com/guides/getting-started/#authentication).
Bevos assumes you have a file with some api token. You can specify the path to
this file with `--token-path`, or by setting the environment variable
`GH_TOKEN_PATH`. If neither is set bevos cannot make a release.
