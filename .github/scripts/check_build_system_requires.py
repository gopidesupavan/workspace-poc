import toml
import requests
import subprocess


def get_latest_version(package_name):
    """Get the latest version of a package from PyPI"""
    response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
    if response.status_code == 200:
        return response.json()['info']['version']
    return None


def parse_pyproject_toml():
    """Parse the pyproject.toml file and extract build-system.requires"""
    with open('pyproject.toml', 'r') as f:  # Open in read mode ('r')
        pyproject_data = toml.load(f)

    return pyproject_data.get('build-system', {}).get('requires', [])


def check_and_update_versions():
    """Check and update build-system.requires versions if needed"""
    requires = parse_pyproject_toml()

    updated = False
    for i, requirement in enumerate(requires):
        if '>=' in requirement:
            package, version = requirement.split('>=')
            latest_version = get_latest_version(package.strip())

            if latest_version and latest_version != version.strip():
                requires[i] = f"{package.strip()} >= {latest_version}"
                updated = True
                print(f"Updated {package.strip()} to version {latest_version}")

    if updated:
        # First, open pyproject.toml in read mode to load its content
        with open('pyproject.toml', 'r') as f:  # Correctly open in read mode ('r')
            pyproject_data = toml.load(f)

        # Now open pyproject.toml in write mode to update it
        with open('pyproject.toml', 'w') as f:  # Open in write mode ('w') for dumping
            pyproject_data['build-system']['requires'] = requires
            toml.dump(pyproject_data, f)

        # Commit and create a pull request
        subprocess.run(["git", "config", "user.name", "dependabot[bot]"])
        subprocess.run(["git", "config", "user.email", "dependabot@users.noreply.github.com"])
        subprocess.run(["git", "checkout", "-b", "update-build-system-requires"])
        subprocess.run(["git", "commit", "-am", "build-system: Update build-system.requires dependencies"])
        subprocess.run(["git", "push", "origin", "update-build-system-requires"])
        subprocess.run(
            ["gh", "pr", "create", "--title", "build-system: Update build-system.requires dependencies", "--body",
             "Automated update of build-system.requires dependencies."])
    else:
        print("No updates necessary")


if __name__ == "__main__":
    check_and_update_versions()