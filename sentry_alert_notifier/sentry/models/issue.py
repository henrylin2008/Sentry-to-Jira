import attr
from datetime import datetime
from sentry_alert_notifier.sentry.models.issue_metadata import IssueMetaData


@attr.s(eq=False)
class Issue(object):
    id_ = attr.ib(type=int)
    permalink = attr.ib(type=str)
    culprit = attr.ib(type=str, default=None)
    metadata = attr.ib(type=IssueMetaData, default=None)
    title = attr.ib(type=str, default=None)
    urls = attr.ib(type=list, default=None)
    count = attr.ib(type=int, default=0)
    most_counted_url = attr.ib(type=str, default=None)
    firstSeen = attr.ib(type=datetime, default=None)
    lastSeen = attr.ib(type=datetime, default=None)
    # the Github team name. i.e. "@ContextLogic/marketplace_price-drop"
    owner = attr.ib(type=str, default=None)
    # head of the list represent bottom of the stack
    stack_traces = attr.ib(type=list, default=attr.Factory(list))

    @staticmethod
    def _ignored_parent_paths():
        return (
            "sweeper/merchant_dashboard/external/v3/common",
        )

    def _ignore_stack_trace(self, stack_trace):
        # skip the file path is it's part of some ancestor files
        for ignored_parent_path in self._ignored_parent_paths():
            if ignored_parent_path in stack_trace.file_name:
                return True
        return False

    def _stack_trace_without_irrelevant_files(self):
        base_name = "sweeper/merchant_dashboard"
        return [
            stack for stack in self.stack_traces if base_name in stack.file_name
        ]

    def related_files(self):
        stack_traces = self._stack_trace_without_irrelevant_files()
        if not stack_traces:
            return []

        ret = []
        for stack_trace in stack_traces:
            if self._ignore_stack_trace(stack_trace):
                continue
            ret.append(stack_trace.file_name)

        # fall back to top of the stack if no relevant files can be found
        if not ret:
            ret = [stack_traces[0].file_name]

        return ret
