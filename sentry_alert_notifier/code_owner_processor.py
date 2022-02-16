import pathspec
from pathspec import util
from collections import defaultdict


def _get_matched_patterns(patterns, file_path):
    """
    Args:
        patterns (list): list of pathspec.pattern.Pattern objects to check
        file_path (str): file_path to match
    Returns:
        list: list of matched pathspec.pattern.Pattern
    """
    matched_patterns = []
    for pattern in patterns:
        if pattern.include is not None:
            if file_path in pattern.match((file_path,)):
                matched_patterns.append(pattern)
    return matched_patterns


def _get_most_specific_pattern(patterns):
    """
    Args:
        patterns (list): list of pathspec.pattern.Pattern objects to check
    Returns:
        pathspec.pattern.Pattern: most specific pattern
    """
    if len(patterns) == 0:
        return None

    most_specific_pattern = ""
    most_specific_regex_pattern = ""
    for pattern in patterns:
        if len(pattern.regex.pattern) > len(most_specific_regex_pattern):
            most_specific_pattern = pattern
            most_specific_regex_pattern = pattern.regex.pattern

    return most_specific_pattern


class CodeOwnerProcessor(object):
    def __init__(self, code_owner_str):
        self.spec_set = {}
        self._read_code_owner_spec(code_owner_str)

    def _read_code_owner_spec(self, code_owner_str):
        code_owner = defaultdict(set)
        lines = code_owner_str.split("\n")
        for line in lines:
            if not line:
                continue
            if line.isspace():
                continue
            if line.startswith("#"):
                continue
            
            items = line.split()
            # There could be more than one owner. Assume first value is the primary owner.
            rule, owner = items[0], items[1]
            code_owner[owner].add(rule)

        for owner, rules in code_owner.iteritems():
            self.spec_set[owner] = pathspec.PathSpec.from_lines(
                pathspec.patterns.GitWildMatchPattern,
                rules,
            )

    def _match(self, file_path):
        """
        Args:
            file_path (string): file path to find a matching owner for
        Returns:
            string: owner with the most specific pattern match for the given file
        """
        owner_by_matched_pattern = {}
        for owner, spec in self.spec_set.iteritems():
            for pattern in _get_matched_patterns(spec.patterns, util.normalize_file(file_path)):
                owner_by_matched_pattern[pattern] = owner

        if len(owner_by_matched_pattern) == 0:
            return None

        return owner_by_matched_pattern[_get_most_specific_pattern(owner_by_matched_pattern.keys())]

    def assign_owners(self, issues):
        """
        Args:
            issues (list): list of Issue objects
        """
        for issue in issues:
            file_paths = issue.related_files()
            for file_path in file_paths:
                owner = self._match(file_path)
                if not owner:
                    continue

                # assign owner and break
                issue.owner = owner
                break
