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


class ActionGroupsInformation(Model):
    """The Action Groups information, used by the alert rule.

    All required parameters must be populated in order to send to Azure.

    :param custom_email_subject: An optional custom email subject to use in
     email notifications.
    :type custom_email_subject: str
    :param custom_webhook_payload: An optional custom web-hook payload to use
     in web-hook notifications.
    :type custom_webhook_payload: str
    :param group_ids: Required. The Action Group resource IDs.
    :type group_ids: list[str]
    """

    _validation = {
        'group_ids': {'required': True},
    }

    _attribute_map = {
        'custom_email_subject': {'key': 'customEmailSubject', 'type': 'str'},
        'custom_webhook_payload': {'key': 'customWebhookPayload', 'type': 'str'},
        'group_ids': {'key': 'groupIds', 'type': '[str]'},
    }

    def __init__(self, *, group_ids, custom_email_subject: str=None, custom_webhook_payload: str=None, **kwargs) -> None:
        super(ActionGroupsInformation, self).__init__(**kwargs)
        self.custom_email_subject = custom_email_subject
        self.custom_webhook_payload = custom_webhook_payload
        self.group_ids = group_ids