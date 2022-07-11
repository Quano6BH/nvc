for i in range(1, 32):
    with open(f"snapshot/2/2022-08/snapshot_WZRDS_2022_8_{i}.txt", "r") as file:
        data = file.read()
    with open(f"snapshot/2/2022-08/2_2022-08-{i}.txt", "w") as file:
        file.write(data)
