"""
Movie Guessing Game Bot
"""
import os
import json
import openai
from bubbletea_chat import bt
from bubbletea_chat.components import Pill, Pills, Text
from dotenv import load_dotenv

load_dotenv()

# Print OPENAI_API_KEY from .env file
openai_api_key = os.getenv('OPENAI_API_KEY')

# Store game states by user session
game_states = {}

# Prompt template for GPT
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

    def __init__(self):
        self.reset()

    def reset(self):
        self.stage = "start"
        self.preferences = {}
        self.questions = []
        self.index = 0
        self.score = 0
        self.last_answer = None


@bt.chatbot("movie-guessing-game")
def movie_guessing_game(message: str,
              user_uuid: str = None,
              conversation_uuid: str = None) -> list:
    session_id = conversation_uuid or user_uuid or "default"

    # Initialize game state
    if message == "start":
        game_states[session_id] = GameState()
    if session_id not in game_states:
        game_states[session_id] = GameState()
    state = game_states[session_id]

    # Handle pill clicks
    if message.startswith("era:"):
        state.preferences["era"] = message.replace("era:", "")
        state.stage = "difficulty"
    elif message.startswith("difficulty:"):
        # Check if era is set
        if "era" not in state.preferences:
            return [
                Text("❌ Please start from the beginning!"),
                Text("Type 'start' to begin the game properly.")
            ]
        state.preferences["difficulty"] = message.replace("difficulty:", "")
        state.stage = "genre"
    elif message.startswith("genre:"):
        # Check if previous preferences are set
        if "era" not in state.preferences or "difficulty" not in state.preferences:
            return [
                Text("❌ Please start from the beginning!"),
                Text("Type 'start' to begin the game properly.")
            ]
        state.preferences["genre"] = message.replace("genre:", "")
        state.stage = "generate"
    elif state.questions and state.stage == "question" and message in [
            opt for q in state.questions for opt in q["options"]
    ]:
        state.last_answer = message

    # Start game flow
    if state.stage == "start":
        state.reset()
        state.stage = "era"
        return [
            Text("🎬 What kind of movie era are you into?"),
            Pills(pills=[
                Pill("All", "era:All"),
                Pill("Classics", "era:Classics"),
                Pill("2000s", "era:2000s"),
                Pill("2010s", "era:2010s"),
                Pill("Recent", "era:Recent")
            ])
        ]

    elif state.stage == "difficulty":
        return [
            Text(f"You picked era: {state.preferences['era']}"),
            Text("🧠 Choose difficulty:"),
            Pills(pills=[
                Pill("All", "difficulty:All"),
                Pill("Easy", "difficulty:Easy"),
                Pill("Medium", "difficulty:Medium"),
                Pill("Hard", "difficulty:Hard")
            ])
        ]

    elif state.stage == "genre":
        return [
            Text(f"Difficulty: {state.preferences['difficulty']}"),
            Text("🎭 Pick a genre:"),
            Pills(pills=[
                Pill("All", "genre:All"),
                Pill("Action", "genre:Action"),
                Pill("Comedy", "genre:Comedy"),
                Pill("Drama", "genre:Drama"),
                Pill("Sci-Fi", "genre:Sci-Fi"),
                Pill("Horror", "genre:Horror"),
                Pill("Romance", "genre:Romance")
            ])
        ]

    elif state.stage == "generate":
        prompt = SYSTEM_PROMPT.format(
            era=state.preferences["era"],
            difficulty=state.preferences["difficulty"],
            genre=state.preferences["genre"])
        try:
            client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": prompt
                }, {
                    "role": "user",
                    "content": "Please generate the movie quiz."
                }],
                temperature=0.8,
                max_tokens=1500,
            )
            content = response.choices[0].message.content
            state.questions = json.loads(content)
            state.index = 0
            state.score = 0
            state.stage = "question"
        except Exception:
            return [Text("❌ Failed to generate quiz. Please try again.")]

    # Handle game questions
    if state.stage == "question":
        components = []

        if state.last_answer is not None:
            correct_answer = state.questions[state.index - 1]["answer"]
            if state.last_answer == correct_answer:
                state.score += 1
                components.append(Text("✅ Correct!"))
            else:
                components.append(
                    Text(f"❌ Wrong! Correct answer was: {correct_answer}"))
            state.last_answer = None

        # End of quiz
        if state.index >= len(state.questions):
            final_score = state.score
            state.stage = "complete"
            components.append(
                Text(f"🏁 Game Over! You scored {final_score}/5 🎉"))
            components.append(Text("Type 'start' to play again!"))
            return components

        # Ask next question
        q = state.questions[state.index]
        state.index += 1

        components.append(Text(f"🎲 Q{state.index}: {q['question']}"))
        components.append(Pills(pills=[Pill(opt, opt)
                                       for opt in q["options"]]))
        return components

    # Final screen
    if state.stage == "complete":
        return [Text("Type 'start' to play again!")]

    return [Text("Type 'start' to begin the Movie Guessing Game! 🎬")]


@movie_guessing_game.config
def get_config():
    return bt.BotConfig(
        name="movie-guessing-game",
        display_name="Movie Guessing Game",
        url="http://localhost:5000",
        icon_url=
        "https://iafqwfegdftjthhbccyt.supabase.co/storage/v1/object/sign/bubble-tea/movie_bot.jpg?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV81MDMyMzM5NS1hZDExLTRkYzEtODdkNC0yMjMwM2JkNjBhMzEiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJidWJibGUtdGVhL21vdmllX2JvdC5qcGciLCJpYXQiOjE3NTQwNTI5OTEsImV4cCI6MTc4NTU4ODk5MX0.d9C45AOhstuj0ZJF6TbDjxJY-TauZZkdfZs8toasrbI",
        is_streaming=False,
        initial_text=
        "🎬 Welcome to the Movie Guessing Game! I'll describe movie plots badly, and you try to guess the movie! Type 'start' to begin!",
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
