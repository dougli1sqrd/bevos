import urllib.parse
import requests
import os

from typing import Dict, Union, List, Optional

from bevos import util

JsonVal = Union[bool, str, float, List, Dict]
Json = Dict[str, JsonVal]

def token() -> Optional[str]:
    path = os.getenv("GH_TOKEN_PATH", ".gh_token") # type: str
    with util.open_file(path, "r") as file_result:
        if file_result.file is None:
            print(file_result.error_message)
            return None
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

def make_release_endpoint(owner: str, repo: str) -> str:
    return "/repos/{owner}/{repo}/releases".format(owner=owner, repo=repo)

def endpoint_url(github_url: str, release_endpoint: str) -> str:
    return urllib.parse.urljoin(github_url, release_endpoint)
