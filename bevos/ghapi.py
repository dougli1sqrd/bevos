import urllib.parse
import requests
import os
import json

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

def token() -> str:
    path = os.getenv("GH_TOKEN_PATH", ".gh_token") # type: str
    with util.open_file(path, "r") as file_result:
        if file_result.file is None:
            return ""
        else:
            return file_result.file.read()

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

def perform_release(owner: str, repo: str, tag: str, target_sha: str, description: str, dryrun: bool) -> GhResult:
    endpoint = make_release_endpoint(owner, repo)
    url = endpoint_url("https://github.com/", endpoint)
    data = make_release_data(tag, target_sha, description, dryrun)
    header = auth_header(token())

    response = requests.post(url, data=json.dumps(data), headers=header)
    return GhResult(response)
