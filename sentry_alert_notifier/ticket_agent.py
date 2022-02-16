import json
import logging
from copy import deepcopy

import attr

from sentry_alert_notifier.jira.client import JiraClient
from sentry_alert_notifier.sentry.client import SentryClient
from sentry_alert_notifier.sentry.issue_filter import filter_new_issues
from sentry_alert_notifier.project_config import ProjectConfig
from sentry_alert_notifier.team_preference import generate_ticket_params
from sentry_alert_notifier.team_preference import team_preference
from sentry_alert_notifier.sentry.issues.fetcher import get_sentry_issues


@attr.s
class Summary(object):
    created = attr.ib(type=list, default=attr.Factory(list))
    failed = attr.ib(type=list, default=attr.Factory(list))
    dryrun = attr.ib(type=list, default=attr.Factory(list))


class TicketAgent(object):
    DEFAULT_ASSIGNEE = "kwei"
    JIRA_NOTE = "Feature owner needs to verify the fix and mark the sentry issue as resolved.\n" \
                "Please do not change title's url part, otherwise a duplicate ticket will get " \
                "created (but move to different project is ok)"
    WIKI_PAGE = "https://wiki.wish.site/pages/viewpage.action?pageId=26509977"

    def __init__(self, sentry_token, jira_token, dry_run):
        """
        Args:
            sentry_token (str): Auth token used to access sentry API
            jira_token (str): Auth token used to access Jira API
            dry_run (bool): indicate whether or not to actually create ticket
        """
        # init Sentry client
        sentry_url = "https://sentry.infra.wish.com"
        self.sentry_client = SentryClient(sentry_url, sentry_token)

        # init Jira client
        jira_url = "https://jira.wish.site"
        self.jira_client = JiraClient(jira_url, jira_token)

        self.dry_run = dry_run
        self.summary = Summary()

    def _get_sentry_issues(self, project, code_owner_str):
        """
        Args:
            project (ProjectConfig): sentry project name
        Returns:
            list: list of issues used for cutting tickets
        """
        issues = get_sentry_issues(self.sentry_client, project, code_owner_str)
        issues = filter_new_issues(self.jira_client, issues)
        logging.info("%s issues left after skipping already reported errors", len(issues))
        issues = [issue for issue in issues if issue.owner]
        logging.info("%s issues left after skipping owner-less errors", len(issues))
        team_pref = team_preference()
        issues = [issue for issue in issues if issue.owner in team_pref]
        logging.info("%s issues left after skipping errors whose team has no ticket preference", len(issues))
        return issues

    def _create_jira_ticket(self, sentry_issue):
        """
        Args:
            sentry_issue (Issue): sentry issue which will be used to cut jira ticket
        """
        logging.info("attempting to create Jira ticket for Sentry issue %s", sentry_issue.permalink)
        summary = "[sentry error] {sentry_issue_link}".format(sentry_issue_link=sentry_issue.permalink)
        description = \
            "sentry issue link:\n" \
            "[{sentry_issue_link}]\n\n" \
            "issue:\n{content}\n{culprit}\n\n" \
            "event count: {count}\n\n" \
            "note:\n{note}\n\n" \
            "Instructions on how to handle sentry errors: [{wiki_link}]".format(
                sentry_issue_link=sentry_issue.permalink,
                content=sentry_issue.title,
                culprit=sentry_issue.culprit,
                count=sentry_issue.count,
                note=self.JIRA_NOTE,
                wiki_link=self.WIKI_PAGE,
            )
        issue_params = generate_ticket_params(
            summary, description, sentry_issue.owner,
        )
        logging.info("Sentry ticket config: %s", issue_params)
        if self.dry_run:
            logging.info("dry-run mode, skip cutting ticket for Sentry issue %s", sentry_issue.permalink)
            self.summary.dryrun.append(sentry_issue.permalink)
            return
        try:
            # record status and update the issue later if needed
            status = issue_params.get("fields").pop("status", None)
            # record watchers and update the issue later if needed
            watchers = ",".join(issue_params.get("fields").pop("watchers", []))
            ticket = self.jira_client.create_issue(params=json.dumps(issue_params))
            ticket_key = ticket.get("key")
            if not ticket_key:
                logging.error(ticket)
                raise Exception("failed to create Jira ticket")

            logging.info("Jira ticket %s created for sentry issue %s", ticket_key, sentry_issue.id_)
            if watchers:
                self.jira_client.add_watcher(ticket_key, json.dumps(watchers))
            if status:
                # update status since we cannot set it when creation
                self.jira_client.update_status(ticket_key, status)
            self.summary.created.append(sentry_issue.permalink)
        except Exception as e:
            logging.error(
                "Failed to create jira ticket for sentry issue %s:\n%s", sentry_issue.id_, str(e)
            )
            logging.error("Error details: %s", str(e))
            self.summary.failed.append(sentry_issue.permalink)

    def cut_tickets_for_project(self, project, code_owner_str):
        """
        Args:
            project (ProjectConfig): sentry project
            code_owner_str (str): CODEOWNERS file in str format
        Returns:
            Summary: a summary object
        """
        logging.info("processing project %s", project.name)
        issues = self._get_sentry_issues(project, code_owner_str)
        logging.info(
            "cutting tickets for the following issues:\n%s",
            "\n".join([issue.permalink for issue in issues])
        )
        for sentry_issue in issues:
            self._create_jira_ticket(sentry_issue)

        # reset summary and return
        ret = deepcopy(self.summary)
        self.summary = Summary()
        return ret
