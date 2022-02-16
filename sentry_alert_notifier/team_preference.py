import attr
from sentry_alert_notifier.constants import (
    JiraTransitionID,
    JiraProjectID,
    JiraIssueTypeID,
    JiraLabel,
    JiraUserID,
    JiraIssuePriorityID,
)


@attr.s
class JiraComponent(object):
    name = attr.ib(type=str)


@attr.s
class JiraProject(object):
    id = attr.ib(type=int)


@attr.s
class JiraPriority(object):
    id = attr.ib(type=int, default=JiraIssuePriorityID.NEEDS_TRIAGE)


@attr.s
class JiraUser(object):
    name = attr.ib(type=str)


@attr.s
class JiraPreference(object):
    project = attr.ib(type=JiraProject)
    priority = attr.ib(type=JiraPriority, default=attr.Factory(lambda: JiraPriority()))
    assignee = attr.ib(type=JiraUser, default=None)
    components = attr.ib(type=list, default=None)
    labels = attr.ib(type=list, default=attr.Factory(lambda: [JiraLabel.SENTRY_AUTO_TICKET_LABEL]))
    status = attr.ib(type=int, default=JiraTransitionID.NEED_TRIAGE)
    watchers = attr.ib(type=list, default=None)


@attr.s
class Team(object):
    name = attr.ib(type=str)
    preference = attr.ib(type=JiraPreference)


product_catalog_team = Team(
    name="Marketplace Product Catalog",
    preference=JiraPreference(
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="Merchant Products"),
        ],
        status=JiraTransitionID.READY_FOR_ENG,
    ),
)


orders_team = Team(
    name="Marketplace Orders",
    preference=JiraPreference(
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="Orders"),
        ],
    ),
)


framework_team = Team(
    name="Marketplace Framework Team",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.KERRY_WEI),
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="Framework"),
        ],
    ),
)


email_and_notification_team = Team(
    name="Marketplace Email and Notifications",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.DAVID_WU),
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="Framework"),
        ],
        watchers=[JiraUserID.KERRY_WEI, JiraUserID.DAVID_WU, JiraUserID.PRIAN],
    ),
)


policy_team = Team(
    name="Marketplace Policy Team",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.BIN_SHI),
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="Policy"),
        ],
    ),
)


tagging_team = Team(
    name="Marketplace Tagging",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.JERRY_LIU),
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="Tagging"),
        ],
    ),
)


payment_team = Team(
    name="Marketplace Payment",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.ZUNPING_CHENG),
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="Merchant Payments"),
        ],
    ),
)


logistics_team = Team(
    name="Marketplace Logistics",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.CHRIS_KIM),
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="FBW"),
        ],
    ),
)


logistics_toronto_team = Team(
    name="Marketplace Logistics Toronto",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.JOHN_WU),
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="MMS"),
        ],
    ),
)


bd_tools_team = Team(
    name="Marketplace BD Tools",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.TONY_SITU),
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="BD Tools"),
        ],
        watchers=[JiraUserID.TONY_SITU],
    ),
)


marketplace_web_team = Team(
    name="Marketplace Web",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.SOLA),
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="Merchant Web"),
        ],
    ),
)


growth_team = Team(
    name="Marketplace Merchant Growth",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.RICHARD_YE),
        project=JiraProject(JiraProjectID.MKL),
        components=[
            JiraComponent(name="Merchant Growth"),
        ],
    ),
)


supply_chain_team = Team(
    name="Marketplace Supply Chain",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.WILL_YOU),
        project=JiraProject(JiraProjectID.MKL),
        labels=[JiraLabel.SENTRY_AUTO_TICKET_LABEL, JiraLabel.SUPPLY_CHAIN_JIRA_TICKET_LABEL],
    ),
)


wishpost_team = Team(
    name="Marketplace Wishpost",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.VINCENT_LI),
        project=JiraProject(JiraProjectID.MKL),
    ),
)


wish_blue_team = Team(
    name="Marketplace Wish Blue",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.ANDREW_POTAPOV),
        project=JiraProject(JiraProjectID.WISH_BLUE),
    ),
)


products_internal_tools = Team(
    name="Wish Internal Tools",
    preference=JiraPreference(
        assignee=JiraUser(JiraUserID.NIDHEESH),
        project=JiraProject(JiraProjectID.PRODUCT),
        labels=[JiraLabel.SENTRY_AUTO_TICKET_LABEL, JiraLabel.INTERNAL_TOOLS_JIRA_TICKET_LABEL],
        watchers=[JiraUserID.KERRY_WEI, JiraUserID.CHINTAN_THAKKEER, JiraUserID.NIDHEESH, JiraUserID.EMMICIA_BRACEY],
    ),
)


def team_preference():
    """
    Returns:
        dict: returns a github team alias -> Team object mapping
    """
    return {
        "@ContextLogic/marketplace_price-drop": product_catalog_team,
        "@ContextLogic/marketplace_product-catalog": product_catalog_team,
        "@ContextLogic/marketplace_productboost": product_catalog_team,
        "@ContextLogic/marketplace_orders": orders_team,
        "@ContextLogic/marketplace_merchant-payments": payment_team,
        "@ContextLogic/marketplace_policy": policy_team,
        "@ContextLogic/marketplace_tagging": tagging_team,
        "@ContextLogic/marketplace_content": tagging_team,
        "@ContextLogic/marketplace_logistics-eng": logistics_team,
        "@ContextLogic/logistics_fbs": logistics_team,
        "@ContextLogic/logistics_fbw": logistics_team,
        "@ContextLogic/marketplace_logistics-eng-toronto": logistics_toronto_team,
        "@ContextLogic/logistics_tracking": logistics_team,
        "@ContextLogic/product_internal_tools_reviewers": products_internal_tools,
        "@ContextLogic/marketplace-wish-blue": wish_blue_team,
        "@ContextLogic/bd-tools-and-security": bd_tools_team,
        "@ContextLogic/marketplace_graphql-reviewers": marketplace_web_team,
        "@ContextLogic/marketplace_web-reviewers": marketplace_web_team,
        "@ContextLogic/marketplace_web_and_mobile": marketplace_web_team,
        "@ContextLogic/marketplace-growth": growth_team,
        "@ContextLogic/merchant-growth": growth_team,
        "@ContextLogic/marketplace-external-api": framework_team,
        "@ContextLogic/marketplace-supply-chain": supply_chain_team,
        "@ContextLogic/marketplace_notifications": email_and_notification_team,
        "@ContextLogic/marketplace_wishpost": wishpost_team,
    }


def generate_ticket_params(summary, description, github_team):
    """
    Args:
        summary (str): jira ticket summary
        description (str): jira ticket description
        github_team (str): the Github team name. i.e. "@ContextLogic/marketplace_price-drop"
    Returns:
        dict: parameters used to create jira ticket
    """
    issue_params = {
        "fields": {
            "summary": summary,
            "description": description,
            "issuetype": {
                "id": JiraIssueTypeID.TASK,
            },
            "project": {
                "id": JiraProjectID.MKL,
            },
            "labels": [
                "sentry_auto_tickets",
            ]
        }
    }
    team = team_preference().get(github_team)
    if not team or not team.preference:
        return issue_params

    pref_dict = attr.asdict(
        team.preference,
        filter=attr.filters.exclude(type(None))
    )
    issue_params["fields"].update(pref_dict)
    return issue_params
