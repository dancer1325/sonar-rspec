import os
from pathlib import Path

import pytest
from rspec_tools.errors import RuleNotFoundError
from rspec_tools.rules import RulesRepository


def test_list_rules(mockrules: Path):
    """Check that rules are all listed."""
    rules = {rule.id for rule in RulesRepository(rules_path=mockrules).rules}
    assert rules == {"S100", "S101", "S120", "S200", "S4727", "S1033"}


def test_list_languages(mockrules: Path):
    """Check that languages are all listed."""
    rule = RulesRepository(rules_path=mockrules).get_rule("S120")

    languages = {lang.language for lang in rule.specializations}
    assert languages == {"flex", "java", "plsql"}

    rulePath = os.path.join(mockrules, "S120")
    ruleSubDirs = [
        subDir
        for subDir in os.listdir(rulePath)
        if os.path.isdir(os.path.join(rulePath, subDir))
    ]
    assert sorted(ruleSubDirs) == ["common", "flex", "java", "plsql"]


def test_get_metadata(mockrules: Path):
    """Check that language metadata are correctly overriden."""
    rule = RulesRepository(rules_path=mockrules).get_rule("S120")
    plsql = rule.get_language("plsql")
    assert plsql.metadata["sqKey"] == "PlSql.PackageNaming"
    java = rule.get_language("java")
    assert java.metadata["sqKey"] == "S120"


def test_nonexisting_rule(mockrules: Path):
    """Check that a nonexisting rule is reported."""
    with pytest.raises(RuleNotFoundError, match=rf"^Cannot find rule S299"):
        RulesRepository(rules_path=mockrules).get_rule("S299")
