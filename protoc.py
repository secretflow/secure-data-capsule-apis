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

"""This module is used to generete protobuf python including pyi for better hint."""

import glob
from os import path

import grpc_tools
from grpc_tools import protoc


def compile_proto(in_path, out_path, pb_files) -> None:
    """Compile protos in the proto directory into the respective directories."""
    # Path to google .proto files
    grpc_path = grpc_tools.__path__[0]
    command = [
        "grpc_tools.protoc",
        f"--proto_path={grpc_path}/_proto",
        f"--proto_path={in_path}",
        # Output path
        f"--python_out={out_path}",
        f"--grpc_python_out={out_path}",
        f"--mypy_out={out_path}",
    ] + pb_files

    exit_code = protoc.main(command)

    if exit_code != 0:
        raise Exception(f"Error: {command} failed with error code {exit_code}")


if __name__ == "__main__":
    root_dir = path.dirname(path.realpath(__file__))
    in_path = path.normpath(f"{root_dir}")
    out_path = path.normpath(f"{root_dir}/python")
    pb_files = glob.glob(f"{root_dir}/secretflowapis/**/*.proto", recursive=True)
    print(pb_files)

    compile_proto(in_path=in_path, out_path=out_path, pb_files=pb_files)
