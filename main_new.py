'''
# pip install langgraph langchain langchain-openai langchain-groq langchain-community langchain-tavily psycopg[binary] psycopg_pool python-dotenv tavily-python pip install requests streamlit

# install PostgresSql and create database
CREATE DATABASE langgraph_memory;  ( or open pgadmin4 and create database there )
'''
# LangGraph Multi-Agent Travel Booking System with Long-Term Memory

# main.py

import os
from typing import TypedDict, Annotated
import operator

import psycopg
from psycopg.rows import dict_row
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# LLM
llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

# State
class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    advisory: str
    llm_calls: int

# Flight Agent
def flight_agent(state: TravelState):
    query = state["user_query"]
    flight_data = search_flights(query)
    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(content=f"Flight results fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Hotel Agent
def hotel_agent(state: TravelState):
    query = state["user_query"]

    hotel_search_query = f"""
    Best hotels for this travel request. Focus on destination, hotel category,
    family suitability, location, safety, and budget:
    {query[:250]}
    """

    hotel_results = tavily_search(hotel_search_query)

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Itinerary Agent
def itinerary_agent(state: TravelState):

    prompt = f"""
    Create a travel itinerary.
    User Query:
    {state['user_query']}

    Flight Results:
    {state['flight_results']}

    Hotel Results:
    {state['hotel_results']}
    """

    response = llm.invoke([
        SystemMessage(
            content="You are an expert travel planner"
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
# Travel Advisory Agent
def travel_advisory_agent(state: TravelState):
    """
    This agent provides practical travel advisory checks:
    - Visa and entry guidance
    - Passport validity reminder
    - Travel insurance recommendation
    - Weather and seasonal advisory
    - Local safety guidance
    - Currency and payment tips
    - Emergency readiness
    """

    query = state["user_query"]

    advisory_search_query = f"""
    Latest travel advisory, visa requirements, passport validity, weather,
    safety tips, currency, travel insurance, and emergency information:
    {query[:250]}   
    """

    advisory_search_results = tavily_search(advisory_search_query)

    prompt = f"""
    You are a senior international travel advisory expert.

    Based on the user travel request, itinerary, flight information, hotel information,
    and latest advisory search results, prepare a practical travel advisory.

    User Travel Request:
    {state['user_query']}

    Flight Results:
    {state['flight_results']}

    Hotel Results:
    {state['hotel_results']}

    Itinerary:
    {state['itinerary']}

    Advisory Search Results:
    {advisory_search_results}

    Prepare the advisory using the following structure:

    1. Visa and Entry Requirements
    - Mention that the traveler must verify the latest official visa rules before booking.
    - Give general visa guidance based on destination.

    2. Passport Validity
    - Mention common requirement: passport should usually be valid for at least 6 months from travel date.

    3. Travel Insurance
    - Recommend insurance coverage for medical emergency, trip cancellation, baggage loss, and flight delay.

    4. Weather and Packing Advisory
    - Suggest practical packing tips based on the destination and season.

    5. Local Safety and Cultural Tips
    - Mention local transport safety, scams, emergency numbers if available, and cultural etiquette.

    6. Currency and Payments
    - Mention currency, card acceptance, cash requirement, and forex planning.

    7. Final Advisory Note
    - Keep it professional, practical, and customer-friendly.
    - Do not create fear; give balanced travel guidance.
    """

    response = llm.invoke([
        SystemMessage(
            content="You are a professional travel risk, visa, safety, and destination advisory expert."
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "advisory": response.content,
        "messages": [
            AIMessage(content="Travel advisory information prepared")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }
# Final Response Agent
def final_agent(state: TravelState):

    final_prompt = f"""
    Generate final travel response.

    Flights:
    {state['flight_results']}

    Hotels:
    {state['hotel_results']}

    Itinerary:
    {state['itinerary']}

    Travel Advisory:
    {state['advisory']}
    """

    response = llm.invoke([
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("advisory_agent", travel_advisory_agent)
graph.add_node("final_agent", final_agent)

graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "advisory_agent")
graph.add_edge("advisory_agent", "final_agent")
graph.add_edge("final_agent", END)


# Persistent connection so both CLI and Streamlit can share the compiled app
# _conn = psycopg.connect(DATABASE_URL)
_conn = psycopg.connect(
    DATABASE_URL,
    autocommit=True,
    row_factory=dict_row
)
checkpointer = PostgresSaver(_conn)
checkpointer.setup()

app = graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "user_akhilesh_trivedi"
        }
    }

    user_input = input("Enter travel request: ")

    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "advisory": "",
            "llm_calls": 0
        },
        config=config
    )

    print("\nFINAL RESPONSE:\n")

    for msg in result["messages"]:
        print(msg.content)
