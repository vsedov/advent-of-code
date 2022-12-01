def question_01_part_a():
    def part_a():
        container = []
        for x in txt.split("\n\n"):
            data = x.split()
            data = list(map(int, data))
            container.append(sum(data))
        return max(container)
