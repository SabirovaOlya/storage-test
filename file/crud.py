from schemas import CreateFile


def create_file(data: CreateFile):
    file = data.model_dump()
    return
