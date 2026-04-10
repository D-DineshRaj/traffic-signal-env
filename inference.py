from env import TrafficEnv

env = TrafficEnv()

tasks = ["easy", "medium", "hard"]

for task in tasks:
    print(f"[START] task={task}", flush=True)

    state = env.reset(task)
    total_reward = 0

    for step in range(20):
        left = state.get("cars_left", 0)
        right = state.get("cars_right", 0)

        # 🔥 SMART LOGIC
        diff = left - right

        if diff > 3:
            action = "switch"
        elif diff < -3:
            action = "switch"
        else:
            action = "stay"

        state, reward, done = env.step(action)
        total_reward += reward

        print(f"[STEP] step={step+1} reward={reward}", flush=True)

        if done:
            break

    score = max(0, min(1, total_reward / 100))

    print(f"[END] task={task} score={score} steps={step+1}", flush=True)
