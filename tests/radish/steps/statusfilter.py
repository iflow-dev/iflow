from radish import step
from bdd.controls import Artifacts, Toolbar


@step(r"I set the status filter to {status:QuotedString}")
def i_set_status_filter_to(step, status):
    toolbar = Toolbar()
    toolbar.filter.status.select(status)


@step(r"I verify the status filter is set to {status:QuotedString}")
def i_verify_status_filter_is_set_to(step, status):
    actual_value = Toolbar().filter.status.value
    assert actual_value == status, f"Status filter verification failed: expected '{status}', but got '{actual_value}'"


@step(r"I see only artifacts with status {status:QuotedString}")
def i_see_only_artifacts_with_status(step, status):
    status_artifacts = [a for a in Artifacts().find() if a.status == status]

    assert status_artifacts, f"No artifacts found with status '{status}'"


@step("I clear the status filter")
def i_clear_status_filter(step):
    toolbar = Toolbar()
    toolbar.filter.status.select("")


@step("I verify the status filter is cleared")
def i_verify_status_filter_is_cleared(step):
    actual_value = Toolbar().filter.status.value
    assert not actual_value or actual_value == "", f"Status filter not cleared: got '{actual_value}' instead of empty"


@step("I see all artifacts again")
def i_see_all_artifacts_again(step):
    all_artifacts = Artifacts().find()
    assert all_artifacts, "No artifacts are visible after clearing the filter"
