"""
Unit tests for the decompose command in goal_cli.py.
"""

import asyncio
import json
import os
import io
import sys
import unittest
import logging
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock
import tempfile
import shutil

# Import goal_cli and the goal decomposer
import midpoint.goal_cli as goal_cli
from midpoint.agents.goal_decomposer import decompose_goal
from tests.test_helpers import async_test

class TestGoalCliDecompose(unittest.TestCase):
    """Test the decompose_existing_goal function in goal_cli.py."""
    
    def setUp(self):
        """Set up temporary directory and files for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.goal_dir = Path(self.temp_dir) / ".goal"
        self.goal_dir.mkdir()
        
        # Create a test goal file
        self.goal_id = "G1"
        self.goal_data = {
            "goal_id": self.goal_id,
            "description": "Test goal",
            "parent_goal": "",
            "timestamp": "20250101_000000"
        }
        self.goal_file = self.goal_dir / f"{self.goal_id}.json"
        with open(self.goal_file, "w") as f:
            json.dump(self.goal_data, f)
        
        # Save original directory
        self.original_dir = os.getcwd()
        # Change to the temporary directory
        os.chdir(self.temp_dir)
    
    def cleanup(self):
        """Clean up the test environment."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir)
    
    def tearDown(self):
        """Clean up after the test."""
        self.cleanup()
    
    @patch('midpoint.goal_cli.agent_decompose_goal')
    @async_test
    async def test_decompose_existing_goal_success(self, mock_decompose_goal):
        """Test the decompose_existing_goal function with a successful result."""
        # Set up the mock
        mock_decompose_goal.return_value = {
            "success": True,
            "next_step": "Implement feature X",
            "validation_criteria": ["Test passes", "Code works"],
            "requires_further_decomposition": True,
            "git_hash": "abcdef123456",
            "memory_hash": "abcdef123456",
            "is_task": False,
            "goal_file": "G1-S1.json",
            "reasoning": "This is the reasoning",
            "relevant_context": "This is the relevant context",
            "initial_memory_hash": "abcdef123456",
            "initial_git_hash": "abcdef123456"
        }
        
        # Capture stdout
        orig_stdout = sys.stdout
        stdout_buffer = io.StringIO()
        sys.stdout = stdout_buffer
        
        try:
            # Call the function with await
            result = await goal_cli.decompose_existing_goal(self.goal_id)
            
            # Check the result
            self.assertTrue(result)
            
            # Check that the function was called with correct arguments
            mock_decompose_goal.assert_called_once()
            args, kwargs = mock_decompose_goal.call_args
            self.assertEqual(kwargs["repo_path"], os.getcwd())
            self.assertEqual(kwargs["goal"], "Test goal")
            self.assertEqual(kwargs["parent_goal"], self.goal_id)
            
            # Check the output
            output = stdout_buffer.getvalue()
            self.assertIn(f"Goal {self.goal_id} successfully decomposed into a subgoal", output)
            self.assertIn("Next step: Implement feature X", output)
            self.assertIn("Validation criteria:", output)
            self.assertIn("- Test passes", output)
            self.assertIn("- Code works", output)
            self.assertIn("Requires further decomposition: Yes", output)
        finally:
            # Restore stdout
            sys.stdout = orig_stdout
    
    @patch('midpoint.goal_cli.agent_decompose_goal')
    @patch('logging.error')
    @async_test
    async def test_decompose_existing_goal_failure(self, mock_logging_error, mock_decompose_goal):
        """Test the decompose_existing_goal function with a failed result."""
        # Set up the mock
        mock_decompose_goal.return_value = {
            "success": False,
            "error": "Failed to generate subgoals"
        }
        
        # Call the function with await
        result = await goal_cli.decompose_existing_goal(self.goal_id)
        
        # Check the result
        self.assertFalse(result)
        
        # Check that the error was logged with the correct message
        mock_logging_error.assert_any_call("Failed to decompose goal: Failed to generate subgoals")
    
    @patch('logging.error')
    @async_test
    async def test_decompose_nonexistent_goal(self, mock_logging_error):
        """Test decompose_existing_goal with a nonexistent goal."""
        # Call the function with a nonexistent goal and await
        result = await goal_cli.decompose_existing_goal("NonExistentGoal")
        
        # Check the result
        self.assertFalse(result)
        
        # Check that the error was logged with the correct message
        mock_logging_error.assert_called_with("Goal NonExistentGoal not found")


if __name__ == "__main__":
    unittest.main() 