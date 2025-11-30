from pydantic import BaseModel


class StudyGuideOverview(BaseModel):
    """Structured overview of study material"""
    main_topic: str
    key_sections: list[str]
    learning_objectives: list[str]
    difficulty_level: str  # "beginner", "intermediate", or "advanced"
