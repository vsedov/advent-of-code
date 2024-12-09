import numpy as np
from numba import njit
from src.aoc.aoc2024 import YEAR, get_day
from src.aoc.aoc_helper import Aoc

def parse_disk_map(s: str) -> np.ndarray:
    d = np.fromiter((int(c) for c in s), dtype=np.int64)
    blocks = []
    fid = 0
    for i in range(len(d)):
        l = d[i]
        if i % 2 == 0:
            for _ in range(l):
                blocks.append(fid)
            fid += 1
        else:
            for _ in range(l):
                blocks.append(-1)
    return np.array(blocks, dtype=np.int64)

@njit
def compute_checksum(b):
    s = 0
    for i in range(b.size):
        if b[i] != -1:
            s += i * b[i]
    return s

@njit
def find_files(b):
    max_fid = -1
    for i in range(b.size):
        if b[i] > max_fid:
            max_fid = b[i]
    file_info = np.zeros((max_fid+1, 2), dtype=np.int64)
    for fid in range(max_fid+1):
        start = -1
        length = 0
        for i in range(b.size):
            if b[i] == fid:
                if start == -1:
                    start = i
                length += 1
        file_info[fid,0] = start
        file_info[fid,1] = length
    return file_info

@njit
def find_free_segments(b):
    segments = []
    seg_start = -1
    for i in range(b.size):
        if b[i] == -1:
            if seg_start == -1:
                seg_start = i
        else:
            if seg_start != -1:
                segments.append((seg_start, i - seg_start))
                seg_start = -1
    if seg_start != -1:
        segments.append((seg_start, b.size - seg_start))
    # Convert segments to a fixed-size array
    arr = np.zeros((len(segments), 2), dtype=np.int64)
    for i, seg in enumerate(segments):
        arr[i,0] = seg[0]
        arr[i,1] = seg[1]
    return arr

@njit
def move_file(b, fid, start, length, free_segments):
    best_idx = -1
    for i in range(free_segments.shape[0]):
        seg_start = free_segments[i,0]
        seg_len = free_segments[i,1]
        if seg_start+seg_len <= start and seg_len >= length:
            best_idx = i
            break
    if best_idx == -1:
        return False
    seg_start = free_segments[best_idx,0]
    seg_len = free_segments[best_idx,1]

    old_positions = []
    for i in range(b.size):
        if b[i] == fid:
            old_positions.append(i)
    old_positions = np.array(old_positions, dtype=np.int64)

    for i in range(length):
        b[seg_start + i] = fid
    for op in old_positions:
        b[op] = -1

    new_start = seg_start + length
    new_len = seg_len - length
    if new_len > 0:
        free_segments[best_idx,0] = new_start
        free_segments[best_idx,1] = new_len
    else:
        # remove the segment by setting length to 0
        # (no easy way to actually remove from array, just mark length as 0)
        free_segments[best_idx,1] = 0

    return True

def part_a(txt: str) -> int:
    b = parse_disk_map(txt.strip())
    @njit
    def compact_disk(b):
        while True:
            left_free = -1
            for i in range(b.size):
                if b[i] == -1:
                    left_free = i
                    break
            if left_free == -1:
                break
            has_file_right = False
            for i in range(left_free+1, b.size):
                if b[i] != -1:
                    has_file_right = True
                    break
            if not has_file_right:
                break
            right_file = -1
            for i in range(b.size-1, -1, -1):
                if b[i] != -1:
                    right_file = i
                    break
            b[left_free] = b[right_file]
            b[right_file] = -1
        return b

    b = compact_disk(b)
    return compute_checksum(b)

def part_b(txt: str) -> int:
    b = parse_disk_map(txt.strip())
    file_info = find_files(b)
    free_segments = find_free_segments(b)
    # Move files in order of decreasing file ID number
    max_fid = file_info.shape[0]-1
    for fid in range(max_fid, -1, -1):
        start = file_info[fid,0]
        length = file_info[fid,1]
        if start == -1 or length == 0:
            continue
        move_file(b, fid, start, length, free_segments)
    return compute_checksum(b)

def main(txt: str) -> None:
    print("part_a: ", part_a(txt))
    print("part_b: ", part_b(txt))

if __name__ == "__main__":
    aoc = Aoc(day=get_day(), years=YEAR)
    aoc.run(main, submit=False, part='both', readme_update=True, profile= True )

