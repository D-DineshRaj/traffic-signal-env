import os
from env import TrafficEnv
from openai import OpenAI

# ✅ LLM client using hackathon proxy
client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY")
)

env = TrafficEnv()
tasks = ["easy", "medium", "hard"]

for task in tasks:
    print(f"[START] task={task}", flush=True)

    state = env.reset()
    total_reward = 0

    for step in range(10):
        try:
            # ✅ REQUIRED API CALL (LLM proxy)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You control a traffic signal."},
                    {"role": "user", "content": f"Cars left: {state.get('cars_left',0)}, Cars right: {state.get('cars_right',0)}. Should I switch or stay?"}
                ]
            )

            decision = response.choices[0].message.content.lower()

            if "switch" in decision:
                action = "switch"
            else:
                action = "stay"

        except Exception:
            # ✅ fallback logic (prevents crash)
            left = state.get("cars_left", 0)
            right = state.get("cars_right", 0)
            action = "switch" if left > right else "stay"

        state, reward, done = env.step(action)
        total_reward += reward

        print(f"[STEP] step={step+1} reward={reward}", flush=True)

        if done:
            break

    # ✅ FIX score range (strictly between 0 and 1)
    score = total_reward / 100
    score = max(0.01, min(0.99, score))

    # ✅ ALWAYS print END
    print(f"[END] task={task} score={score} steps={step+1}", flush=True)
