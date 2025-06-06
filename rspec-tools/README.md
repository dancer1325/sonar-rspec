* == python CLI tool / 
  * allows
    * adding & validating rules
  * uses
    * GitHub checks
    * GitHub actions

# Install

```
$ brew install pipenv

$ cd rspec-tools
$ pipenv install -e .
```

# Usage

```
# see ALL commands
$ pipenv run rspec-tools --help
```

# Development

* TODO:
.Install dev dependencies

[source,sh]
----
$ pipenv install --dev
----

.Run tests
[source,sh]
----
$ pipenv run pytest
----

.Format
[source,sh]
----
$ pipenv run black rspec_tools tests
$ pipenv run usort format rspec_tools tests
----

.Lint

Note, this step is not run in CI because it is not configured in CAYC mode.
You can also run flake8 in your IDE.
[source,sh]
----
$ pipenv run flake8
----

.Fixtures

When writing a new test, create a fixture rule in `tests/resources/{invalid_rules, rules}`.

In order to generate an HTML file from the ASCIIdoc, you can use [asciidoctor](https://docs.asciidoctor.org/) as follows:

[source,sh]
----
$ asciidoctor rule.adoc
----
