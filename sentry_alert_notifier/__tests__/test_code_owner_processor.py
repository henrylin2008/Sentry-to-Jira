import os
import pytest
from sentry_alert_notifier.code_owner_processor import CodeOwnerProcessor
from sentry_alert_notifier.sentry.models.issue import Issue
from sentry_alert_notifier.sentry.models.stack_trace import StackTrace


@pytest.fixture
def code_owner_str():
    file_path = os.path.join(
        os.path.dirname(__file__), "resources", "CODEOWNER.txt",
    )
    with open(file_path, 'r') as f:
        return f.read()


@pytest.mark.parametrize(
    "issues,expected_owners",
    [
        (
            [
                # stack track of size 1 with code owner declared
                Issue(
                    id_=1,
                    permalink="link",
                    stack_traces=[
                        StackTrace(
                            file_name="sweeper/merchant_dashboard/external/v3/products/variations/api/put_variation.py",
                            line_num=0,
                        ),

                    ],
                ),
                # stack track of common code path to be skipped
                Issue(
                    id_=1,
                    permalink="link",
                    stack_traces=[
                        StackTrace(
                            file_name="sweeper/merchant_dashboard/external/v3/common/method/limiter/base_limiter_method.py",
                            line_num=0,
                        ),
                        StackTrace(
                            file_name="sweeper/merchant_dashboard/external/v3/common/method/base_method.py",
                            line_num=0,
                        ),
                        StackTrace(
                            file_name="sweeper/merchant_dashboard/external/v3/products/variations/api/put_variation.py",
                            line_num=0,
                        ),
                    ],
                ),
                # # stack track with irrelevant parent file path
                Issue(
                    id_=1,
                    permalink="link",
                    stack_traces=[
                        StackTrace(
                            file_name="cl/utils/tornadoutil/abstract.py",
                            line_num=0,
                        ),
                        StackTrace(
                            file_name="sweeper/merchant_dashboard/external/v3/products/variations/api/put_variation.py",
                            line_num=0,
                        ),
                    ],
                ),
                # stack trace with file in the bottom of the stack is the owner
                Issue(
                    id_=1,
                    permalink="link",
                    stack_traces=[
                        StackTrace(
                            file_name="sweeper/merchant_dashboard/some_file/without_owners.py",
                            line_num=0,
                        ),
                        StackTrace(
                            file_name="sweeper/merchant_dashboard/external/v3/products/variations/api/put_variation.py",
                            line_num=0,
                        ),
                    ],
                ),
                # stack trace with only common parent path should get assigned no owners
                Issue(
                    id_=2,
                    permalink="link",
                    stack_traces=[
                        StackTrace(
                            file_name="sweeper/merchant_dashboard/external/v3/common/base_method.py",
                            line_num=0,
                        ),
                    ],
                ),
                Issue(
                    id_=2,
                    permalink="link",
                    stack_traces=[
                        StackTrace(
                            file_name="sweeper/merchant_dashboard/external/v3/common/base_method.py",
                            line_num=0,
                        ),
                        StackTrace(
                            file_name="sweeper/merchant_dashboard/external/v3/common/rate_limiter.py",
                            line_num=0,
                        ),
                    ],
                ),
                # products org code path gets no owners
                Issue(
                    id_=2,
                    permalink="link",
                    stack_traces=[
                        StackTrace(
                            file_name="/sweeper/api/commerce_subscription.py",
                            line_num=0,
                        ),
                        StackTrace(
                            file_name="/sweeper/lib/commerce_subscription_utils.py",
                            line_num=0,
                        ),
                    ],
                ),
                Issue(
                    id_=2,
                    permalink="link",
                    stack_traces=[
                        StackTrace(
                            file_name="/sweeper/merchant_dashboard/model/paypal_merchant.py",
                            line_num=0,
                        ),
                        StackTrace(
                            file_name="sweeper/merchant_dashboard/api/v3_api_internal/paypal/initialize_signup.py",
                            line_num=0,
                        ),
                    ],
                ),
            ],
            [
                "@ContextLogic/marketplace_product-catalog",
                "@ContextLogic/marketplace_product-catalog",
                "@ContextLogic/marketplace_product-catalog",
                "@ContextLogic/marketplace_product-catalog",
                "@ContextLogic/marketplace-external-api",
                "@ContextLogic/marketplace-external-api",
                None,
                "@ContextLogic/marketplace-growth",
            ],
        ),
    ],
)
def test_code_owner_processor(
        issues, expected_owners, code_owner_str
):
    processor = CodeOwnerProcessor(code_owner_str)
    processor.assign_owners(issues)
    for i in xrange(len(issues)):
        issue = issues[i]
        expected = expected_owners[i]
        assert issue.owner == expected
