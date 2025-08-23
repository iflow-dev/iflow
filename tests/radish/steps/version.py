from radish import then


@then("I see version information in the header")
def i_see_version_information_in_header(step):
    from bdd.controls.version import Header
    version_text = Header().version
    assert version_text, "Version information not found in header"


@then("I do not see version information in the statistics line")
def i_do_not_see_version_in_statistics_line(step):
    from bdd.controls.version import StatisticsLine
    assert not StatisticsLine().contains_version(), "Version information found in statistics line"


@then("I see the statistics line")
def i_see_statistics_line(step):
    from bdd.controls.version import StatisticsLine
    assert StatisticsLine().is_visible, "Statistics line is not visible"


@then("the statistics line does not contain version information")
def statistics_line_does_not_contain_version(step):
    from bdd.controls.version import StatisticsLine
    assert not StatisticsLine().contains_version(), "Statistics line contains version information"
