import asyncio
import random
from datetime import datetime, timezone
from typing import TypedDict

from mcp import ServerSession
from mcp.server.fastmcp import Context
from pydantic import BaseModel

from . import mcp_server


@mcp_server.tool()
def get_current_time() -> str:
    """Return the current server time as a string."""
    return datetime.now(timezone.utc).isoformat()


@mcp_server.tool()
def roll_a_dice(sides: int = 6) -> int:
    """Roll a dice with a specified number of sides and return the result."""
    return random.randint(1, sides)


@mcp_server.tool()
async def get_weather(city: str, time: datetime, ctx: Context) -> str:
    await ctx.info("Calling get_weather tool")
    await ctx.info(f"city: {city}; {type(time) = }, {time = }")
    await asyncio.sleep(0.1)  # Simulate network delay
    return "Sunny with a chance of rain"


@mcp_server.tool()
async def long_running_task(
    task_name: str, ctx: Context[ServerSession, None], steps: int = 5
) -> str:
    """Execute a task with progress updates."""
    await ctx.info(f"Starting: {task_name}")

    for i in range(steps):
        progress = (i + 1) / steps
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Step {i + 1}/{steps}",
        )
        await ctx.debug(f"Completed step {i + 1}")

    return f"Task '{task_name}' completed"


class NumberGuessingUserInputSchema(BaseModel):
    value: int
    """The user's guessed number."""


class NumberGuessingOutputSchema(TypedDict):
    has_won: bool
    """Indicates whether the user has won the game."""
    guesses: list[int]
    """List of user's guesses."""
    answer: int
    """The correct answer."""
    max_allowed_attempts: int
    """Maximum number of allowed attempts."""


@mcp_server.tool(structured_output=True)
async def number_guessing_game(
    ctx: Context[ServerSession, None],
    max_number: int = 100,
    max_attempts: int = 5,
) -> NumberGuessingOutputSchema:
    """A simple number guessing game using elicitation."""
    number_to_guess = random.randint(1, max_number)
    await ctx.info("Welcome to the Number Guessing Game!")
    await ctx.info(
        f"I'm thinking of a number between 1 and {max_number}. You have {max_attempts} attempts to guess it."
    )
    guesses: list[int] = []

    for attempt in range(1, max_attempts + 1):
        response = await ctx.elicit(
            f"Attempt {attempt}: What's your guess?",
            schema=NumberGuessingUserInputSchema,
        )

        if response.action == "accept":
            guess = response.data.value
            guesses.append(guess)
            if guess < number_to_guess:
                await ctx.info("Too low!")
            elif guess > number_to_guess:
                await ctx.info("Too high!")
            else:
                await ctx.info(
                    f"Congratulations! You've guessed the number {number_to_guess}!"
                )
                return {
                    "answer": number_to_guess,
                    "has_won": True,
                    "max_allowed_attempts": max_attempts,
                    "guesses": guesses,
                }

    await ctx.info(
        f"Sorry, you've used all your attempts. The number was {number_to_guess}."
    )
    return {
        "answer": number_to_guess,
        "has_won": False,
        "max_allowed_attempts": max_attempts,
        "guesses": guesses,
    }
