import click
import json
import sys
import os

from typing import Optional

from bevos import ghapi
from bevos import util

@click.group()
def cli() -> None:
    pass

@cli.command()
@click.argument("owner")
@click.argument("repo")
@click.option("--tag", required=True)   # type: ignore # Option descends from Argument, where required is defined
@click.option("--target", default="master")
@click.option("--verbose", "-V", is_flag=True)
@click.option("--dry-run", is_flag=True)
@click.option("--description", default="")
@click.option("--token-path", envvar="GH_TOKEN_PATH", type=click.Path(exists=True))
@click.option("--artifact", type=click.Path(exists=True))
def release(owner: str, repo: str, tag: str, target: str, verbose: bool, dry_run: bool, description: str, token_path: Optional[str], artifact: Optional[str]) -> None:

    util._messenger.setVerbosity(verbose)

    if token_path is None:
        raise click.UsageError("No path to a github api token defined. Specify GH_TOKEN_PATH or use --token-path.")

    click.echo("I'm doing a release! to {repo}".format(repo=repo))
    endpoint = ghapi.make_release_endpoint(owner, repo)
    url = ghapi.endpoint_url("https://api.github.com", endpoint)
    result = ghapi.perform_release(owner, repo, tag, target, artifact, token_path, description, dry_run)
    click.echo(result.message())
    if not result.success:
        sys.exit(1)

@cli.command()
@click.argument("url")
@click.argument("artifact-path")
@click.option("--token-path", envvar="GH_TOKEN_PATH", type=click.Path(exists=True))
@click.option("--verbose", "-V", is_flag=True)
def upload(url: str, artifact_path: str, token_path: Optional[str], verbose: bool) -> None:

    util._messenger.setVerbosity(verbose)

    if token_path is None:
        raise click.UsageError("No path to a github api token defined. Specify GH_TOKEN_PATH or use --token-path.")

    click.echo("uploading artifact to {}".format(url))

    full_url = "{url}?name={filename}".format(url=url, filename=os.path.basename(artifact_path))
    result = ghapi.upload_artifact(full_url, artifact_path, token_path)
    click.echo(result.message())
    if not result.success:
        sys.exit(1)
