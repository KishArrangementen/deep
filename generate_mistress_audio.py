import os
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise ValueError("Please set ELEVENLABS_API_KEY in your .env file")

client = ElevenLabs(api_key=API_KEY)

# The three voices
VOICES = {
    "domi": "AZnzlk1XvdvUeBnXmlld",
    "charlotte": "XB0fDUnXU5powFXDhCwa",
    "rachel": "21m00Tcm4TlvDq8ikWAM",
}

# All lines (you can add more later)
LINES = [
    # 1. Setup
    "Look at me. Listen carefully.",
    "Lube that toy up… nice and slow… then slide it into your ass for me.",
    "Good boy.",
    "Now put it in. Don’t make me wait.",
    "Mmm… good. Thank you for taking my toy like a good boy.",
    "You’re welcome.",

    # 2. Expectations
    "You’re going to deepthroat that cock for me. Every time your nose hits the button you get rewarded. The longer you stay down, the harder I make the toy in your ass vibrate. If you choke, I want to hear it. If you pull off too early… no reward. And you’ll slap that ass until I say you’ve had enough. Only good performance earns the right to cum. Understand?",
    "Good. Begin when you’re ready.",

    # 3. Training
    "On it.",
    "Deeper… yes, just like that.",
    "Hold it. Stay right there.",
    "Five… four… three… two… one… stay.",
    "Don’t you dare pull off until I say.",
    "Choke on it for me… let me hear that pretty sound.",
    "Mmm, good boy. That’s better.",
    "Again. Deeper this time.",
    "You’re doing so well for me… keep going.",
    "Stay down. Feel how hard it’s buzzing for you.",
    "That’s it… take it all.",
    "Deeper.",
    "Hold.",
    "Stay.",

    # 4. Success
    "There it is… feel that? That’s yours.",
    "Good boy… you earned that vibration.",
    "Stay right there and enjoy it.",
    "Mmm, look at you taking it so well.",
    "That’s my good boy.",
    "Nice… keep it there.",

    # 5. Stroking permission
    "Good boy… you earned it. Stroke that cock for me.",
    "You can stroke it now. Ten seconds.",
    "Hands on it. Stroke slowly… enjoy it.",
    "That’s it… stroke for me while it buzzes in your ass.",
    "Nice and slow.",
    "Faster… just a little.",
    "Don’t you dare cum yet.",
    "Five… four… three… two… one…",
    "Hands off. Now.",
    "Back on that cock. Show me you still deserve more.",
    "Good. Now earn the next one.",

    # 6. Failure
    "I didn’t say you could pull off.",
    "No. That’s not good enough.",
    "No reward for that.",
    "You failed me.",

    # 7. Slap punishment
    "Slap your ass. Five times. Hard. I want to hear it.",
    "Harder.",
    "Again.",
    "Don’t make me wait.",
    "Good. That’s enough.",
    "Now get back on that cock and do it properly.",
    "Don’t fail me again.",

    # 8. Progress reminders
    "You’re not ready to cum yet.",
    "Keep earning it.",
    "I decide when you get to finish.",
    "More. Show me you deserve it.",
    "That wasn’t good enough. Keep going.",
    "You want to cum? Then stay down longer.",
    "Earn it, good boy.",
    "You’re getting closer…",
    "Almost there. Keep going.",
    "A few more good holds and you might earn it.",
    "You’re close now. Don’t mess it up.",
    "One more long one… then maybe I’ll let you cum.",
    "You’re doing better. Keep it up.",
    "You’re right on the edge of earning it.",
    "So close. Stay focused.",
    "Don’t fail me now… you’re nearly there.",

    # 9. Ending
    "You’ve been good enough… for now.",
    "Alright. You’ve earned it.",
    "Stay down on that cock. Don’t you dare pull off.",
    "Stroke that cock for me. Harder.",
    "Choke on it while you jerk off. I want to hear you struggle.",
    "That’s it… deeper. Keep stroking.",
    "Don’t stop. You’re going to cum with my cock in your throat.",
    "Good boy… choke on it. Let me hear it.",
    "Faster. You’re so close, aren’t you?",
    "Stay down. Cum for me.",
    "Yes… cum. Cum with it buried in your throat.",
    "Good boy… make a mess for me.",
    "That’s it… take it. Cum.",

    # 10. Aftercare
    "Mmm… look at you. Such a good boy.",
    "Breathe. You did so well for me.",
    "Clean yourself up.",
    "I’m proud of you… for now.",
    "We’ll do this again soon.",
]

def safe_filename(text: str) -> str:
    """Create a clean filename from the line."""
    name = text.lower().strip()
    name = "".join(c if c.isalnum() or c in " -_" else "" for c in name)
    name = name.replace(" ", "_")[:60]
    return name or "line"

def main():
    output_dir = Path("audio")
    output_dir.mkdir(exist_ok=True)

    for voice_name, voice_id in VOICES.items():
        voice_dir = output_dir / voice_name
        voice_dir.mkdir(exist_ok=True)
        print(f"\n=== Generating for {voice_name} ===")

        for i, text in enumerate(LINES, 1):
            filename = f"{i:03d}_{safe_filename(text)}.mp3"
            filepath = voice_dir / filename

            if filepath.exists():
                print(f"  Skipping (already exists): {filename}")
                continue

            print(f"  [{i}/{len(LINES)}] {text[:50]}...")

            try:
                audio = client.text_to_speech.convert(
                    text=text,
                    voice_id=voice_id,
                    model_id="eleven_multilingual_v2",
                    output_format="mp3_44100_128",
                )
                save(audio, str(filepath))
            except Exception as e:
                print(f"  ERROR on line {i}: {e}")

    print("\nDone! All audio files are in the /audio folder.")

if __name__ == "__main__":
    main()