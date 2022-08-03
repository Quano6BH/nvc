with open("2_2022-04-26.txt", "r") as file:
    data = file.read()
for i in range(4, 9):
    for j in range(1, 32):
        if j < 10:
            with open(f"./snapshot/2/2022-0{i}/2_2022-0{i}-0{j}.txt", "w") as file:
                file.write(data)
        else:
            with open(f"./snapshot/2/2022-0{i}/2_2022-0{i}-{j}.txt", "w") as file:
                file.write(data)
