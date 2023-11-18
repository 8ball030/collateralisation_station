
from pathlib import Path

import git
import yaml
from aea.configurations.data_types import PublicId


def get_repo_root():
    current_dir = Path.cwd()  # Get the current directory
    repo = git.Repo(current_dir, search_parent_directories=True)
    return Path(repo.git.rev_parse("--show-toplevel"))


def get_new_package_ignores():
    packages_path = get_repo_root() / "mas" / "packages" / "packages.json"
    packages = yaml.safe_load(packages_path.read_text(encoding="utf-8"))
    dev_ids = [Path(p).parts[:-1] for p in packages["dev"]]
    for component_type, author, name in dev_ids:
        yield f"{author}/{component_type}s/{name}"


def update_gitignore():
    gitignore_path = get_repo_root() / ".gitignore"
    new_lines = []
    found = False
    for line in gitignore_path.read_text().splitlines():
        if found:
            new_lines.append("!mas/packages/packages.json")
            for item in get_new_package_ignores():
                new_lines.append(f"!mas/packages/{item}")
            found = False
        if line.startswith("mas/packages/*"):
            found = True
        elif line.startswith("!mas/packages/"):
            continue
        new_lines.append(line)
    gitignore_path.write_text("\n".join(new_lines) + "\n")


if __name__ == "__main__":
    update_gitignore()
