from pydantic import BaseModel

class GitBaseModel(BaseModel):
    repo_path: str