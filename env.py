class TrafficEnv:
    def __init__(self):
        self.lane1 = 10
        self.lane2 = 5
        self.signal = "lane1"

    def reset(self):
        self.lane1 = 10
        self.lane2 = 5
        self.signal = "lane1"
        return self.state()

    def state(self):
        return {
            "lane1": self.lane1,
            "lane2": self.lane2,
            "signal": self.signal
        }

    def step(self, action):
        if action == "switch":
            self.signal = "lane2" if self.signal == "lane1" else "lane1"

        if self.signal == "lane1":
            self.lane1 = max(0, self.lane1 - 3)
        else:
            self.lane2 = max(0, self.lane2 - 3)

        self.lane1 += 2
        self.lane2 += 2

        total_wait = self.lane1 + self.lane2
        reward = -total_wait

        if action == "switch":
            reward -= 1

        done = False

        return self.state(), reward, done


# THIS MUST BE AT BOTTOM (IMPORTANT)
if __name__ == "__main__":
    env = TrafficEnv()

    print("Reset:", env.reset())

    state, reward, done = env.step("switch")
    print("After step:", state)
    print("Reward:", reward)