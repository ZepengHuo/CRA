
UUIDmap = {}
with open('Questions.txt','r') as question_file:
    with open('UUIDs.txt','r') as UUID_file:
        Questions = question_file.readlines()
        ULines = UUID_file.readlines()
        for question in Questions:
            for uuid in ULines:
                uuid = uuid.strip()
                if uuid not in UUIDmap:
                    UUIDmap[uuid] = question.strip()
                    break
print(UUIDmap)