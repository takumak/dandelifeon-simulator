import sys
import os
import tempfile
import subprocess
import argparse

def graph(text):
    data = bytes.fromhex(text)
    layout = []
    for y in range(25):
        row = []
        for x in range(25):
            i = y * 25 + x
            bit = (data[i//8] >> (7 - (i%8))) & 1
            row.append(bit)
        layout.append(row)

    hr = '+' + ('-' * 25) + '+'
    r = [hr]
    for y, row in enumerate(layout):
        c = 'o' if y in range(11, 14) else '*'
        line = ''
        for x, cell in enumerate(row):
            m = c if x in range(11, 14) else '*'
            if not cell:
                m = ' '
            line += m
        r.append(f'|{line}|')
    r.append(hr)
    return '\n'.join(r)

def graph_parse(g):
    lines = g.strip().split('\n')[1:-1]
    binary = []
    for l in lines:
        binary += [{' ': '0', '*': '1'}[c] for c in l.strip('|')]
    binary += ['0'] * 8

    data = ''
    for i in range(79):
        octal = ''.join(binary[i*8:i*8+8])
        data += bytes([int(octal, 2)]).hex()
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data')
    args = parser.parse_args()

    EDITOR = os.environ.get('EDITOR', 'vim')

    with tempfile.NamedTemporaryFile(suffix='.txt', mode='w+') as f:
        filename = f.name
        f.write(graph(args.data))
        f.flush()

        subprocess.call([EDITOR, filename])

        f.seek(0)
        print(graph_parse(f.read()))

if __name__ == '__main__':
    main()

