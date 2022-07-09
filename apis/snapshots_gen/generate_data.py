# 0x811a7c9334966401C22B79a55B6aCE749004D543
# 0xd21682098B868B71e1c26754B4d8dc1d8Ce19700
# 0x63412cA517c1EeA44BCaa2B93332f3c39e72277b

from pathlib import Path


def read_from_files(file_name):
    with open(file_name, "r") as f:
        return f.read()


def create_new_files(data, month, from_date, to):
    for i in range(from_date, to+1):
        Path(f"./data/month-{month}").mkdir(parents=True, exist_ok=True)
        with open(f"./data/month-{month}/snapshot_Doodles_2022-0{month}-{i}.txt", "w") as f:
            f.write(data)


data = read_from_files("./data/snapshot_Doodles_20220701.txt")

create_new_files(data, 5, 1, 15)

data = read_from_files("./data/snapshot_Doodles_20220702.txt")
create_new_files(data, 5, 16, 23)

data = read_from_files("./data/snapshot_Doodles_20220703.txt")
create_new_files(data, 5, 24, 31)
create_new_files(data, 6, 1, 10)


data = read_from_files("./data/snapshot_Doodles_20220704.txt")
create_new_files(data, 6, 11, 24)
create_new_files(data, 6, 25, 29)

data = read_from_files("./data/snapshot_Doodles_20220705.txt")
create_new_files(data, 6, 30, 31)
create_new_files(data, 7, 1, 15)


data = read_from_files("./data/snapshot_Doodles_20220706.txt")
create_new_files(data, 7, 16, 31)
create_new_files(data, 8, 1, 13)


data = read_from_files("./data/snapshot_Doodles_20220707.txt")
create_new_files(data, 8, 14, 23)



data = read_from_files("./data/snapshot_Doodles_20220708.txt")
create_new_files(data, 8, 24, 31)
create_new_files(data, 9, 1, 2)



data = read_from_files("./data/snapshot_Doodles_20220709.txt")
create_new_files(data, 9, 3, 12)

data = read_from_files("./data/snapshot_Doodles_20220710.txt")
create_new_files(data, 9, 13, 30)

