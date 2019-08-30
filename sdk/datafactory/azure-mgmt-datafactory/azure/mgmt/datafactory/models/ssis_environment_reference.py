# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SsisEnvironmentReference(Model):
    """Ssis environment reference.

    :param id: Environment reference id.
    :type id: long
    :param environment_folder_name: Environment folder name.
    :type environment_folder_name: str
    :param environment_name: Environment name.
    :type environment_name: str
    :param reference_type: Reference type
    :type reference_type: str
    """

    _attribute_map = {
        'id': {'key': 'id', 'type': 'long'},
        'environment_folder_name': {'key': 'environmentFolderName', 'type': 'str'},
        'environment_name': {'key': 'environmentName', 'type': 'str'},
        'reference_type': {'key': 'referenceType', 'type': 'str'},
    }

    def __init__(self, id=None, environment_folder_name=None, environment_name=None, reference_type=None):
        super(SsisEnvironmentReference, self).__init__()
        self.id = id
        self.environment_folder_name = environment_folder_name
        self.environment_name = environment_name
        self.reference_type = reference_type