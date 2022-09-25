"""
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""

from rdkit import Chem
from rdkit.Chem import Descriptors
import functions_framework
import json

# Register an HTTP function with the Functions Framework
@functions_framework.http
def rdkit_molecular_descriptors(request):
  try:
    return_value = []
    request_json = request.get_json()
    calls = request_json["calls"]

    for call in calls:
      smiles = call[0]
      try:
        mol = Chem.MolFromSmiles(smiles)

        descriptor_list = ["ExactMolWt", "FractionCSP3", "NumAliphaticRings",
              "BalabanJ", "BertzCT", "HallKierAlpha","HeavyAtomCount",
              "HeavyAtomMolWt", "MaxAbsPartialCharge",  "MaxPartialCharge",
              "MolLogP", "MolMR", "MolWt","NHOHCount","NOCount",
              "NumAliphaticCarbocycles","NumAliphaticHeterocycles",
              "NumAliphaticRings","NumAromaticCarbocycles",
              "NumAromaticHeterocycles","NumAromaticRings",
              "NumHAcceptors","NumHDonors","NumHeteroatoms",
              "NumRadicalElectrons","NumRotatableBonds",
              "NumSaturatedCarbocycles","NumSaturatedHeterocycles",
              "NumSaturatedRings","NumValenceElectrons"]

        data = {}

        for descriptor_name in descriptor_list:
          data[descriptor_name] = getattr(Descriptors, descriptor_name)(mol)

        molecular_descriptors_as_json_string = json.dumps(data)

        return_value.append(molecular_descriptors_as_json_string)

      except: # pylint: disable=bare-except
        return_value.append("")

    return_json = json.dumps( { "replies" :  return_value} ), 200
    return return_json
  except Exception: # pylint: disable=broad-except
    return (json.dumps({"errorMessage": "something unexpected in input"}),
     400 )
