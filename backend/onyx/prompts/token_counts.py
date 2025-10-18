from onyx.configs.chat_configs import LANGUAGE_HINT
from onyx.llm.utils import check_number_of_tokens
from onyx.prompts.chat_prompts import ADDITIONAL_INFO, CHAT_USER_PROMPT, CITATION_REMINDER
from onyx.prompts.constants import DEFAULT_IGNORE_STATEMENT
from onyx.prompts.prompt_utils import get_current_llm_day_time

CHAT_USER_PROMPT_WITH_CONTEXT_OVERHEAD_TOKEN_CNT = check_number_of_tokens(
    CHAT_USER_PROMPT.format(
        context_docs_str="",
        task_prompt="",
        user_query="",
        optional_ignore_statement=DEFAULT_IGNORE_STATEMENT,
    )
)

CITATION_STATEMENT_TOKEN_CNT = check_number_of_tokens(CITATION_REMINDER)

CITATION_REMINDER_TOKEN_CNT = check_number_of_tokens(CITATION_REMINDER)

LANGUAGE_HINT_TOKEN_CNT = check_number_of_tokens(LANGUAGE_HINT)

ADDITIONAL_INFO_TOKEN_CNT = check_number_of_tokens(ADDITIONAL_INFO.format(datetime_info=get_current_llm_day_time()))
