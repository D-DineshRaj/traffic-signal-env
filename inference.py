from env import TrafficEnv

def run():
    env = TrafficEnv()
    state = env.reset()

    total_reward = 0

    for step in range(10):
        # simple logic: always switch
        action = "switch"

        state, reward, done = env.step(action)
        total_reward += reward

    print("Final State:", state)
    print("Total Reward:", total_reward)


if __name__ == "__main__":
    run()