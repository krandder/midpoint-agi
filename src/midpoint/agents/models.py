"""
Data models for the Midpoint system.

This module defines the core data structures used throughout the system.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class State:
    """Represents a specific state of the repository."""
    git_hash: str
    description: str
    repository_path: Optional[str] = None

@dataclass
class Goal:
    """Represents a goal to be achieved."""
    description: str
    validation_criteria: List[str]
    success_threshold: float = 0.8

@dataclass
class SubgoalPlan:
    """Represents the next step toward achieving a goal."""
    next_step: str
    validation_criteria: List[str]
    reasoning: str
    requires_further_decomposition: bool = True  # Flag to indicate if more decomposition is needed
    relevant_context: Dict[str, Any] = field(default_factory=dict)  # Context to pass to child goals
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class StrategyPlan:
    """Represents a plan for achieving a goal."""
    steps: List[str]
    reasoning: str
    estimated_points: int
    metadata: Dict[str, Any]

@dataclass
class TaskContext:
    """Represents the context for a task execution."""
    state: State
    goal: Goal
    iteration: int
    points_consumed: int
    total_budget: int
    execution_history: List[Dict[str, Any]]

@dataclass
class ExecutionTrace:
    """Represents the execution trace of a task."""
    task_description: str
    actions_performed: List[Dict[str, Any]]  # List of actions with their details
    tool_calls: List[Dict[str, Any]]  # List of tool calls with their details
    points_consumed: int
    resulting_state: State  # The state after execution
    execution_time: float  # Time taken to execute the task
    success: bool  # Whether the execution was successful
    branch_name: str  # The git branch where execution occurred
    error_message: Optional[str] = None  # Error message if execution failed

@dataclass
class ExecutionResult:
    """Represents the result of a task execution."""
    success: bool  # Whether the execution was successful
    branch_name: str  # The git branch where execution occurred
    git_hash: str  # The git hash after execution
    error_message: Optional[str] = None  # Error message if execution failed
    execution_time: float = 0.0  # Time taken to execute the task
    points_consumed: int = 0  # Points consumed during execution

@dataclass
class ValidationResult:
    """Represents the result of goal validation."""
    success: bool  # Whether the validation passed
    score: float  # Score between 0 and 1
    reasoning: str  # Explanation of the validation result
    criteria_results: List[Dict[str, Any]]  # Results for each validation criterion
    git_hash: str  # The git hash that was validated
    branch_name: str  # The branch that was validated 