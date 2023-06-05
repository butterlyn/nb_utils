import yaml
import subprocess
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def read_environment_file(environment_file_path: str) -> dict:
    try:
        with open(environment_file_path, "r") as stream:
            environment = yaml.safe_load(stream)
    except FileNotFoundError:
        logger.error(f"File {environment_file_path} does not exist.")
        return {}
    except yaml.YAMLError as exc:
        logger.error(f"Error reading file {environment_file_path}: {exc}")
        return {}
    return environment


def write_environment_file(environment: dict, input_file_path: str) -> None:
    output_file_path = Path(input_file_path).with_suffix("_conda_converted.yml")
    try:
        with open(output_file_path, "w") as outfile:
            yaml.dump(environment, outfile, default_flow_style=False)
    except IOError:
        logger.error(f"Error writing to file {output_file_path}")


def get_pip_index(dependencies: list[dict]) -> int:
    pip_indices = [
        index for index, dependency in enumerate(dependencies) if "pip" in dependency
    ]
    if not pip_indices:
        logger.error("No pip packages found in environment file.")
        raise ValueError("No pip packages found in environment file.")
    return pip_indices[0]


def search_for_package(package_name: str, version: str) -> bool:
    try:
        result = subprocess.run(
            ["conda", "search", package_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error(f"Error searching for package {package_name} in conda: {e}")
        return False
    return package_name in result.stdout and (version in result.stdout or version == "")


def convert_pip_packages(environment: dict, pip_index: int) -> None:
    pip_packages = environment["dependencies"][pip_index]["pip"]
    for i, package in enumerate(pip_packages):
        package_name, version = (
            package.split("==") if "==" in package else (package, "")
        )
        conda_package = search_for_package(package_name, version)
        if conda_package:
            conda_version = conda_package["version"]
            if conda_version >= version:
                environment["dependencies"].insert(
                    pip_index + i, f"{package_name}={conda_version}"
                )
                pip_packages[i] = None
                logger.info(
                    f"Pip package {package_name} version {version} found in conda with version {conda_version}."
                )

            else:
                logger.info(
                    f"Package {package_name} found in conda, but version {version} not available."
                )
        else:
            logger.info(
                f"Package {package_name} not found in conda, or version {version} not available."
            )
    environment["dependencies"][pip_index]["pip"] = [
        p for p in pip_packages if p is not None
    ]


def convert_environment(input_file_path: str) -> None:
    environment = read_environment_file(input_file_path)
    pip_index = get_pip_index(environment.get("dependencies", []))
    if pip_index is None:
        logger.info("No pip packages found.")
        return
    convert_pip_packages(environment, pip_index)
    write_environment_file(environment, input_file_path)


if __name__ == "__main__":
    input_file_path = "./environment.yml"
    convert_environment(input_file_path)
