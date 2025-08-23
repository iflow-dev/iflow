from radish import when, then
from bdd.controls.verification import VerificationField, ArtifactForm, ArtifactVerification, SuccessIndicator


@then("I should see a verification field")
def should_see_verification_field(step):
    verification = VerificationField()
    assert verification.is_visible, "Verification field should be visible"


@then("the verification field should have default value {default_value}")
def verification_field_default_value(step, default_value):
    verification = VerificationField()
    assert verification.value == default_value, \
        f"Verification field should have default value '{default_value}', but got '{verification.value}'"


@then("I can edit the verification field")
def can_edit_verification_field(step):
    verification = VerificationField()
    assert verification.is_enabled, "Verification field should be editable"


@when("I set the verification field to {value}")
def set_verification_field(step, value):
    VerificationField().set_value(value)


@then("the artifact should be saved with verification method {method}")
def artifact_saved_with_verification_method(step, method):
    assert ArtifactVerification().contains_method(method), \
        f"Artifact with verification method '{method}' should be displayed"


@then("I should see the verification method displayed")
def should_see_verification_method_displayed(step):
    assert ArtifactVerification().is_visible, "Verification method should be displayed in artifact tile"


@then("it should show {method}")
def should_show_verification_method(step, method):
    assert ArtifactVerification().contains_method(method), \
        f"Verification method should show '{method}'"


@when("I fill in the summary with {summary}")
def fill_in_summary(step, summary):
    ArtifactForm().set_summary(summary)


@when("I fill in the description with {description}")
def fill_in_description(step, description):
    ArtifactForm().set_description(description)


@then("I should see a success message")
def should_see_success_message(step):
    SuccessIndicator().wait_for_success()
