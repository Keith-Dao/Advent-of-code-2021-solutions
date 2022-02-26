from __future__ import annotations

filename: str = "day23.txt"

from typing import Generator
from heapq import heapify, heappop, heappush


class Amphipod:
    def __init__(self, type_id: str):
        self.target_room: int = ord(type_id) - ord("A")
        self.cost = 10**self.target_room

    @staticmethod
    def cost_from_room(target_room: int) -> int:
        return 10**target_room

    def __str__(self) -> str:
        return chr(self.target_room + ord("A"))

    def __repr__(self) -> str:
        return str(self)


class State:
    def __init__(
        self,
        cost: int = 0,
        rooms: list[list[Amphipod | None]] | None = None,
        hallway: list[Amphipod | None] | None = None,
        swaps: tuple[int, int, int] | None = None,
        part_2: bool = False,
    ):
        self.rooms: list[list[Amphipod | None]] = rooms or [
            [] for _ in range(4)
        ]
        self.hallway: list[Amphipod | None] = hallway or []

        if rooms is None and hallway is None:
            with open(filename, "r") as text:
                text.readline()  # First line

                # Hallway
                self.hallway = [None] * (len(text.readline().strip()) - 2)

                # Rooms
                def populateRoom(line: str):
                    room_num: int = 0
                    for c in line:
                        if c not in "ABCD":
                            continue

                        self.rooms[room_num].append(Amphipod(c))
                        room_num += 1

                populateRoom(text.readline().strip())
                if part_2:
                    populateRoom("DCBA")
                    populateRoom("DBAC")
                populateRoom(text.readline().strip())

        if swaps is not None:
            self.swap_room_hallway(*swaps)

        self.cost: int = cost
        self.total_cost: int = cost + self.heuristic_cost()

    def is_final(self) -> bool:

        for target_room, room in enumerate(self.rooms):
            for amphipod in room:
                if amphipod is None or amphipod.target_room != target_room:
                    return False

        return True

    def is_room_enterable_by_matching(self, target_room: int) -> bool:
        for amp in self.rooms[target_room]:
            if amp is not None and amp.target_room != target_room:
                return False
        return True

    def is_room_exitable(self, target_room: int) -> bool:
        return not self.is_room_enterable_by_matching(target_room)

    def get_room_x(self, target_room: int) -> int:
        return 2 + 2 * target_room

    def is_pos_above_room(self, x: int) -> bool:
        return 2 <= x <= 8 and x % 2 == 0

    def is_hallway_clear(self, x1: int, x2: int) -> bool:
        if x1 == x2:
            return True
        if x1 < x2:
            start, stop = x1 + 1, x2
        else:
            start, stop = x2, x1

        for i in range(start, stop):
            if self.hallway[i] is not None:
                return False
        return True

    def empty_hallway_positions(self, x: int) -> Generator[int, None, None]:
        for i in range(x - 1, -1, -1):
            if self.is_pos_above_room(i):
                continue

            if self.hallway[i] is None:
                yield i
            else:
                break

        for i in range(x + 1, len(self.hallway)):
            if self.is_pos_above_room(i):
                continue

            if self.hallway[i] is None:
                yield i
            else:
                break

    def get_top_in_room(self, target_room: int) -> tuple[int, Amphipod | None]:
        for i, amp in enumerate(self.rooms[target_room]):
            if amp is not None:
                return i, amp

        return (-1, None)

    def get_space_in_room(self, target_room: int) -> int:
        for i in range(len(self.rooms[target_room]) - 1, -1, -1):
            if self.rooms[target_room][i] is None:
                return i
        return -1

    def clone(self, additional_cost: int = 0) -> State:
        return State(
            self.cost + additional_cost,
            [[amp for amp in room] for room in self.rooms],
            [amp for amp in self.hallway],
            # prev=self,
        )

    def swap_room_hallway(
        self, target_room: int, room_depth: int, hallway: int
    ) -> None:
        self.rooms[target_room][room_depth], self.hallway[hallway] = (
            self.hallway[hallway],
            self.rooms[target_room][room_depth],
        )

    def heuristic_cost(self) -> int:
        # Cost of amphipods exiting their rooms to get to their target rooms
        exit_room_cost: int = 0
        for room_i, room in enumerate(self.rooms):
            skip: bool = True
            current_x: int = self.get_room_x(room_i)
            for room_depth in range(len(room) - 1, -1, -1):
                amp: Amphipod | None = room[room_depth]
                if amp is None or (skip and amp.target_room == room_i):
                    continue

                # Stop skipping
                skip = False
                target_x: int = self.get_room_x(amp.target_room)

                # Steps to move out of the room
                # 2 steps to moving out of the way if the amphipod is in the correct room
                # or steps to move to the correct room
                steps: int = room_depth + 1 + max(abs(target_x - current_x), 2)
                exit_room_cost += steps * amp.cost

        # Cost of amphipods moving from the hallway to space above the target room
        hallway_cost: int = 0
        for current_x, amp in enumerate(self.hallway):
            if amp is None:
                continue

            target_x: int = self.get_room_x(amp.target_room)

            steps: int = abs(target_x - current_x)
            hallway_cost += steps * amp.cost

        # Cost of amphipods moving into the room
        enter_room_cost: int = 0
        for target_room, room in enumerate(self.rooms):
            skip: bool = True
            for room_depth in range(len(room) - 1, -1, -1):
                amp: Amphipod | None = room[room_depth]
                if (
                    skip and amp is not None and amp.target_room == target_room
                ):  # Skip depth if the amphipod is in the right room
                    continue

                skip = False
                steps: int = room_depth + 1
                enter_room_cost += steps * Amphipod.cost_from_room(target_room)

        return exit_room_cost + hallway_cost + enter_room_cost

    def create_new_state(
        self,
        target_room: int,
        room_depth: int,
        current_x: int,
        target_x: int,
        amp: Amphipod,
    ) -> State:
        steps: int = 1 + room_depth + abs(current_x - target_x)
        energy: int = steps * amp.cost

        return State(
            self.cost + energy,
            [[amp for amp in room] for room in self.rooms],
            [amp for amp in self.hallway],
            swaps=(target_room, room_depth, target_x),
        )

    def get_next_move(self) -> Generator[State, None, None]:
        # Room to hallway transitions
        for target_room in range(len(self.rooms)):
            if not self.is_room_exitable(target_room):
                continue

            room_depth, amp = self.get_top_in_room(target_room)
            if amp is None:
                continue
            current_x: int = self.get_room_x(target_room)

            for target_x in self.empty_hallway_positions(current_x):
                yield self.create_new_state(
                    target_room, room_depth, current_x, target_x, amp
                )

        # Hallway to room transitions
        for current_x, amp in enumerate(self.hallway):
            if amp is None:
                continue

            target_room: int = amp.target_room
            if not self.is_room_enterable_by_matching(target_room):
                continue  # Room cannot be entered

            target_x: int = self.get_room_x(target_room)
            if not self.is_hallway_clear(current_x, target_x):
                continue  # Hallway blocked

            room_depth: int = self.get_space_in_room(target_room)

            yield self.create_new_state(
                target_room, room_depth, target_x, current_x, amp
            )

    def __lt__(self, other: State) -> bool:
        return self.total_cost < other.total_cost

    def __hash__(self) -> int:
        def encode(amp: Amphipod | None) -> int:
            if amp is None:
                return 0
            return amp.target_room + 1

        hashcode: int = 0
        for room in self.rooms:
            for amp in room:
                hashcode = hashcode * 5 + encode(amp)
        for amp in self.hallway:
            hashcode = hashcode * 5 + encode(amp)

        return hashcode

    def __eq__(self, other: object) -> bool:
        return hash(self) == hash(other)

    def __str__(self) -> str:

        string: str = "#" * (len(self.hallway) + 2)
        string += "\n"

        # Hallway
        string += "#"
        for amp in self.hallway:
            if amp is None:
                string += "."
            else:
                string += str(amp)
        string += "#\n"

        # Rooms
        for i in range((n := len(self.rooms[0])) + 1):
            # Start
            if i == 0:
                string += "###"
            else:
                string += "  #"

            # Rooms
            for j in range(len(self.rooms)):
                if i < n:
                    amp: Amphipod | None = self.rooms[j][i]
                    string += f"{'.' if amp is None else amp}#"
                else:
                    string += "##"

            # End
            if i == 0:
                string += "##\n"
            else:
                string += "  \n"

        return string


def solve(initial_state: State):

    queue: list[State] = [initial_state]
    visited: dict[State, int] = {initial_state: 0}
    heapify(queue)

    while len(queue) != 0:
        current_state: State = heappop(queue)

        if current_state.is_final():
            return current_state.total_cost

        for next_state in current_state.get_next_move():
            if (
                next_state in visited
                and next_state.total_cost >= visited[next_state]
            ):
                continue

            heappush(queue, next_state)
            visited[next_state] = next_state.total_cost

    raise AssertionError("Unsolvable.")


def part1():
    print("Part 1")

    print(solve(State()))


def part2():
    print("Part 2")

    print(solve(State(part_2=True)))


if __name__ == "__main__":
    print("Day 23")
    part1()
    print("---")
    part2()
