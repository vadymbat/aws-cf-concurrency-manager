import json
import logging
import cf_concurrency_macro


logging.basicConfig(level=logging.INFO)
SAMPLE_TEMAPLATE = "demo.json"


def check_resource_quantity(old_fagment, new_fragment):
    assert len(old_fagment[cf_concurrency_macro.CF_RESOURCES]) == len(
        new_fragment[cf_concurrency_macro.CF_RESOURCES]
    )
    logging.info(
        "The resource quanity in the processed template is the same as in the original."
    )


def check_all_resource_present(old_fagment, new_fragment):
    for old_resource in old_fagment[cf_concurrency_macro.CF_RESOURCES]:
        assert (
            old_resource in new_fragment[cf_concurrency_macro.CF_RESOURCES].keys()
        )
    logging.info(
        "All the resource from the original tempalate are present in the new one."
    )


if __name__ == "__main__":
    with open(SAMPLE_TEMAPLATE) as sample_template:
        event = {
            cf_concurrency_macro.FRAGMENT: json.loads(sample_template.read()),
            cf_concurrency_macro.REQUEST_ID: "1",
        }

    processed_event = cf_concurrency_macro.handler(event, "")

    check_resource_quantity(
        event[cf_concurrency_macro.FRAGMENT], processed_event[cf_concurrency_macro.FRAGMENT]
    )

    check_all_resource_present(
        event[cf_concurrency_macro.FRAGMENT], processed_event[cf_concurrency_macro.FRAGMENT]
    )

