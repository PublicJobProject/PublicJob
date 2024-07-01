text = "//table[@width='639' and contains(@summary,'제목')]/tbody/tr[;]/td[3]/p/a;6;2"
#text = "//table[@width='639' and contains(@summary,'제목')]/tbody/tr[;]/td[3]/p/a;6"
#text = "//table[@width='639' and contains(@summary,'제목')]/tbody/tr[;]/td[3]/p/a"

textList = text.split(';')
textParsing = ';'.join(textList[:2])
print(textParsing)
removedtext = ';'.join(textList[2:])
print(removedtext)

startIndex, stepIndex = (int(removedtext[0]), int(removedtext[-1])) if len(removedtext) == 3 else (int(removedtext[0]), 1) if len(removedtext) == 1 else (1,1)
print(startIndex, stepIndex)

# if len(removedtext) >= 1:
#     startIndex = removedtext[0]
# if len(removedtext) == 3:
#     stepIndex = removedtext[-1]

# print(startIndex)
# print(stepIndex)