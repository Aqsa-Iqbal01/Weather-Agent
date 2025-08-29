import asyncio
from decouple import config
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool , set_tracing_disabled


GEMINI_API_KEY = config("GEMINI_API_KEY")
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
    Returns mocked temperature for a given city.
    """
    mock_data = {
        "Karachi": "33°C, hot and humid",
        "Lahore": "36°C, dry and sunny",
        "Islamabad": "30°C, partly cloudy",
        "New York": "22°C, cool and breezy",
        "London" : "20°C, cool and clear"
    }
    return mock_data.get(city, f"Sorry, I don't have weather data for {city} right now.")


weather_agent = Agent(
    name="WeatherInfoAgent",
    instructions=(
        "You are a weather bot. "
        "If someone asks about the weather in a city, use the get_weather tool. and if the user try to ask about something else you simply refuse and tell i dont know the answer if user type in small letter the inform them that the city names should be in title case or like the first letter should be capital  , "
    ),
    model=MODEL,
    tools=[get_weather],
)


async def main():
    while True:
        print("\nWelcome to the weather app you can check the weather of your favourite city\n")
        print("Type 'exit , quit , stop' to exit the program\n")
        question = input("You: ")
        if question.lower() in ["exit", "quit" , "stop"]:
            break
        result = await Runner.run(weather_agent, question)
        print("Agent:", result.final_output)

asyncio.run(main())