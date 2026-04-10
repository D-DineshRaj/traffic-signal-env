from env import TrafficEnv

env = TrafficEnv()

tasks = ["easy", "medium", "hard"]

for task in tasks:
    print(f"[START] task={task}", flush=True)

    state = env.reset()
    total_reward = 0

    for step in range(1, 6):
        action = "switch"
        state, reward, done = env.step(action)
        total_reward += reward

        print(f"[STEP] step={step} reward={reward}", flush=True)

    score = max(0, min(1, total_reward / 100))

    print(f"[END] task={task} score={score} steps=5", flush=True)
