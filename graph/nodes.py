import logging

from langchain_core.messages import ToolMessage
from langgraph.types import interrupt


logger = logging.getLogger(__name__)


# Only operations that can change repository state require approval.
APPROVAL_REQUIRED_TOOLS = {
    "index_repository",
}


class ApprovalNode:

    @staticmethod
    def execute(state):

        messages = state.get(
            "messages",
            [],
        )

        if not messages:
            return {
                "approval_status": "not_required"
            }

        last_message = messages[-1]

        tool_calls = (
            getattr(
                last_message,
                "tool_calls",
                [],
            )
            or []
        )

        approval_required = [
            call
            for call in tool_calls
            if call.get("name")
            in APPROVAL_REQUIRED_TOOLS
        ]

        if not approval_required:

            logger.info(
                "graph_node=approval "
                "event=not_required"
            )

            return {
                "approval_status": "not_required",
                "approval_request": None,
            }

        requested_tools = []

        for call in approval_required:

            requested_tools.append(
                {
                    "tool_call_id": call.get(
                        "id"
                    ),
                    "tool": call.get(
                        "name"
                    ),
                    "arguments": call.get(
                        "args",
                        {},
                    ),
                }
            )

        approval_request = {
            "type": "tool_approval",
            "message": (
                "The agent wants to execute "
                "a repository-changing operation."
            ),
            "tools": requested_tools,
        }

        logger.info(
            "graph_node=approval "
            "event=interrupt "
            "tools=%s",
            [
                item["tool"]
                for item in requested_tools
            ],
        )

        decision = interrupt(
            approval_request
        )

        approved = bool(
            decision.get(
                "approved",
                False,
            )
        )

        if approved:

            logger.info(
                "graph_node=approval "
                "event=approved "
                "tools=%s",
                [
                    item["tool"]
                    for item in requested_tools
                ],
            )

            return {
                "approval_status": "approved",
                "approval_request": approval_request,
            }

        logger.info(
            "graph_node=approval "
            "event=rejected "
            "tools=%s",
            [
                item["tool"]
                for item in requested_tools
            ],
        )

        rejection_messages = []

        for call in approval_required:

            rejection_messages.append(
                ToolMessage(
                    content=(
                        "Human approval was rejected. "
                        "Do not execute this operation."
                    ),
                    tool_call_id=call.get(
                        "id"
                    ),
                )
            )

        return {
            "messages": rejection_messages,
            "approval_status": "rejected",
            "approval_request": approval_request,
        }