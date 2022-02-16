# Sentry auto-ticket Agent

## Summary

To help simplify tracking errors originated from [clroot repo](https://github.com/ContextLogic/clroot) in Sentry, Marketplace has launched this auto-ticket agent which runs every 15 minutes and cuts a ticket on any Sentry errors whose last seen time is within 24 hours AND the event count is more than certain threshold. 

This feature is currently enabled with Merchant External API project and Merchant Backend Production project. It will be expanded to cover other projects in the future. Tickets will be auto assigned to team leaders or PMs to be triaged. The auto-ticket feature avoids cutting duplicated tickets by searching Jira using the Sentry link, so as long as the title of the ticket includes the corresponding Sentry issue link, changing attributes (i.e. Status, Component, Label) of the ticket or moving it to a different project won't cause duplicated tickets cut. Closing the Jira ticket alone will  not work as the auto ticket agent would a new one if the underlying Sentry issue is not marked as resolved. 

Please be reminded that this feature is NOT intended to replace Prometheus alerts you set up. It only aims to save you time searching for errors belonging to your team and create tasks to track them manually.

## FAQs

### Is this agent applicable to all projects?
This agent is only intended to solve tracking issues in a repo with mixed ownership from completely different organizations or teams. [clroot repo](https://github.com/ContextLogic/clroot) is a typical example of such candidate. If your service is outside clroot and your own Sentry project, you can simply install existing plugins offered by Sentry to perform actions on issues automatically. There are already a variety of [plugins](https://github.com/getsentry/sentry/tree/master/src/sentry_plugins) to do this for you.  

### How do you avoid duplicated tickets? 
Before creating tickets, our agent would search for Jira by the Sentry issue link (i.e. https://sentry.infra.wish.com/sentry/merchant-external-api/issues/367814/). If there are not issues with an active status (i.e. "Need Triage", "In progress", "Ready for Eng"), the agent would go ahead creating a new close. This means closing the ticket alone in Jira is not enough to fully resolve a Sentry issue -- feature owners need to either release a fix or communicate with our team to avoid cutting tickets for certain exceptions.

### How do you link an Sentry issue with a team?
The ticket agent relies on the user to pass in CODEOWNERS file in string, where file ownership is declared using Github team alias. The sentry-auto-ticket repo maintains a hardcoded mapping of Github team alias -> Jira ticket preference (i.e. in which project to cut tickets, what to set on "Components"/"Labels"/"Status" etc., default assignee). We enforce users to declare code ownership in CODEOWNERS file in clroot for code under sweeper/merchant_dashboard/external and sweeper/merchant_dashboard/processing by introducing a pre-commit hook. We expect other teams/orgs who want to be onboarded to use this tool enforcing the same requirements so that the agent can recognize owners and cut tickets accordingly.


## Links
[Sample ticket created](https://jira.wish.site/browse/WB-1168) 

[Instructions on handling Sentry errors](https://wiki.wish.site/pages/viewpage.action?pageId=26509977)
