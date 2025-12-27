import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_groq import ChatGroq
from langchain.messages  import HumanMessage, AIMessage, SystemMessage
from config import checkpointer, llm

# =====================================================
# Load environment
# =====================================================
load_dotenv()

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")




system_message = SystemMessage(
    content="You are a helpful assistant."
)

# =====================================================
# LLM Node (Graph Node)
# =====================================================
def llm_node(state: MessagesState):
    """
    Takes message history from state and returns AI response.
    """
    messages = state["messages"]

    # Ensure system message exists only once
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [system_message] + messages

    response = llm.invoke(messages)
    return {"messages": [response]}

# =====================================================
# Build LangGraph
# =====================================================
workflow = StateGraph(MessagesState)

workflow.add_node("llm", llm_node)
workflow.add_edge(START, "llm")
workflow.add_edge("llm", END)

graph = workflow.compile(checkpointer=checkpointer)

# =====================================================
# Run graph with thread_id + user message
# =====================================================
def run_graph_with_message(thread_id: str, user_input: str) -> str:
    config = {"configurable": {"thread_id": thread_id}}

    result = graph.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )

    return result["messages"][-1].content

# =====================================================
# Load conversation history
# =====================================================
def load_conversation(thread_id: str):
    snapshots = graph.get_state_history(
        config={"configurable": {"thread_id": thread_id}}
    )

    first_snapshot = next(iter(snapshots))
    messages = first_snapshot.values["messages"]

    paired_messages = []

    for i in range(0, len(messages) - 1, 2):
        if isinstance(messages[i], HumanMessage) and isinstance(messages[i + 1], AIMessage):
            paired_messages.append({
                "Human": messages[i].content,
                "Assistant": messages[i + 1].content
            })

    return paired_messages
