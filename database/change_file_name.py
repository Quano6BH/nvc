for i in range(1, 10):
    with open(f"snapshot/month-7/snapshot_Doodles_2022-07-{i}.txt", "r") as file:
        data = file.read()
    with open(f"snapshot/month-7/1_2022-07-{i}.txt", "w") as file:
        file.write(data)
