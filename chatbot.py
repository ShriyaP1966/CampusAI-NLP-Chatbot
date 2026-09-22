import sys

from engine import predict_intent, get_response, load_engine, EngineLoadError

# Windows consoles/pipes default to cp1252, which can't encode the emoji
# below and crashes the whole CLI with UnicodeEncodeError. Force UTF-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

# -------------------------
# Chat Loop
# -------------------------

try:
    load_engine()
except EngineLoadError as exc:
    print(f"CampusAI couldn't start: {exc}")
    sys.exit(1)

print("=" * 50)
print("🎓 CampusAI - Intelligent University Assistant")
print("=" * 50)

while True:

    query = input("\nYou : ")

    if query.lower() == "exit":
        print("\nBot : Goodbye! Have a great day.")
        break

    intent, confidence = predict_intent(query)

    if intent is None:
        print("\nBot : Please type a question.")
        continue

    response, entity = get_response(intent, query)

    print("\n" + "=" * 50)

    print(f"Detected Intent : {intent}")
    print(f"Detected Entity : {entity}")
    print(f"Confidence      : {confidence:.2f}")

    print(f"\nBot : {response}")

    print("=" * 50)
