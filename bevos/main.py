import click
import json

from bevos import ghapi

@click.group()
def cli() -> None:
    pass

@cli.command()
@click.argument("owner")
@click.argument("repo")
@click.option("--tag", required=True)   # type: ignore # Option descends from Argument, where required is defined
@click.option("--target", default="master")
@click.option("--verbose", "-V", is_flag=True)
def release(owner: str, repo: str, tag: str, target: str, verbose: bool) -> None:
    click.echo("I'm doing a release! to {repo}".format(repo=repo))
    endpoint = ghapi.make_release_endpoint(owner, repo)
    url = ghapi.endpoint_url("https://github.com", endpoint)
    if verbose:
        click.echo("POST {url}".format(url=url))
        click.echo(json.dumps(ghapi.make_release_data(tag, target, "my fancy release", True), indent=4))
