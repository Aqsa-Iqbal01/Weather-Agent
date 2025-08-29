import asyncio
from decouple import config
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool , set_tracing_disabled
import requests


GEMINI_API_KEY = config("GEMINI_API_KEY")

API_KEY = config("API_KEY")
set_tracing_disabled(True)

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai",
)

MODEL = OpenAIChatCompletionsModel(
    openai_client=client,
    model="gemini-2.5-flash",
)



@function_tool
def get_weather(city: str) -> str:
    """
    Gets real weather using weatherapi.com.
    """
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp_c = data['current']['temp_c']
        condition = data['current']['condition']['text']
        return f"The weather in {city} is {temp_c}°C, {condition}."
    else:
        return f"Sorry, I couldn't get weather for {city}."

weather_agent = Agent(
    name="WeatherInfoAgent",
    instructions=(
        "You are a weather bot. "
        "If someone asks about the weather in a city, use the get_weather tool. and if the user try to ask about something else you simply refuse and tell i dont know the answer , "
    ),
    model=MODEL,
    tools=[get_weather],
)


async def main():
    while True:
        question = input("You: ")
        if question.lower() in ["exit", "quit" , "stop"]:
            break
        result = await Runner.run(weather_agent, question)
        print("Agent:", result.final_output)

asyncio.run(main())