import os
import shutil
import subprocess
import tempfile
from bdb import BdbQuit
from pathlib import Path

import click

from gbd_mapping_generator import (
    base_template_builder,
    cause_builder,
    covariate_builder,
    etiology_builder,
    id_builder,
    risk_builder,
    sequela_builder,
)

AUTO_MAPPINGS = {
    "id": id_builder,
    "base_template": base_template_builder,
    "cause": cause_builder,
    "sequela": sequela_builder,
    "etiology": etiology_builder,
    "risk_factor": risk_builder,
    "covariate": covariate_builder,
}

ROOT = Path(__file__).resolve().parent.parent.joinpath("gbd_mapping")  # type: Path


def format_python_file(file_path: Path):
    """Format a Python file with isort and black."""
    try:
        # Run isort first
        subprocess.run(["isort", str(file_path)], check=True, capture_output=True)
        # Then run black
        subprocess.run(["black", str(file_path)], check=True, capture_output=True)
        print(f"Formatted {file_path.name} with isort and black")
    except subprocess.CalledProcessError as e:
        print(f"Warning: Failed to format {file_path.name}: {e}")
    except FileNotFoundError:
        print(f"Warning: isort or black not found. Skipping formatting for {file_path.name}")


@click.command()
@click.argument("mapping_type", default="id")
@click.option("--pdb", "with_debugger", is_flag=True)
def build_mapping(mapping_type, with_debugger):
    if mapping_type not in AUTO_MAPPINGS:
        raise ValueError(
            f"Unknown mapping type {mapping_type}. "
            f"Mapping type must be one of {list(AUTO_MAPPINGS.keys())}"
        )

    try:
        make_dirs_and_init(mapping_type)

        builder = AUTO_MAPPINGS[mapping_type]
        generated_files = []

        if hasattr(builder, "build_mapping_template"):
            template_file = ROOT.joinpath(f"{mapping_type}_template.py")
            with template_file.open("w") as f:
                f.write(builder.build_mapping_template())
            generated_files.append(template_file)

        mapping_file = ROOT.joinpath(f"{mapping_type}.py")
        with mapping_file.open("w") as f:
            f.write(builder.build_mapping())
        generated_files.append(mapping_file)

        # Format all generated files with isort and black
        for file_path in generated_files:
            format_python_file(file_path)

    except (BdbQuit, KeyboardInterrupt):
        raise
    except Exception as e:
        if with_debugger:
            import pdb
            import traceback

            traceback.print_exc()
            pdb.post_mortem()
        else:
            raise


def make_dirs_and_init(mapping_type):
    ROOT.mkdir(exist_ok=True)
    init_path = ROOT.joinpath("__init__.py")

    init_stanza = f"from .{mapping_type} import {', '.join(AUTO_MAPPINGS[mapping_type].IMPORTABLES_DEFINED)}\n"

    if not init_path.exists():  # Create a new init file
        with init_path.open("w") as init_file:
            init_file.write(init_stanza)
    else:  # Replace the init_stanza if it exists, otherwise append it to the end of the file.
        replaced = False

        temp_file, temp_path = tempfile.mkstemp()
        with open(temp_file, "w") as new_init_file:
            with open(init_path) as old_init_file:
                for line in old_init_file:
                    if f"from .{mapping_type} import " in line:
                        new_init_file.write(init_stanza)
                        replaced = True
                    else:
                        new_init_file.write(line)

                if not replaced:
                    new_init_file.write(init_stanza)

        os.remove(str(init_path))
        shutil.move(temp_path, str(init_path))
