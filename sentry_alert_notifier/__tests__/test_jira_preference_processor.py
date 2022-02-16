import pytest
from sentry_alert_notifier.team_preference import generate_ticket_params


@pytest.mark.parametrize(
    "sentry_issue_id, summary, description, team, expected",
    [
        (  # No team preference
            "sentry_id_1",
            "ticket_title_1",
            "ticket_description_1",
            "test_resource_1",
            {
                "fields": {
                    "issuetype": {"id": "10100"},
                    "project": {"id": "10501"},
                    "labels": ["sentry_auto_tickets"],
                    "description": "ticket_description_1",
                    "summary": "ticket_title_1",
                }
            },
        ),
        (  # Orders team preference
            "sentry_id_2",
            "ticket_title_2",
            "ticket_description_2",
            "@ContextLogic/marketplace_orders",
            {
                "fields": {
                    "summary": "ticket_title_2",
                    "description": "ticket_description_2",
                    "issuetype": {"id": "10100"},
                    "project": {"id": "10501"},
                    "labels": ["sentry_auto_tickets"],
                    "status": "10000",
                    "components": [{"name": "Orders"}],
                    "priority": {
                        "id": "10001",
                    },
                },
            },
        ),
        (  # Products team preference
            "sentry_id_3",
            "ticket_title_3",
            "ticket_description_3",
            "@ContextLogic/marketplace_productboost",
            {
                "fields": {
                    "summary": "ticket_title_3",
                    "description": "ticket_description_3",
                    "issuetype": {"id": "10100"},
                    "project": {"id": "10501"},
                    "labels": ["sentry_auto_tickets"],
                    "components": [{"name": "Merchant Products"}],
                    "status": "10906",
                    "priority": {
                        "id": "10001",
                    },
                },
            },
        ),
    ],
)
def test_generate_ticket_params(
    sentry_issue_id, summary, description, team, expected
):
    actual_params = generate_ticket_params(
        summary,
        description,
        team,
    )
    assert actual_params == expected
