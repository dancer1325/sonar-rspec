* goal
  * 💡ALL static-analysis rule specification 💡

* uses |
  * SonarLint,
  * SonarCloud,
  * SonarQube

# [rules/](rules)

* `rules/Sxxxx`
  * rule `Sxxxx`'s specification 
  * `rules/Sxxxx/*.adoc`
    * 👀reused -- by -- MULTIPLE language-specific descriptions👀
  * `rules/Sxxxx/metadata.json`
    * shared BETWEEN language-specific RSPECs /
      * 's fields can be overridden / EACH language
  * `rules/Sxxxx/common`
    * COMMON content / shared by ALL supported languages
    * == 
      * `rules/Sxxxx/common/fix`
      * `rules/Sxxxx/common/images`
      * `rules/Sxxxx/common/pitfalls`
      * `rules/Sxxxx/common/resources`
  * `rules/Sxxxx/[LANGUAGE]`
    * language-specific RSPEC
      * ⚠️MUST exist >= 1 subdirectory / EACH language⚠️
    * 👀[supported `LANGUAGE`](supported_languages.adoc) 👀
    * `rules/Sxxxx/[LANGUAGE]/rule.adoc`
      * uses
        * generate the `Sxxxx` rule description -- for -- programming language
    * `rules/Sxxxx/[LANGUAGE]/metadata.json`
      * EACH key overrides `rules/Sxxxx/metadata.json` key

# [shared_content/](shared_content)
* content / shared BETWEEN MULTIPLE rules
* subfolders
  * ❌NOT standardized❌

# Rule description file

* [here](docs/description.md)

# Metadata file

* [here](docs/metadata.md)

# Non-content modifications

* [here](docs/testing.md)

# Search rules

* display ALL specified rules (⚠️implemented or not⚠️)
  * if NOT implemented -> link to PR
* [site](https://sonarsource.github.io/rspec/#/)
* [source code](frontend)

# Create or modify a rule

* TODO: Before, the Languages Team used Jira to host both implemented and unimplemented rules. This is why the `rules` directory contains both too.

However, one of the reasons we are migrating to a git repository is that we want to have a clean process and history for rule creation and modification.

In particular, the main branch aims at representing what will be integrated in the next version of the analyzers, i.e. what will be part of the next releases.

Thus every newly created rule or modification of rule should follow these steps:

. Create a pull request adding or modifying a rule
. Ask for a review
. Create an implementation ticket
. Implement the new rule or the change in the existing rule
. Fetch the updated metadata with `rule-api` by pointing it to the PR branch with `-branch` parameter
. Merge the implementation PR
. Merge the RSPEC PR

A <<multi-language-rule-creation>> is somewhat more involved.

=== 1. Create a pull request

==== To create a new rule
. go to the https://github.com/SonarSource/rspec/actions/workflows/create_new_rspec.yml[Create new RSPEC] GitHub action
. click on the grey _Run wokflow_ button (on the right).
. in the field _"Comma-separated list of targeted languages"_ write the list of languages you want to specify this rule for. +
They can be any of the following:

include::supported_languages.adoc[]

. click on the green _Run workflow_ button.

image::img/new-rule-workflow.png[]

You should see https://github.com/pulls/assigned[a new pull request assigned to you] with the appropriate language labels.
It might take up to a few minutes to appear.
It contains a scaffolding of files for the new rule. Feel free to modify it as you please.

The title of the PR for a new rule will say only "Create rule Sxxxx", which is not very informative. +
Modify the title to better summarize the nature or the rule, so that it is easier to find when searching through unimplemented rules.
Do preserve the "Create rule Sxxxx" prefix, as it is used by our tooling.
For example:

----
Create rule S7028: All identifiers should be in CamelCase
----

Add the description of the PR to further increase its discoverability
(GitHub PR search does not see the `rule.adoc`).
To do that, click on the three dots (next to the smile) on the first comment (created by github-actions bot) and select "Edit".

The rule must contain subdirectories corresponding to all the languages this rule will be implemented for.

Each language subdirectory contains the `rule.adoc` that is the root document used to render the specification.
The rule specification in `rule.adoc` can include other `*.adoc` files that are in the language subdirectory or in the parent directory by using the `include::content.adoc[]` syntax.

To reduce the number of turnarounds with the asciidoc edits you can install an asciidoc plugin.
Otherwise, you can use https://asciidoclive.com/[AsciiDocLIVE] and this https://docs.asciidoctor.org/asciidoc/latest/syntax-quick-reference/[cheatsheet].

==== To add language to an existing rule

Similar to adding a new rule, if the rule exists on the main branch, trigger the "Add language to a rule" GitHub action.

. go to the https://github.com/SonarSource/rspec/actions/workflows/add_language.yml[Add language to a rule] GitHub action
. click on the grey _Run workflow_ button (on the right).
. in the field _"ID of an existing rule"_ write the ID of the existing rule you want to add language to.
It must be in a form `Sxxxx` where `xxxx` is the number of the rule.
For example: `S100`, `S1234`, or `S6000`.
. in the field _"Language to be added to the rule"_ specify one language you want to add to the rule. +
It can be any of the following:

include::supported_languages.adoc[]

. click on the green _Run workflow_ button.

image::img/add-language-workflow.png[]

You should see https://github.com/pulls/assigned[a new pull request assigned to you] with the appropriate language label.
It might take up to a few minutes to appear.
It contains a scaffolding of files for the new rule. Feel free to modify it as you please.

The title of the PR for a new rule will say only "Create rule Sxxxx", which is not very informative. +
Modify the title to better summarize the nature or the rule, so that it is easier to find when searching through unimplemented rules.
Do preserve the "Create rule Sxxxx" prefix, as it is used by our tooling.
For example:
----
Create rule S100: Method names should comply with a naming convention
----

Otherwise, if the rule has not been merged yet (i.e. the rule has not been implemented by any plugin), you can use the already existing PR corresponding to this rule. +

==== To modify an existing rule
Create a branch for your modifications manually.
Then open a pull request manually.
The subject must start with the following required prefix:
----
Modify rule Sxxxx
----
Add a short summary of the PR after the required prefix. For example:
----
Modify rule S1234: Allow tail recursion for languages supporting TCO
----
Add at least one label corresponding to the language(s) the PR relates to.

==== To deprecate a rule
Create a branch for the deprecation manually.
Then open a pull request manually.
In the subject add the following text:
----
Deprecate rule Sxxxx
----
Add at least one label corresponding to the language(s) the PR relates to.

In the `metadata.json` of the rule you want to deprecate:

* Remove all tags
* Remove all quality profiles
* Change the status to `deprecated`
* Fill in the `replacementRules` array with strings in the form `"RSPEC-xxxx"` with the rules that deprecate this one, if any

See link:rules/S1212/metadata.json[S1212] for an example.

==== To delete a rule
If the rule has never been implemented and is still defined in an open pull request, just close the pull request. +
Otherwise, create a pull request to change the status of the rule to "closed".

NOTE: use a GitHub hot-key `t` in the source view to navigate to an existing rule specification.

=== 2. Ask for a review

Every PR that is creating or modifying a rule should be reviewed.
Exceptions can be made for small PRs that only resolve simple spelling mistakes.

If it is a new rule, or if it requires the analyzer to change its implementation, do not merge the pull request yet.

If the change does not require an implementation, merge the pull request after the review.

Following the submission of every PR, an automatic checklist will be generated.
This checklist is intended for the reviewer and serves as a guide to ensure comprehensive evaluation of the PR.
As the reviewer navigates through the review process, each fulfilled item on the checklist should be marked off.

A PR should not be merged before the checklist is fully completed.
This ensures that all necessary checks have been made, and all requirements have been met before merging, fostering a systematic and thorough review process.

=== 3. Create an implementation ticket

Create an implementation ticket as it is usually done for your plugin (i.e. as a Jira ticket or a Github issue). +
For this ticket to be correcty indexed on the search page of the rules, it has to contain the rule ID (RSPEC-1234 or S1234) either in the ticket title or in the ticket description. +
It is also recommended to add a link to the Github Page of the related rule, to ease the navigation between the ticket and the rule.

In the pull request adding the rule specification, add the following text referencing the implementation ticket:
----
Implementation ticket: CPP-1234 (for a CFamily ticket on Jira)
----
or
----
Implementation ticket: SonarSource/sonar-dotnet/issues/1234 (for a sonar-dotnet issue on Github)
----


=== 4. Implement the rule

Implement the rule or the modification as usual, generate the rule metadata,
and merge the rule implementation in your analyzer repository.


==== Generate rule metadata for the analyzer

* Download the last version of https://github.com/SonarSource/sonar-rule-api[rule-api].
* Run `generate` and specify the RSPEC-repository branch with the modified version of the rule specification.

Example:
[source,shell]
----
$ java -jar rule-api-2.1.0.jar generate -branch <RSPEC branch> -rule S4328
----

=== 5. Merge the RSPEC PR

Once the corresponding implementation is done you can merge the PR containing the new rule
(or the new version of the existing rule).

=== Multi-Language Rule Creation
Multi-language rule creation has more steps than the default process because it involves multiple roles that typically do not coincide.
It is infeasible to synchronize the implementation of the rule for all the languages it covers.

. An RSPECator creates a PR and specifies the multi-language rule.
 * The RSPECator asks for a review for the PR.
 * The RSPECator does not merge the PR, even after the review is done.
. The RSPECator opens implementation tickets for all the targeted languages.
. An Ada analyzer developer Alice implements the rule first. Alice prepares the PR with the implementation.
. As soon as the implementation of the rule is ready for Ada analyzer, Alice merges both PRs:
.. Alice fetches the rule metadata with `rule-api` into Ada analyzer. She needs to specify the PR branch in the `-branch` argument of `rule-api`.
.. Alice merges the rule implementation in Ada analyzer.
.. Alice merges the RSPEC PR opened by the RSPECator.
. A Cobol analyzer developer Bob implements the rule some time later. Bob prepares the PR with the implementation.
. As soon as the Cobol implementation is ready:
.. If Bob needs to change the rule specification, he opens an RSPEC PR and uses the PR branch in the `-branch` argument of `rule-api`.
.. Bob fetches the rule metadata with `rule-api` into Cobol analyzer.
.. Bob merges the rule implementation in Cobol analyzer.
.. If Bob had opened an RSPEC PR with changes, he merges it once the rule is implemented in the analyzer.

# Untriaged PRs

* TODO: Untriaged PRs are the ones without any GitHub label assigned to them.
You can easily see all of them with the filter https://github.com/SonarSource/rspec/pulls?q=is%3Aopen+is%3Apr+no%3Alabel[`no:label`].

All triaged PRs should have at least one label that corresponds to the bubble(s) the PR is related to.
This allows bubbles to easily filter the PRs they are interested in.

# Tooling
* [rspec-tools](rspec-tools)

# RSPEC dataflow

![](img/RSPEC-flow-2.png)

* == RSPEC path
  * [inception | Github RSPEC repository, consumption | SQ/SC/SL or on rules.sonarsource.com]
* grayed out
  * OLD days / RSPECs hosted | Jira
