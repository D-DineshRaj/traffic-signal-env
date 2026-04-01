from fastapi import FastAPI
from env import TrafficEnv

app = FastAPI()

env = TrafficEnv()

@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {"id": "easy", "desc": "Reduce cars below 20"},
            {"id": "medium", "desc": "Balance both lanes"},
            {"id": "hard", "desc": "Optimize long traffic"}
        ]
    }

@app.get("/baseline")
def run_baseline():
    state = env.reset()
    total_reward = 0

    for _ in range(10):
        action = "switch"
        state, reward, done = env.step(action)
        total_reward += reward

    return {
        "final_state": state,
        "score": total_reward
    }

@app.get("/grader")
def grader():
    state = env.reset()
    total_reward = 0

    for _ in range(10):
        action = "switch"
        state, reward, done = env.step(action)
        total_reward += reward

    score = max(0, min(1, total_reward / 100))

    return {"grade": score}