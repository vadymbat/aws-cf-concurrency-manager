#!/bin/env python

import json

FRAGMENT = "fragment"
REQUEST_ID = "requestId"
STATUS = "status"
SUCCESS = "SUCCESS"
FAILURE = "FAILURE"
RESOURCES = "Resources"
DEPENDS_ON = "DependsOn"
CF_PARALLEL_PARAM = "ParallelTaskQuantity"
CF_COMMON_DEPENDANCIES = "CommonDependancies"


def create_deploy_streams(resource_list, concurrency_number):
    parallel_length = len(resource_list) // concurrency_number
    for i in range(0, len(resource_list), parallel_length):
        yield resource_list[i:i+parallel_length]


def create_dependency_tree(fragment, cf_thread, common_dependencies):
    previous_resource_name = ""
    resources = fragment[RESOURCES]
    for resource_name in cf_thread:
        resource = resources[resource_name]
        if DEPENDS_ON in resource:
            del resource[DEPENDS_ON]
        dependencies = []
        if(common_dependencies):
            dependencies += common_dependencies
        if (previous_resource_name):
            dependencies.append(previous_resource_name)
        if (dependencies):
            resource[DEPENDS_ON] = dependencies
        previous_resource_name = resource_name


def handle_template(fragment):
    theads_quantity = fragment.get(CF_PARALLEL_PARAM)
    common_dependencies = fragment.get(CF_COMMON_DEPENDANCIES)
    if theads_quantity:
        resource_list = list(fragment.get(RESOURCES).keys())
        if common_dependencies:
            resource_list = list(set(resource_list) - set(common_dependencies))
            del fragment[CF_COMMON_DEPENDANCIES]
        for thread in create_deploy_streams(resource_list, theads_quantity):
            create_dependency_tree(fragment, thread, common_dependencies)
        del fragment[CF_PARALLEL_PARAM]
    return fragment


def handler(event, context):
    fragment = event[FRAGMENT]
    status = SUCCESS

    try:
        fragment = handle_template(fragment)
    except Exception as e:
        status = FAILURE
        print(e)

    return {
        REQUEST_ID: event[REQUEST_ID],
        STATUS: status,
        FRAGMENT: fragment,
    }


with open("demo.json") as semple:
    event = {
        FRAGMENT: json.loads(semple.read()),
        REQUEST_ID: "1"
    }
    handler(event, "")
