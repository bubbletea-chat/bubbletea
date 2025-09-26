"""Movie Guessing Game Bot"""

import os
import json
from typing import Dict, List, Optional, Any
import openai
import bubbletea_chat as bt
from bubbletea_chat.components import Pill, Pills, Text
from dotenv import load_dotenv

load_dotenv()

# Store game states by user session
game_states: Dict[str, "GameState"] = {}

SYSTEM_PROMPT = """
You are a game master for a Movie Guessing Game.

Your task is to generate 5 movie guessing questions. Each question must include:
- a badly written movie description (humorous, vague, or misleading)
- four multiple choice options
- the correct answer (must match one of the options)

The user has selected the following preferences:
- Era: {era}
- Difficulty: {difficulty}
- Genre: {genre}

Please follow these rules:
- Make the bad descriptions short and funny (1-2 sentences).
- Do not use the movie title in the description.
- Avoid repeating any movie across questions.
- Return the result as a JSON array with 5 items. Each item must have:
  - "question": string
  - "options": list of 4 strings
  - "answer": string (must match one of the options)
"""


class GameState:
    """Manages the state of a single game session."""

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the game state to initial values."""
        self.stage = "start"
        self.preferences: Dict[str, str] = {}
        self.questions: List[Dict[str, Any]] = []
        self.index = 0
        self.score = 0
        self.last_answer: Optional[str] = None


def get_or_create_state(user_id: str) -> GameState:
    """Get existing game state or create a new one."""
    if user_id not in game_states:
        game_states[user_id] = GameState()
    return game_states[user_id]


def generate_quiz(preferences: Dict[str, str]) -> Optional[List[Dict[str, Any]]]:
    """Generate quiz questions using OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    prompt = SYSTEM_PROMPT.format(
        era=preferences["era"], difficulty=preferences["difficulty"], genre=preferences["genre"]
    )

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Please generate the movie quiz."},
            ],
            temperature=0.8,
            max_tokens=1500,
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception:
        return None


@bt.chatbot("movie-guessing-game")
def movie_guessing_game(
    message: str, user_uuid: Optional[str] = None, conversation_uuid: Optional[str] = None
) -> List[Any]:
    """Movie guessing game chatbot."""

    user_id = user_uuid or "default"
    state = get_or_create_state(user_id)

    # Process user input
    if message.lower() in ["start", "restart", "new game"]:
        state.reset()
        state.stage = "era"
    elif message.startswith("era:"):
        state.preferences["era"] = message.replace("era:", "")
        state.stage = "difficulty"
    elif message.startswith("difficulty:"):
        if "era" not in state.preferences:
            return [Text("❌ Please start from the beginning!"), Text("Type 'start' to begin the game properly.")]
        state.preferences["difficulty"] = message.replace("difficulty:", "")
        state.stage = "genre"
    elif message.startswith("genre:"):
        if "era" not in state.preferences or "difficulty" not in state.preferences:
            return [Text("❌ Please start from the beginning!"), Text("Type 'start' to begin the game properly.")]
        state.preferences["genre"] = message.replace("genre:", "")
        state.stage = "generate"
    elif state.questions and state.stage == "question":
        if message in [opt for q in state.questions for opt in q["options"]]:
            state.last_answer = message

    # Handle game flow
    if state.stage == "start":
        state.reset()
        state.stage = "era"
        return [
            Text("🎬 Welcome to Movie Guessing Game!"),
            Text("Can you guess the movie from a hilariously bad description?"),
            Text(""),
            Text("Let's set up your game preferences..."),
            Text("🎬 What kind of movie era are you into?"),
            Pills(
                pills=[
                    Pill("All", "era:All"),
                    Pill("Classics", "era:Classics"),
                    Pill("2000s", "era:2000s"),
                    Pill("2010s", "era:2010s"),
                    Pill("Recent", "era:Recent"),
                ]
            ),
        ]

    elif state.stage == "difficulty":
        return [
            Text(f"You picked era: {state.preferences['era']}"),
            Text("🧠 Choose difficulty:"),
            Pills(
                pills=[
                    Pill("All", "difficulty:All"),
                    Pill("Easy", "difficulty:Easy"),
                    Pill("Medium", "difficulty:Medium"),
                    Pill("Hard", "difficulty:Hard"),
                ]
            ),
        ]

    elif state.stage == "genre":
        return [
            Text(f"Difficulty: {state.preferences['difficulty']}"),
            Text("🎭 Pick a genre:"),
            Pills(
                pills=[
                    Pill("All", "genre:All"),
                    Pill("Action", "genre:Action"),
                    Pill("Comedy", "genre:Comedy"),
                    Pill("Drama", "genre:Drama"),
                    Pill("Sci-Fi", "genre:Sci-Fi"),
                    Pill("Horror", "genre:Horror"),
                    Pill("Romance", "genre:Romance"),
                ]
            ),
        ]

    elif state.stage == "generate":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return [Text("❌ OpenAI API key not configured."), Text("Please set OPENAI_API_KEY in your environment.")]

        questions = generate_quiz(state.preferences)
        if not questions:
            return [Text("❌ Failed to generate quiz. Please try again.")]

        state.questions = questions
        state.index = 0
        state.score = 0
        state.stage = "question"

    # Handle game questions
    if state.stage == "question":
        components = []

        if state.last_answer is not None:
            correct_answer = state.questions[state.index - 1]["answer"]
            if state.last_answer == correct_answer:
                state.score += 1
                components.append(Text("✅ Correct!"))
            else:
                components.append(Text(f"❌ Wrong! Correct answer was: {correct_answer}"))
            state.last_answer = None

        # End of quiz
        if state.index >= len(state.questions):
            final_score = state.score
            state.stage = "complete"
            components.append(Text(f"🎬 Game Over! Final Score: {final_score}/{len(state.questions)}"))
            if final_score == len(state.questions):
                components.append(Text("🏆 Perfect Score! You're a movie genius!"))
            elif final_score >= len(state.questions) * 0.8:
                components.append(Text("🌟 Great job! You really know your movies!"))
            elif final_score >= len(state.questions) * 0.6:
                components.append(Text("👍 Good effort! Not bad at all!"))
            else:
                components.append(Text("😅 Nice try! Watch more movies!"))

            components.append(Text(""))
            components.append(Pills(pills=[Pill("🎮 Play Again", "start")]))
            return components

        # Show next question
        current_question = state.questions[state.index]
        components.append(Text(f"📽️ Question {state.index + 1}/{len(state.questions)}"))
        components.append(Text(f"Score: {state.score}/{state.index}"))
        components.append(Text(""))
        components.append(Text(current_question["question"]))
        components.append(Pills(pills=[Pill(opt, opt) for opt in current_question["options"]]))
        state.index += 1

        return components

    # Default response
    return [Text("👋 Welcome to Movie Guessing Game!"), Text("Type 'start' to begin a new game.")]


@movie_guessing_game.config
def get_config():
    return bt.BotConfig(
        name="movie-guessing-game",
        display_name="Movie Quiz Bot",
        url=os.getenv("BOT_URL", "http://localhost:5002"),
        icon_url="https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400",
        is_streaming=False,
        initial_text="🎬 Ready for a movie challenge? Type 'start' to begin the ultimate movie guessing game!",
        description="""
# Movie Guessing Game Bot 🎬

Test your movie knowledge with hilariously bad plot descriptions!

## How to Play
1. Choose your preferred movie era
2. Select difficulty level
3. Pick a genre (or all)
4. Guess 5 movies from terrible descriptions
5. Get your score!

## Features
- Multiple difficulty levels
- Various movie eras and genres
- Funny, misleading descriptions
- Score tracking
- Instant feedback

Type 'start' to begin!
        """,
        visibility="public",
    )


if __name__ == "__main__":
    bt.run_server(movie_guessing_game, port=8080, host="0.0.0.0")
