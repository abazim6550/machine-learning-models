from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage

def read_email_tool(id: str) -> str:
    """mocked function to read emails"""
    return f"email content for id {id}"

def send_email_tool(id: str) -> str:
    """mocked function to send email"""
    return f"emil sent to id {id}"

agent=create_agent(
    model="llama3:8b",
    tools=[read_email_tool,send_email_tool],
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                send_email_tool: {
                    'allowed_decisions': ['approve', 'reject']
                },
                read_email_tool: False

            }
        )
    ]
)


config = {"configurable": {"thread_id": "test-approve"}}

result = agent.invoke(
    {"messages": [HumanMessage(content="Send email to destination@test.com'")]},
    config=config
)


from langgraph.types import Command

if "__interrupt__" in result:
    print("⏸️ Paused! Approving...")
    
    result = agent.invoke(
        Command(
            resume={
                "decisions": [
                    {"type": "approve"}
                ]
            }
        ),
        config=config
    )