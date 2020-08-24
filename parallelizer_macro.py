#!/bin/env python

import json

FRAGMENT = "fragment"
REQUEST_ID = "requestId"
CF_STACK_STATUS = "status"
CF_STATUS_SUCCESS = "SUCCESS"
CF_STATUS_FAILURE = "FAILURE"
CF_RESOURCES = "Resources"
CF_DEPENDS_ON = "DependsOn"
CF_PARALLEL_PARAM_KEY = "ParallelTaskQuantity"
CF_COMMON_DEPENDANCIES_KEY = "CommonDependancies"


def create_deploy_streams(resource_list, deploy_streams_quantity):
    streams = []
    resource_quantity = len(resource_list)
    stream_length = resource_quantity // deploy_streams_quantity
    last_stream_index = deploy_streams_quantity - 1
    for i in range(0, resource_quantity, stream_length):
        if len(streams) == last_stream_index:
            streams.append(resource_list[i:])
            return streams
        streams.append(resource_list[i:i + stream_length])


def create_dependency_tree(fragment, cf_thread, common_dependencies):
    previous_resource_name = ""
    resources = fragment[CF_RESOURCES]
    for resource_name in cf_thread:
        resource = resources[resource_name]
        if CF_DEPENDS_ON in resource:
            del resource[CF_DEPENDS_ON]
        dependencies = []
        if(common_dependencies):
            dependencies += common_dependencies
        if (previous_resource_name):
            dependencies.append(previous_resource_name)
        if (dependencies):
            resource[CF_DEPENDS_ON] = dependencies
        previous_resource_name = resource_name


def handle_template(fragment):
    streams_quantity = fragment.get(CF_PARALLEL_PARAM_KEY)
    common_dependencies = fragment.get(CF_COMMON_DEPENDANCIES_KEY)
    if streams_quantity:
        resource_list = list(fragment.get(CF_RESOURCES).keys())
        if streams_quantity > len(resource_list):
            raise ValueError("The quantity of parallel tasks can't be greater than resource quantity.")
        if common_dependencies:
            resource_list = list(set(resource_list) - set(common_dependencies))
            del fragment[CF_COMMON_DEPENDANCIES_KEY]
        for stream in create_deploy_streams(resource_list, streams_quantity):
            create_dependency_tree(fragment, stream, common_dependencies)
        del fragment[CF_PARALLEL_PARAM_KEY]
    return fragment


def handler(event, context):
    fragment = event[FRAGMENT]
    status = CF_STATUS_SUCCESS

    try:
        fragment = handle_template(fragment)
    except Exception as e:
        status = CF_STATUS_FAILURE
        print(e)

    return {
        REQUEST_ID: event[REQUEST_ID],
        CF_STACK_STATUS: status,
        FRAGMENT: fragment,
    }


if __name__ == "__main__":
    with open("demo.json") as semple:
        event = {
            FRAGMENT: json.loads(semple.read()),
            REQUEST_ID: "1"
        }
        handler(event, "")
