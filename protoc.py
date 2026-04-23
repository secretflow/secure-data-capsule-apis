#! /usr/bin/env python3

# Copyright 2023 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""This module is used to generate protobuf python using betterproto."""

import glob
from os import path
from pathlib import Path

import grpc_tools
from grpc_tools import protoc


def compile_proto(in_path, out_path, pb_files) -> None:
    """Compile protos using betterproto plugin."""
    grpc_path = grpc_tools.__path__[0]
    command = [
        "grpc_tools.protoc",
        f"--proto_path={grpc_path}/_proto",
        f"--proto_path={in_path}",
        f"--python_betterproto_out={out_path}",
    ] + pb_files

    exit_code = protoc.main(command)
    if exit_code != 0:
        raise Exception(f"Error: {command} failed with error code {exit_code}")


def generate_shims(out_path, in_path, proto_files) -> None:
    """Generate compatibility shim files for legacy import paths.

    betterproto merges messages of the same package into __init__.py.
    This function generates *_pb2.py / *_pb2_grpc.py shims for each
    legacy path, so that downstream code using old import paths still works.
    """
    in_path = Path(in_path)
    for proto_file in proto_files:
        proto_path = Path(proto_file)
        # Convert to a path relative to in_path to ensure correct package_import
        rel_path = proto_path.relative_to(in_path)
        stem = rel_path.stem
        parent = Path(out_path) / rel_path.parent
        # Derive the Python import path for the proto package
        # e.g., secretflowapis/v2/sdc/capsule_manager -> secretflowapis.v2.sdc.capsule_manager
        package_import = ".".join(rel_path.parent.parts)

        if not parent.exists():
            continue

        # _pb2.py shim
        (parent / f"{stem}_pb2.py").write_text(
            f'"""Compatibility shim."""\n'
            f'from {package_import} import *  # noqa: F401,F403\n'
        )
        # _pb2_grpc.py shim
        (parent / f"{stem}_pb2_grpc.py").write_text(
            f'"""Compatibility shim."""\n'
            f'from {package_import} import *  # noqa: F401,F403\n'
        )


if __name__ == "__main__":
    root_dir = path.dirname(path.realpath(__file__))
    in_path = path.normpath(f"{root_dir}")
    out_path = path.normpath(f"{root_dir}/python")
    pb_files = glob.glob(f"{root_dir}/secretflowapis/**/*.proto", recursive=True)
    print(pb_files)

    compile_proto(in_path=in_path, out_path=out_path, pb_files=pb_files)
    generate_shims(out_path=out_path, in_path=in_path, proto_files=pb_files)