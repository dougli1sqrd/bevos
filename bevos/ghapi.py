import urllib.parse
import requests
import os
import json
import click

from typing import Dict, Union, List, Optional

from bevos import util

JsonVal = Union[bool, str, float, List, Dict]
Json = Dict[str, JsonVal]
Header = Dict[str, str]

class GhResult(object):

    def __init__(self, response: requests.Response) -> None:
        self.success = response.status_code < 300

    def message(self) -> str:
        if self.success:
            return "Release successful"
        else:
            return "Failed to release"

def token(path: str) -> str:
    path = os.getenv("GH_TOKEN_PATH", path) # type: ignore
    with util.open_file(path, "r") as file_result:
        if file_result.contents is None:
            return ""
        else:
            return file_result.contents.rstrip()

def make_release_data(version_name: str, target_sha: str, description: str, dryrun: bool) -> Json:
    data = {
      "tag_name": version_name,
      "target_commitish": target_sha,
      "name": version_name,
      "body": description,
      "draft": dryrun,
      "prerelease": False
    } # type: Dict[str, JsonVal]
    return data

def auth_header(token: str) -> Header:
    return {"Authorization": "token {tok}".format(tok=token)}

def make_release_endpoint(owner: str, repo: str) -> str:
    return "/repos/{owner}/{repo}/releases".format(owner=owner, repo=repo)

def endpoint_url(github_url: str, endpoint: str) -> str:
    return urllib.parse.urljoin(github_url, endpoint)

def artifact_upload_url(release_response: requests.Response, artifact_path: str) -> str:
    response = release_response.json()
    url_template = response["assets_url"]
    return "{url}?name={filename}".format(url=url_template, filename=os.path.basename(artifact_path))

def perform_release(owner: str, repo: str, tag: str, target_sha: str, artifact_path: Optional[str], token_path:str, description: str, dryrun: bool) -> GhResult:
    endpoint = make_release_endpoint(owner, repo)
    url = endpoint_url("https://api.github.com/", endpoint)
    util.message("POST {}".format(url))
    data = make_release_data(tag, target_sha, description, dryrun)
    util.message(json.dumps(data, indent=4))
    header = auth_header(token(token_path))

    response = requests.post(url, data=json.dumps(data), headers=header)
    util.message(response.text)

    if artifact_path and response.status_code < 300:
        artifact_url = artifact_upload_url(response, artifact_path)
        result = upload_artifact(artifact_url, artifact_path, token_path)
        if not result.success:
            raise click.ClickException("Could not upload {}".format(artifact_path))

    return GhResult(response)

def upload_artifact(url: str, path: str, token_path: str) -> GhResult:
    click.echo("Uploading artifact...")
    headers = auth_header(token(token_path))
    headers["Content-Type"] = "application/octet-stream"

    try:
        with open(path) as artifact:
            response = requests.post(url, headers=headers)

    except OSError as e:
        raise click.ClickException(e.strerror)

    util.message(response.text)

    return GhResult(response)
