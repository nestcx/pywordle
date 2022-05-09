from collections import Counter

class SolveTracker():

    def __init__(self, turn_limit):
        self.turn_limit = turn_limit
        self.wins = 0
        self.losses = 0
        self.turn_no_history = []
        self.loss_answers = []


    def submit(self, finished_game):

        if finished_game.state == "win":
            self.wins += 1
        if finished_game.state == "loss":
            self.losses += 1
            self.loss_answers.append(finished_game.answer)

        self.turn_no_history.append(finished_game.turn_no - 1)


    def _get_distribution(self):
        c = Counter(self.turn_no_history)

        pc = {}
        for i in range(1, self.turn_limit + 1):
            pc[i] = int((c[i] / len(self.turn_no_history)) * 100)

        return c, pc


    def _vis_dist(self, c, pc):

        output = ''

        for i in range(1, 7):

            if i % 2 == 0:
                output += f'{i}: \033[48;5;245m'
            else:
                output += f'{i}: \033[48;5;250m'

            for x in range(pc[i]):
                output += ' '

            output += f'\033[0m{c[i]}\n'
        
        output += f'X: {len(self.loss_answers)}\n'

        return f'{output}\033[0m'


    def get_stats(self):
        data = {}
        data["win_rate"] = f'{self.wins} / {(self.wins + self.losses)}'
        data["avg_turns"] = (sum(self.turn_no_history) / len(self.turn_no_history))
        data["total_turns"] = sum(self.turn_no_history)
        data["turn_distribution"] = self._get_distribution()[0]
        data["loss_answers"] = self.loss_answers
        return data


    def get_graph(self):
        dist = self._get_distribution()
        return self._vis_dist(dist[0], dist[1])