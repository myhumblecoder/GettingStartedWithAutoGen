from autogen import ConversableAgent, GroupChat, GroupChatManager
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Configure LM Studio's local LLM
config_list = [
    {
        "model": "mistral-7b-instruct",
        "base_url": "http://host.docker.internal:1234/v1",
        "api_key": "not-needed",
    }
]

# Create agents
planner = ConversableAgent(
    name="Planner",
    llm_config={
        "config_list": config_list,
        "temperature": 0.7,  # Moved to llm_config root
        "max_tokens": 2048,  # Moved to llm_config root
    },
    system_message="Propose a clear plan to solve the task and guide the group concisely."
)

coder = ConversableAgent(
    name="Coder",
    llm_config={
        "config_list": config_list,
        "temperature": 0.7,
        "max_tokens": 2048,
    },
    system_message="Write Python code based on the Planner's instructions. Add comments."
)

tester = ConversableAgent(
    name="Tester",
    llm_config={
        "config_list": config_list,
        "temperature": 0.7,
        "max_tokens": 2048,
    },
    system_message="Test the Coder's code, report errors, and verify correctness."
)

# Set up group chat
group_chat = GroupChat(
    agents=[planner, coder, tester],
    messages=[],
    max_round=8,
    speaker_selection_method="round_robin"
)

# Create group chat manager
manager = GroupChatManager(
    groupchat=group_chat,
    llm_config={
        "config_list": config_list,
        "temperature": 0.7,
        "max_tokens": 2048,
    }
)

# Initiate chat
task = "Plan and implement a Python function to check if a string is a palindrome."
planner.initiate_chat(manager, message=task)

# Save chat history
with open("chat_history.txt", "w") as f:
    for msg in group_chat.messages:
        f.write(str(msg) + "\n")