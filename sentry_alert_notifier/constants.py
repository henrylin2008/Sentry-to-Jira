class JiraLabel(object):
    SENTRY_AUTO_TICKET_LABEL = "sentry_auto_tickets"
    INTERNAL_TOOLS_JIRA_TICKET_LABEL = "Internal_Tools_Product"
    SUPPLY_CHAIN_JIRA_TICKET_LABEL = "SupplyChain"


class JiraUserID(object):
    KERRY_WEI = "kwei"
    DAVID_WU = "dwu"
    PRIAN = "pkuhanandan"
    BIN_SHI = "bshi"
    JERRY_LIU = "jerry_liu"
    ZUNPING_CHENG = "zcheng"
    CHRIS_KIM = "ckim"
    JOHN_WU = "jwu"
    TONY_SITU = "tsitu"
    SOLA = "sola"
    RICHARD_YE = "rye"
    NIDHEESH = "nidheesh"
    CHINTAN_THAKKEER = "cthakker"
    EMMICIA_BRACEY = "ebracey"
    ANDREW_POTAPOV = "apotapov"
    WILL_YOU = "willyou"
    VINCENT_LI = "vincentli"


class JiraProjectID(object):
    MKL = "10501"  # project = Marketplace & Logistics
    WISH_BLUE = "11209"  # project = WishBlue Eng
    PRODUCT = "10657"  # project = Product


class JiraIssueTypeID(object):
    TASK = "10100"


class JiraIssuePriorityID(object):
    NEEDS_TRIAGE = "10001"
    LOW = "4"
    NORMAL = "10002"
    MEDIUM = "10201"
    HIGH = "2"


class JiraTransitionID(object):
    READY_FOR_ENG = "10906"
    NEED_TRIAGE = "10000"
