"""Crea o inspecciona el repositorio remoto usando Git Credential Manager.

La credencial solo se mantiene en memoria y nunca se muestra ni se guarda aquí.
"""

import argparse
import json
import subprocess
import sys
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def credential():
    result = subprocess.run(
        ["git", "credential", "fill"],
        input="protocol=https\nhost=github.com\n\n",
        text=True,
        capture_output=True,
        check=True,
    )
    values = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    if not values.get("password"):
        raise RuntimeError("No hay credencial de GitHub disponible.")
    return values["password"]


def api(method, path, token, data=None):
    body = json.dumps(data).encode() if data is not None else None
    request = Request(
        "https://api.github.com" + path,
        data=body,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "lumiere-preview-setup",
            **({"Content-Type": "application/json"} if body else {}),
        },
    )
    try:
        with urlopen(request, timeout=25) as response:
            return response.status, json.load(response)
    except HTTPError as error:
        try:
            details = json.load(error)
        except (ValueError, OSError):
            details = {}
        return error.code, details


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["check", "create", "enable-pages", "pages-status"])
    parser.add_argument("--name", default="lumiere-belleza-preview")
    args = parser.parse_args()
    token = credential()
    status, account = api("GET", "/user", token)
    if status != 200:
        raise RuntimeError(f"No se pudo consultar GitHub (HTTP {status}).")
    login = account["login"]
    print(f"Cuenta: {login}")
    repo_path = f"/repos/{login}/{args.name}"
    if args.action == "check":
        status, repo = api("GET", repo_path, token)
        print(f"Repositorio: {'existente' if status == 200 else 'no encontrado'} (HTTP {status})")
        if status == 200:
            print(repo["html_url"])
        return
    if args.action == "create":
        status, repo = api("GET", repo_path, token)
        if status == 200:
            print("El repositorio ya existe: " + repo["html_url"])
            return
        status, repo = api("POST", "/user/repos", token, {
            "name": args.name,
            "description": "Vista previa responsive de Lumière basada en referencia visual",
            "private": False,
            "auto_init": False,
        })
        if status != 201:
            raise RuntimeError(f"No se pudo crear el repositorio (HTTP {status}): {repo.get('message', '')}")
        print("Creado: " + repo["html_url"])
        return
    if args.action == "enable-pages":
        status, pages = api("POST", repo_path + "/pages", token, {"build_type": "workflow"})
        if status not in (201, 409):
            raise RuntimeError(f"No se pudo activar Pages (HTTP {status}): {pages.get('message', '')}")
        print(f"Pages: HTTP {status}")
        if pages.get("html_url"):
            print(pages["html_url"])
        return
    status, pages = api("GET", repo_path + "/pages", token)
    print(f"Pages: HTTP {status}")
    if status == 200:
        print("URL: " + pages.get("html_url", ""))
        print("Estado: " + pages.get("status", ""))


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.CalledProcessError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
