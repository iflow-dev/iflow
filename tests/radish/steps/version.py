from radish import then
from bdd.controls.version import Version, StatisticsLine


@then("I see version information in the footer")
def i_see_version_information_in_footer(step):
    assert Version().text, "Version information not found in footer"


@then("I do not see version information in the statistics line")
def i_do_not_see_version_in_statistics_line(step):
    assert not StatisticsLine().contains_version(), "Version information found in statistics line"


@then("I see the statistics line")
def i_see_statistics_line(step):
    assert StatisticsLine().is_visible, "Statistics line is not visible"


@then("the statistics line does not contain version information")
def statistics_line_does_not_contain_version(step):
    assert not StatisticsLine().contains_version(), "Statistics line contains version information"
