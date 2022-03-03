#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ibm_pi_ike_policy
for_more_info:  refer - https://registry.terraform.io/providers/IBM-Cloud/ibm/latest/docs/resources/pi_ike_policy

short_description: Configure IBM Cloud 'ibm_pi_ike_policy' resource

version_added: "2.8"

description:
    - Create, update or destroy an IBM Cloud 'ibm_pi_ike_policy' resource
    - This module does not support idempotency
requirements:
    - IBM-Cloud terraform-provider-ibm v1.39.1
    - Terraform v0.12.20

options:
    pi_cloud_instance_id:
        description:
            - (Required for new resource) PI cloud instance ID
        required: True
        type: str
    pi_policy_name:
        description:
            - (Required for new resource) Name of the IKE Policy
        required: True
        type: str
    pi_policy_dh_group:
        description:
            - (Required for new resource) DH group of the IKE Policy
        required: True
        type: int
    pi_policy_encryption:
        description:
            - (Required for new resource) Encryption of the IKE Policy
        required: True
        type: str
    pi_policy_version:
        description:
            - (Required for new resource) Version of the IKE Policy
        required: True
        type: int
    pi_policy_preshared_key:
        description:
            - (Required for new resource) Preshared key used in this IKE Policy (length of preshared key must be even)
        required: True
        type: str
    pi_policy_key_lifetime:
        description:
            - (Required for new resource) Policy key lifetime
        required: True
        type: int
    pi_policy_authentication:
        description:
            - Authentication for the IKE Policy
        required: False
        type: str
        default: none
    id:
        description:
            - (Required when updating or destroying existing resource) IBM Cloud Resource ID.
        required: False
        type: str
    state:
        description:
            - State of resource
        choices:
            - available
            - absent
        default: available
        required: False
    zone:
        description:
            - Denotes which IBM Cloud zone to connect to in multizone
              environment. This can also be provided via the environment
              variable 'IC_ZONE'.
        required: False
        type: str
    region:
        description:
            - The IBM Cloud region where you want to create your
              resources. If this value is not specified, us-south is
              used by default. This can also be provided via the
              environment variable 'IC_REGION'.
        default: us-south
        required: False
        type: str
    ibmcloud_api_key:
        description:
            - The IBM Cloud API key to authenticate with the IBM Cloud
              platform. This can also be provided via the environment
              variable 'IC_API_KEY'.
        required: True

author:
    - Jay Carman (@jaywcarman)
'''

# Top level parameter keys required by Terraform module
TL_REQUIRED_PARAMETERS = [
    ('pi_cloud_instance_id', 'str'),
    ('pi_policy_name', 'str'),
    ('pi_policy_dh_group', 'int'),
    ('pi_policy_encryption', 'str'),
    ('pi_policy_version', 'int'),
    ('pi_policy_preshared_key', 'str'),
    ('pi_policy_key_lifetime', 'int'),
]

# All top level parameter keys supported by Terraform module
TL_ALL_PARAMETERS = [
    'pi_cloud_instance_id',
    'pi_policy_name',
    'pi_policy_dh_group',
    'pi_policy_encryption',
    'pi_policy_version',
    'pi_policy_preshared_key',
    'pi_policy_key_lifetime',
    'pi_policy_authentication',
]

# Params for Data source
TL_REQUIRED_PARAMETERS_DS = [
]

TL_ALL_PARAMETERS_DS = [
]

TL_CONFLICTS_MAP = {
}

# define available arguments/parameters a user can pass to the module
from ansible_collections.ibm.cloudcollection.plugins.module_utils.ibmcloud import Terraform, ibmcloud_terraform
from ansible.module_utils.basic import env_fallback
module_args = dict(
    pi_cloud_instance_id=dict(
        required=False,
        type='str'),
    pi_policy_name=dict(
        required=False,
        type='str'),
    pi_policy_dh_group=dict(
        required=False,
        type='int'),
    pi_policy_encryption=dict(
        required=False,
        type='str'),
    pi_policy_version=dict(
        required=False,
        type='int'),
    pi_policy_preshared_key=dict(
        required=False,
        type='str'),
    pi_policy_key_lifetime=dict(
        required=False,
        type='int'),
    pi_policy_authentication=dict(
        required=False,
        type='str'),
    id=dict(
        required=False,
        type='str'),
    state=dict(
        type='str',
        required=False,
        default='available',
        choices=(['available', 'absent'])),
    zone=dict(
        type='str',
        fallback=(env_fallback, ['IC_ZONE'])),
    region=dict(
        type='str',
        fallback=(env_fallback, ['IC_REGION']),
        default='us-south'),
    ibmcloud_api_key=dict(
        type='str',
        no_log=True,
        fallback=(env_fallback, ['IC_API_KEY']),
        required=True)
)


def run_module():
    from ansible.module_utils.basic import AnsibleModule

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # New resource required arguments checks
    missing_args = []
    if module.params['id'] is None:
        for arg, _ in TL_REQUIRED_PARAMETERS:
            if module.params[arg] is None:
                missing_args.append(arg)
        if missing_args:
            module.fail_json(msg=(
                "missing required arguments: " + ", ".join(missing_args)))

    conflicts = {}
    if len(TL_CONFLICTS_MAP) != 0:
        for arg in TL_CONFLICTS_MAP:
            if module.params[arg]:
                for conflict in TL_CONFLICTS_MAP[arg]:
                    try:
                        if module.params[conflict]:
                            conflicts[arg] = conflict
                    except KeyError:
                        pass
    if len(conflicts):
        module.fail_json(msg=("conflicts exist: {}".format(conflicts)))

    result = ibmcloud_terraform(
        resource_type='ibm_pi_ike_policy',
        tf_type='resource',
        parameters=module.params,
        ibm_provider_version='1.39.1',
        tl_required_params=TL_REQUIRED_PARAMETERS,
        tl_all_params=TL_ALL_PARAMETERS)

    if result['rc'] > 0:
        module.fail_json(
            msg=Terraform.parse_stderr(result['stderr']), **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()