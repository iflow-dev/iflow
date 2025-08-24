from radish import step
from bdd.controls import Artifacts, Toolbar


@step(r"I set the status filter to {status:QuotedString}")
def i_set_status_filter_to(step, status):
    toolbar = Toolbar()
    toolbar.filter.status.select(status)





@step(r"I see only artifacts with status {status:QuotedString}")
def i_see_only_artifacts_with_status(step, status):
    all_artifacts = Artifacts().find()
    print(f"DEBUG: Found {len(all_artifacts)} total artifacts")
    for a in all_artifacts:
        print(f"DEBUG: Artifact {a.id} has status '{a.status}'")
    
    status_artifacts = [a for a in all_artifacts if a.status and a.status.lower() == status.lower()]
    print(f"DEBUG: Found {len(status_artifacts)} artifacts with status '{status}'")

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
