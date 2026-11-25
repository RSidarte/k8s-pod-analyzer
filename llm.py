from dotenv import load_dotenv
import anthropic

load_dotenv()                    # cette fois, on ne l'oublie pas 😉
client = anthropic.Anthropic()   # lit ANTHROPIC_API_KEY automatiquement

message = client.messages.create(
    model="claude-haiku-5-5",
    max_tokens=300,
    messages=[
        {"role": "user", "content": "Explique ce qu'est un CrashLoopBackOff en 3 phrases."}
    ],
)

print(message.content[0].text)
print(message.usage)