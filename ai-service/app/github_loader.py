import requests
from pathlib import PurePosixPath
import base64
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}


def get_repository_tree(repo_url: str):
    # Remove trailing ".git" and "/"
    repo_url = repo_url.rstrip("/")
    if repo_url.endswith(".git"):
        repo_url = repo_url[:-4]

    # Extract owner and repository name
    parts = repo_url.split("/")

    owner = parts[-2]
    repo = parts[-1]

    # Get repository information
    repo_info_url = f"https://api.github.com/repos/{owner}/{repo}"

    response = requests.get(repo_info_url, headers=HEADERS)
    response.raise_for_status()

    repo_info = response.json()

    default_branch = repo_info["default_branch"]

    # GitHub API endpoint
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"

    response = requests.get(url, headers=HEADERS)

    # Raise an exception if GitHub returned an error
    response.raise_for_status()

    data = response.json()

    return data["tree"]



IGNORED_DIRECTORIES = {
    ".git",
    "node_modules",
    "dist",
    "build",
    "target",
    "venv",
    "__pycache__",
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".java",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".html",
    ".css",
    ".json",
    ".yaml",
    ".yml",
    ".xml",
    ".md",
}

IGNORED_FILES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "bun.lock",
    "bun.lockb",
    "composer.lock",
    "poetry.lock",
    "Cargo.lock",
}

IGNORED_SUFFIXES = {
    ".min.js",
    ".min.css",
    ".map",
}

MAX_FILE_SIZE = 500_000  # 500 KB

def is_relevant_file(path: str) -> bool:
    path_obj = PurePosixPath(path)

    # Ignore unwanted directories
    if any(
        part.lower() in IGNORED_DIRECTORIES
        for part in path_obj.parts
    ):
        return False

    filename = path_obj.name.lower()

    # Ignore specific files
    if filename in IGNORED_FILES:
        return False

    # Ignore minified and generated files
    if any(filename.endswith(suffix) for suffix in IGNORED_SUFFIXES):
        return False

    # Check allowed extensions
    return path_obj.suffix.lower() in ALLOWED_EXTENSIONS

def get_file_content(owner: str, repo: str, path: str) -> str:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    data = response.json()

    content = data["content"]

    return base64.b64decode(content).decode("utf-8")

def get_repository_files(repo_url: str):
    tree = get_repository_tree(repo_url)

    files = [
        item["path"]
        for item in tree
        if item["type"] == "blob"
        and is_relevant_file(item["path"])
        and item.get("size", 0) <= MAX_FILE_SIZE
    ]

    repo_url = repo_url.rstrip("/")

    if repo_url.endswith(".git"):
        repo_url = repo_url[:-4]

    parts = repo_url.split("/")

    owner = parts[-2]
    repo = parts[-1]

    repository_files = []

    for path in files:
        content = get_file_content(owner, repo, path)

        repository_files.append({
            "path": path,
            "content": content,
        })

    return repository_files