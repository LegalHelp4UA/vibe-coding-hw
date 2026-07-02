"""Перевіряє, що секрети Telegram-бота не потраплять у коміт.

Запуск: python scripts/security_check.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GITIGNORE = ROOT / ".gitignore"
ENV_EXAMPLE = ROOT / ".env.example"
TOKEN_RE = re.compile(r"\d{6,}:[A-Za-z0-9_-]{30,}")


def configure_output_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def run_git_ls_files() -> tuple[list[str], str | None]:
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        return [], f"Не вдалося виконати `git ls-files`: {exc}"

    return [line.strip() for line in result.stdout.splitlines() if line.strip()], None


def has_env_gitignore_entry() -> bool:
    if not GITIGNORE.exists():
        return False

    for line in GITIGNORE.read_text(encoding="utf-8", errors="ignore").splitlines():
        entry = line.strip()
        if not entry or entry.startswith("#"):
            continue
        if entry in {".env", "/.env"}:
            return True

    return False


def read_tracked_text(relative_path: str) -> str | None:
    path = ROOT / relative_path
    if not path.is_file():
        return None

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return None


def find_token_like_values(files: list[str], excluded: set[str]) -> list[str]:
    findings: list[str] = []

    for relative_path in files:
        normalized = relative_path.replace("\\", "/")
        if normalized in excluded:
            continue

        content = read_tracked_text(relative_path)
        if content is None:
            continue

        for line_number, line in enumerate(content.splitlines(), start=1):
            if TOKEN_RE.search(line):
                findings.append(f"{normalized}:{line_number}")

    return findings


def check_env_example() -> list[str]:
    problems: list[str] = []

    if not ENV_EXAMPLE.exists():
        return [".env.example відсутній"]

    content = ENV_EXAMPLE.read_text(encoding="utf-8", errors="ignore")
    if TOKEN_RE.search(content):
        problems.append(".env.example містить значення, схоже на реальний Telegram bot token")

    bot_token_lines = [
        line
        for line in content.splitlines()
        if line.strip() and not line.lstrip().startswith("#") and line.split("=", 1)[0].strip() == "BOT_TOKEN"
    ]
    if not bot_token_lines:
        problems.append(".env.example не містить плейсхолдер BOT_TOKEN")

    return problems


def main() -> int:
    configure_output_encoding()

    problems: list[str] = []

    print("Перевірка секретів перед комітом")
    print()

    print("1. .env у .gitignore:", "OK" if has_env_gitignore_entry() else "ПРОБЛЕМА")
    if not has_env_gitignore_entry():
        problems.append(".env не додано до .gitignore")

    tracked_files, git_error = run_git_ls_files()
    if git_error:
        problems.append(git_error)
        print("2. git ls-files:", "ПРОБЛЕМА")
    else:
        print("2. git ls-files:", f"OK, перевірено {len(tracked_files)} файлів")

    tracked_env_files = [path for path in tracked_files if path.replace("\\", "/") == ".env"]
    print("3. .env серед відстежуваних файлів:", "ПРОБЛЕМА" if tracked_env_files else "OK")
    if tracked_env_files:
        problems.append(".env відстежується git і може потрапити в коміт")

    token_findings = find_token_like_values(tracked_files, excluded={".env.example"})
    print(
        "4. Реальні Telegram-токени у відстежуваному коді:",
        "ПРОБЛЕМА" if token_findings else "OK",
    )
    for finding in token_findings:
        problems.append(f"Знайдено рядок, схожий на Telegram bot token: {finding}")

    env_example_problems = check_env_example()
    print(
        "5. .env.example містить лише плейсхолдер:",
        "ПРОБЛЕМА" if env_example_problems else "OK",
    )
    problems.extend(env_example_problems)

    print()
    if problems:
        print("Знайдено проблеми:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print("✅ БЕЗПЕЧНО комітити")
    return 0


if __name__ == "__main__":
    sys.exit(main())
