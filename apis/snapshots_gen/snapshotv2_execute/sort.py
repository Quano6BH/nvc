with open("snapshot_NVC.txt", "r") as file:
    lines = file.readlines()
    lines.sort(key=lambda line: int(line.split("|")[0]))
with open("snapshot_NVC_sorted.txt", "w") as file:
    file.writelines(lines)
# token_ids = [int(x.split("|")[0]) for x in lines]
# count = 0
# for i in range(0, 1000):
#     if i not in token_ids:
#         print(i)
#         count += 1
# print(count)
