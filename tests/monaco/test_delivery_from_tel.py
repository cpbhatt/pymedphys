# Copyright (C) 2019 Cancer Care Associates and Simon Biggs

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import numpy as np

import pydicom

import pymedphys


def test_delivery_from_monaco():
    data_paths = pymedphys.zip_data_paths("tel-dicom-pairs.zip")
    dir_names = {path.parent.name for path in data_paths}

    assert len(dir_names) >= 2

    for dir_name in dir_names:
        current_paths = [path for path in data_paths if path.parent.name == dir_name]

        tel_path = get_file_type(current_paths, "tel")
        dcm_path = get_file_type(current_paths, "dcm")

        delivery_dcm = pymedphys.Delivery.from_dicom(
            pydicom.read_file(str(dcm_path), force=True)
        )

        delivery_monaco = pymedphys.Delivery.from_monaco(tel_path)

        assert np.allclose(delivery_monaco.mu, delivery_dcm.mu, atol=0.01)
        assert np.allclose(delivery_monaco.gantry, delivery_dcm.gantry, atol=0.01)
        assert np.allclose(
            delivery_monaco.collimator, delivery_dcm.collimator, atol=0.01
        )
        assert np.allclose(delivery_monaco.mlc, delivery_dcm.mlc, atol=0.1)
        assert np.allclose(delivery_monaco.jaw, delivery_dcm.jaw, atol=0.01)


def get_file_type(input_paths, file_type):
    paths = [path for path in input_paths if file_type in path.name]
    assert len(paths) == 1
    return paths[0]
