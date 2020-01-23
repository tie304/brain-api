from pydantic import BaseModel, Field


class RunParameters(BaseModel):
    run_parameters: dict