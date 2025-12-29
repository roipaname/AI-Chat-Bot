from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

@tool
def calculator(a:float,b:float)->str:
    """
   Useful for performing basic arithmetic with numbers
    """
    logging.info(f"Calculating {a} + {b}")
    return f'The result of {a} + {b} is {a+b}'
@tool
def greet_user(name:str)->str:
    """
    Greets the user with their name.
    """
    logging.info(f"Greeting user: {name}")
    return f"Hello, {name}! How can I assist you today?"

def main():
    model=ChatOpenAI(temperature=0)
    tools=[calculator,greet_user]
    agent_exec=create_react_agent(model=model,tools=tools)

    logging.info("Agent si ready to receive your Query.")
    logging.info("You can ask me any calculations or chat with me.")
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit","quit"}:
            break
        print("\nAgent: ",end="")
        for chunk in agent_exec.stream(
            {"messages":[HumanMessage(content=user_input)]}
        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content,end="")
        print()

if __name__=="__main__":
    main()
  

