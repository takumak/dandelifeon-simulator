import numpy as np
import random
import functools
import argparse

killzone = set([
    286, 287, 288,
    311, 312, 313,
    336, 337, 338,
])

evolvezone = list(set(range(25*25)) - killzone)

class Layout:
    K = 20

    def __init__(self, init_layout):
        self.init_layout = init_layout
        self.current = init_layout.copy()

    def cost(self):
        return np.count_nonzero(self.init_layout)

    def evolve(self):
        newlayout = self.init_layout.copy()
        for i in random.sample(evolvezone, self.K):
            y = i // 25
            x = i % 25
            newlayout[y,x] = 0 if self.init_layout[y,x] else 1
        return Layout(newlayout)

    def _to_bytes(self, layout):
        cells = list(layout.flatten())
        data = []
        for i in range(79):
            chunk = cells[i*8:i*8+8]
            b = int(''.join(['1' if b else '0' for b in chunk]), 2)
            data.append(b)
        return bytes(data)

    def _to_hex(self, layout):
        return self._to_bytes(layout).hex()

    def to_bytes(self):
        return self._to_bytes(self.init_layout)

    def to_hex(self):
        return self._to_hex(self.init_layout)

    def current_bytes(self):
        return self._to_bytes(self.current)

    def _graph(self, layout):
        hr = '+' + ('-' * 25) + '+'
        r = [hr]
        for y in range(25):
            c = 'o' if y in range(11, 14) else '*'
            line = ''
            for x in range(25):
                m = c if x in range(11, 14) else '*'
                if not layout[y, x]:
                    m = ' '
                line += m
            r.append(f'|{line}|')
        r.append(hr)
        return '\n'.join(r)

    def graph_init(self):
        return self._graph(self.init_layout)

    def graph_current(self):
        return self._graph(self.current)

    def graph_both(self):
        a = self.graph_init().split('\n')
        b = self.graph_current().split('\n')
        return '\n'.join([f'{a} {b}' for a, b in zip(a, b)])

    @classmethod
    def from_bytes(cls, data):
        cells = []
        for y in range(25):
            row = []
            for x in range(25):
                i = y * 25 + x
                bit = (data[i//8] >> (7 - (i%8))) & 1
                row.append(bit)
            cells.append(row)
        return cls(np.array(cells))

    @classmethod
    def from_hex(cls, text):
        return cls.from_bytes(bytes.fromhex(text))

    @classmethod
    def zeros(cls):
        return cls(np.zeros((25, 25)))

    def _shifted(self, m, y, x):
        r = np.roll(m, (y, x), (0, 1))

        if y < 0:
            r[y:] = 0
        else:
            r[0:y] = 0

        if x < 0:
            r[:,x:] = 0
        else:
            r[:,0:x] = 0

        return r

    def shifted(self, y, x):
        return self._shifted(self.current, y, x)

    def nextgen(self):
        ages = np.zeros((8, 25, 25))
        ages[0,:,:] = self.shifted(-1, -1)
        ages[1,:,:] = self.shifted(-1,  0)
        ages[2,:,:] = self.shifted(-1,  1)
        ages[3,:,:] = self.shifted( 0, -1)
        ages[4,:,:] = self.shifted( 0,  1)
        ages[5,:,:] = self.shifted( 1, -1)
        ages[6,:,:] = self.shifted( 1,  0)
        ages[7,:,:] = self.shifted( 1,  1)

        counts = np.count_nonzero(ages, 0)

        for y in range(25):
            for x in range(25):
                age = self.current[y,x]
                cnt = counts[y,x]
                if age > 0:
                    if cnt <= 1:
                        age = 0
                    elif cnt <= 3:
                        age = min(age + 1, 101)
                    else:
                        age = 0
                else:
                    if cnt == 3:
                        age = max(ages[:,y,x])
                self.current[y,x] = age

    def centerzone(self):
        return self.current[11:14,11:14]

    def isend(self):
        return np.count_nonzero(self.centerzone()) > 0

    def run(self):
        history = set()

        self.current = self.init_layout.copy()
        self.mana = 0
        self.score = 0
        self.cycle = 0

        g = 0
        while True:
            h = self.current_bytes()
            if h in history:
                return False
            history.add(h)

            if self.isend():
                absorbed = self.centerzone()
                self.mana = np.sum(absorbed * 60) - (np.count_nonzero(absorbed) * 60)
                self.score = self.mana - (self.cost() * 10)
                self.cycle = g
                return True

            self.nextgen()
            g += 1

    def summary(self):
        return f'score={self.score} mana={self.mana} cycle={self.cycle} cost={self.cost()}'

def optimize(layout):
    # optimize
    while True:
        ones_y, ones_x = np.where(layout.init_layout == 1)
        improved = False
        for y, x in zip(ones_y, ones_x):
            new_layout = layout.init_layout.copy()
            new_layout[y, x] = 0
            new_layout = Layout(new_layout)
            if not new_layout.run():
                continue
            if new_layout.score > layout.score:
                # print(f'optimize: mana=[{layout.mana} => {new_layout.mana}] cost=[{layout.cost()} => {new_layout.cost()}]')
                layout = new_layout
                improved = True
                break
        if not improved:
            break
    return layout

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', metavar='K', type=int, default=20)
    parser.add_argument('--init', metavar='INIT_LAYOUT')
    args = parser.parse_args()
    Layout.K = args.k

    random.seed()

    layout = Layout.zeros()

    if args.init:
        layout = Layout.from_hex(args.init)

    # 18000
    # layout = Layout.from_hex('00000020000014000000000002000000000000080001000000ae000001000010400000000000000001000000001001400000800600000a000002000000000000400000200000240000020000000000')

    layout.run()
    print(layout.graph_both())
    print(f'gen0: {layout.summary()}')

    for i in range(10):
        children = []
        for j in range(500):
            c = layout.evolve()
            c.run()
            children.append(c)

        best = sorted(children, key=lambda c: c.score)[-1]
        if best.score > layout.score:
            best = optimize(best)
            print(f'gen{i+1}: {best.summary()}')
            print(f'{best.to_hex()}')
            layout = best
        else:
            print(f'gen{i+1}: *skip*')

    layout.run()
    print(layout.graph_both())
    print(layout.summary())

if __name__ == '__main__':
    main()
