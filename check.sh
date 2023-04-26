#!/bin/bash
#
# Copyright 2023 Ant Group Co., Ltd.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
PROTO_CPP_OUT=./proto_cpp/
PROTOC=./protoc.py
ERROR_FILE=error_file

# for exitcode in signal list, perform $your_cmd on exit
trap cleanup 0 2

function cleanup() {
  rm -rf ${ERROR_FILE}
  rm -rf ${PROTO_CPP_OUT}
}


# $1: proto_dir
# $2: proto_cpp_dir
function generate_and_lint_protodir()
{
    proto_dir=$1
    proto_cpp_dir=${2:-${PROTO_CPP_OUT}}
    cleanup
    mkdir -p ${proto_cpp_dir}
    for proto_file in $( ls ${proto_dir}*.proto )
    do
      ${PROTOC} --proto_path=${proto_dir} --cpp_out=${proto_cpp_dir} -I=. ${proto_file} >/dev/null 2>${ERROR_FILE}
      if [ $? -ne 0 ]; then
        echo "here"
        if [ -f "${ERROR_FILE}" ];then
            cat ${ERROR_FILE}
        fi
        exit 1
      fi
    done
}

function main()
{   
    dirs=`find . -type d -not -path '*/\.*'`
    for dir in $dirs
    do 
      if find ${dir} -maxdepth 1 -name "*.proto" | grep -q .; then
        generate_and_lint_protodir "$dir/" $PROTO_CPP_OUT
      fi
    done
}

main
