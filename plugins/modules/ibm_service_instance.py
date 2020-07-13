#!/usr/bin/python
# -*- coding: utf-8 -*-

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: ibm_service_instance
short_description: Configure IBM Cloud 'ibm_service_instance' resource

version_added: "2.8"

description:
    - Create, update or destroy an IBM Cloud 'ibm_service_instance' resource

requirements:
    - IBM-Cloud terraform-provider-ibm v1.8.1
    - Terraform v0.12.20

options:
    name:
        description:
            - (Required for new resource) A name for the service instance
        required: True
        type: str
    space_guid:
        description:
            - (Required for new resource) The guid of the space in which the instance will be created
        required: True
        type: str
    service_keys:
        description:
            - The service keys asociated with the service instance
        required: False
        type: list
        elements: dict
    parameters:
        description:
            - Arbitrary parameters to pass along to the service broker. Must be a JSON object
        required: False
        type: dict
    plan:
        description:
            - (Required for new resource) The plan type of the service
        required: True
        type: str
    tags:
        description:
            - None
        required: False
        type: list
        elements: str
    service:
        description:
            - (Required for new resource) The name of the service offering like speech_to_text, text_to_speech etc
        required: True
        type: str
    credentials:
        description:
            - The service broker-provided credentials to use this service.
        required: False
        type: dict
    service_plan_guid:
        description:
            - The uniquie identifier of the service offering plan type
        required: False
        type: str
    wait_time_minutes:
        description:
            - Define timeout to wait for the service instances to succeeded/deleted etc.
        required: False
        type: int
        default: 10
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
    iaas_classic_username:
        description:
            - (Required when generation = 1) The IBM Cloud Classic
              Infrastructure (SoftLayer) user name. This can also be provided
              via the environment variable 'IAAS_CLASSIC_USERNAME'.
        required: False
    iaas_classic_api_key:
        description:
            - (Required when generation = 1) The IBM Cloud Classic
              Infrastructure API key. This can also be provided via the
              environment variable 'IAAS_CLASSIC_API_KEY'.
        required: False
    region:
        description:
            - The IBM Cloud region where you want to create your
              resources. If this value is not specified, us-south is
              used by default. This can also be provided via the
              environment variable 'IC_REGION'.
        default: us-south
        required: False
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
    ('name', 'str'),
    ('space_guid', 'str'),
    ('plan', 'str'),
    ('service', 'str'),
]

# All top level parameter keys supported by Terraform module
TL_ALL_PARAMETERS = [
    'name',
    'space_guid',
    'service_keys',
    'parameters',
    'plan',
    'tags',
    'service',
    'credentials',
    'service_plan_guid',
    'wait_time_minutes',
]

# define available arguments/parameters a user can pass to the module
from ansible_collections.ibm.cloudcollection.plugins.module_utils.ibmcloud import Terraform, ibmcloud_terraform
from ansible.module_utils.basic import env_fallback
module_args = dict(
    name=dict(
        required= False,
        type='str'),
    space_guid=dict(
        required= False,
        type='str'),
    service_keys=dict(
        required= False,
        elements='',
        type='list'),
    parameters=dict(
        required= False,
        type='dict'),
    plan=dict(
        required= False,
        type='str'),
    tags=dict(
        required= False,
        elements='',
        type='list'),
    service=dict(
        required= False,
        type='str'),
    credentials=dict(
        required= False,
        type='dict'),
    service_plan_guid=dict(
        required= False,
        type='str'),
    wait_time_minutes=dict(
        default=10,
        type='int'),
    id=dict(
        required= False,
        type='str'),
    state=dict(
        type='str',
        required=False,
        default='available',
        choices=(['available', 'absent'])),
    iaas_classic_username=dict(
        type='str',
        no_log=True,
        fallback=(env_fallback, ['IAAS_CLASSIC_USERNAME']),
        required=False),
    iaas_classic_api_key=dict(
        type='str',
        no_log=True,
        fallback=(env_fallback, ['IAAS_CLASSIC_API_KEY']),
        required=False),
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

    result = ibmcloud_terraform(
        resource_type='ibm_service_instance',
        tf_type='resource',
        parameters=module.params,
        ibm_provider_version='1.8.1',
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
