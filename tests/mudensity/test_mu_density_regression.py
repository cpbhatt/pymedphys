# Copyright (C) 2018 Simon Biggs

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# pylint: disable=C0103,C1801


"""End to end regression testing.
"""

import os

import pytest

import numpy as np

import pymedphys

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), "data")
DELIVERY_DATA_FILEPATH = os.path.abspath(
    os.path.join(DATA_DIRECTORY, "mu_density_example_arrays.npz")
)


@pytest.mark.slow
def test_regression():
    """The results of MU Density calculation should not change
    """
    regress_test_arrays = np.load(DELIVERY_DATA_FILEPATH)

    mu = regress_test_arrays["mu"]
    mlc = regress_test_arrays["mlc"]
    jaw = regress_test_arrays["jaw"]

    cached_mu_density = regress_test_arrays["mu_density"]
    mu_density = pymedphys.mudensity.calculate(mu, mlc, jaw)
    assert np.allclose(mu_density, cached_mu_density, atol=0.1)
