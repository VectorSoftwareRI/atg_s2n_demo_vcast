# The MIT License
#
# Copyright (c) 2020 Vector Informatik, GmbH. http://vector.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os

import atg_execution.scm_hooks as atg_scm_hooks
from functools import partial


def __guess_location():
    start = os.path.dirname(__file__)
    needed = ["src", "vcast", ".git"]
    while start != "/" and not all(
        [os.path.exists(os.path.join(start, req)) for req in needed]
    ):
        start = os.path.dirname(start)

    if start == "/":
        return None

    return start


def store_updated_tests(changed_files):
    print("The following changed files were reported as changed:")
    for fname in changed_files:
        print("    {:s}".format(fname))


def get_configuration(options):
    # Guess where this repo lives
    cloned_location = __guess_location()
    assert cloned_location is not None

    # What's the path to our repo?
    repository_path = os.path.abspath(os.path.join(cloned_location, "src"))

    # What's the path to our Manage root folder?
    manage_vcm_path = os.path.abspath(os.path.join(cloned_location, "vcast", "s2n.vcm"))

    # Set the environment variable needed for the environments to build
    os.environ["S2N_SRC_PATH"] = repository_path

    # What two shas do we want to analyse?
    current_id = "c158f0c8cb190b5121702fbe0e2b16547c5b63b4"
    new_id = "4caa406c233b57e6f0bb7d5a62c83aca237b7e31"

    # Build-up an impact object
    impact_object = atg_scm_hooks.GitImpactedObjectFinder(
        repository_path, allow_moves=options.allow_moves
    )

    # Create a 'future' for the unchanged function call
    find_unchanged_files = partial(
        impact_object.calculate_preserved_files, current_id=current_id, new_id=new_id
    )

    configuration = {
        "repository_path": repository_path,
        "manage_vcm_path": manage_vcm_path,
        "find_unchanged_files": find_unchanged_files,
        "store_updated_tests": store_updated_tests,
    }

    return configuration


# EOF


# EOF
