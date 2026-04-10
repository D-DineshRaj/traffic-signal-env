import os
from env import TrafficEnv
from openai import OpenAI

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

    for step in range(15):
        left = state.get("cars_left", 0)
        right = state.get("cars_right", 0)

        try:
            # ✅ ALWAYS CALL LLM (important)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You control traffic efficiently."},
                    {"role": "user", "content": f"Left: {left}, Right: {right}. Best action?"}
                ]
            )

            decision = response.choices[0].message.content.lower()

            # 🔥 HYBRID LOGIC (BEST)
            if abs(left - right) > 3:
                action = "switch" if left > right else "stay"
            else:
                if "switch" in decision:
                    action = "switch"
                else:
                    action = "stay"

        except Exception:
            action = "switch" if left > right else "stay"

        state, reward, done = env.step(action)
        total_reward += reward

        print(f"[STEP] step={step+1} reward={reward}", flush=True)

        if done:
            break

    score = total_reward / 100
    score = max(0.01, min(0.99, score))

    print(f"[END] task={task} score={score} steps={step+1}", flush=True)
