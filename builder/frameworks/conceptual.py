# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#
# Builder for application using Conceptual Framework
#

import os

from SCons.Script import DefaultEnvironment

print("foo")

env = DefaultEnvironment()
platform = env.PioPlatform()
board = env.BoardConfig()
build_mcu = env.get("BOARD_MCU", board.get("build.mcu", ""))

FRAMEWORK_DIR = platform.get_package_dir("framework-conceptual")
CMSIS_DIR = platform.get_package_dir("framework-cmsis")

env.Append(
    ASFLAGS=[
        # "-flto",
        "-mthumb",
        "-mcpu=%s" % board.get("build.cpu"),
    ],
    ASPPFLAGS=[
        "-x", "assembler-with-cpp",
    ],

    CFLAGS=[
        "-std=gnu11",
    ],

    CCFLAGS=[
        "-Os",  # optimize for size
        "-flto",
        "-ffunction-sections",  # place each function in its own section
        "-fdata-sections",
        "-mthumb",
        "-mcpu=%s" % board.get("build.cpu"),
        "-Wall",
        "--param", "max-inline-insns-single=500",
    ],

    CXXFLAGS=[
        "-fno-rtti",
        "-fno-exceptions",
        "-std=gnu++23",
        "-fno-threadsafe-statics",
        "-Wno-register"
    ],

    CPPDEFINES=[
        ("F_CPU", "$BOARD_F_CPU")
    ],

    CPPPATH=[
        os.path.join(CMSIS_DIR, "CMSIS", "Include"),
        os.path.join(FRAMEWORK_DIR, "include"),
    ],

    LINKFLAGS=[
        "-Os",
        "-flto",
        "-mthumb",
        "-mcpu=%s" % board.get("build.cpu"),
        "-Wl,--gc-sections",
        "-Wl,--check-sections",
        "-Wl,--unresolved-symbols=report-all",
        "-Wl,--warn-common",
        "-Wl,--warn-section-align",
        # "--specs=nosys.specs",
        # "--specs=nano.specs"
    ],

    LIBS=["m"],
)

libs = [env.BuildLibrary(os.path.join("$BUILD_DIR", "ConceptualFramework"), os.path.join(FRAMEWORK_DIR, "src")
)]

env.Prepend(LIBS=libs)