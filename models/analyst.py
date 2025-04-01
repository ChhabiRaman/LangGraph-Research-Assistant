"""
Models for the research assistant system.
Contains the data structures for analysts and their related components.
"""

from typing import List
from pydantic import BaseModel, Field

class Analyst(BaseModel):
    """Represents an individual analyst in the research system."""
    
    name: str = Field(
        description="Name of the analyst."
    )

    role: str = Field(
        description="The role of the analyst relevant to the topic."
    )

    description: str = Field(
        description="A short description of the analyst task considering its focus area, expected output, and goal."
    )

    affiliation: str = Field(
        description="The primary affiliation of the analyst."
    )

    @property
    def persona(self) -> str:
        """Returns a formatted string representation of the analyst's persona."""
        return f"Name: {self.name}\nRole: {self.role}\nDescription: {self.description}\nAffiliation: {self.affiliation}"

class Analysts(BaseModel):
    """Container for a list of analysts."""
    
    analysts: List[Analyst] = Field(
        description="A list of analysts with their name, role, description, and affiliation."
    ) 