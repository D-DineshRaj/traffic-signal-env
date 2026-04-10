import os
from env import TrafficEnv
from openai import OpenAI

# ✅ MUST use their proxy
client = OpenAI(
    base_url=os.environ.get("API_BASE_URL"),
    api_key=os.environ.get("API_KEY")
)

env = TrafficEnv()
tasks = ["easy", "medium", "hard"]

for task in tasks:
    print(f"[START] task={task}", flush=True)

    state = env.reset()   # ✅ FIXED
    total_reward = 0

    for step in range(10):
        try:
            # ✅ REQUIRED API CALL
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You control a traffic signal."},
                    {"role": "user", "content": f"Left: {state.get('cars_left',0)}, Right: {state.get('cars_right',0)}. Action?"}
                ]
            )

            decision = response.choices[0].message.content.lower()

            if "switch" in decision:
                action = "switch"
            else:
                action = "stay"

        except Exception:
            # ✅ fallback (prevents crash)
            left = state.get("cars_left", 0)
            right = state.get("cars_right", 0)
            action = "switch" if left > right else "stay"

        state, reward, done = env.step(action)
        total_reward += reward

        print(f"[STEP] step={step+1} reward={reward}", flush=True)

        if done:
            break

    score = max(0, min(1, total_reward / 100))

    print(f"[END] task={task} score={score} steps={step+1}", flush=True)
