---
title: "Chapter 2: LLM-Based Cognitive Planning"
sidebar_position: 2
---

# Chapter 2: LLM-Based Cognitive Planning

## Overview

Welcome to Chapter 2 of Module 4: Vision-Language-Action (VLA) Integration. This chapter focuses on designing systems that convert natural language instructions to structured robot action plans using Large Language Models (LLMs). You'll learn how to implement prompt engineering strategies, map natural language to ROS 2 actions, handle ambiguous instructions, and validate LLM-generated plans for safety.

## Learning Objectives

By the end of this chapter, you will be able to:
- Design prompt engineering strategies for robotic tasks
- Convert natural language instructions to structured robot action plans
- Implement safety validation for LLM-generated action sequences
- Handle ambiguous or complex natural language instructions
- Evaluate and optimize LLM performance for robotic planning

## Prerequisites

Before starting this chapter, ensure you have:
- Completed Chapter 1 (Voice-to-Action)
- Access to LLM API (OpenAI, Llama, etc.)
- Basic understanding of ROS 2 action servers and services
- Familiarity with prompt engineering concepts

## LLM Integration for Robotics

### Setting Up LLM Access

```python
import openai
import os
from typing import Dict, List, Any, Optional
import json

class LLMConfig:
    def __init__(self):
        # Load API key from environment variable
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        openai.api_key = self.api_key
        self.model = os.getenv("LLM_MODEL", "gpt-4-turbo")  # Default to GPT-4 Turbo

class LLMInterface:
    def __init__(self):
        self.config = LLMConfig()
        self.system_prompt = self._create_system_prompt()

    def _create_system_prompt(self) -> str:
        """Create system prompt for robotic planning"""
        return """
        You are an expert robotic planning assistant. Your role is to convert natural language instructions into structured robot action plans.

        When processing instructions:
        1. Break down complex instructions into simple, executable steps
        2. Consider robot capabilities and environmental constraints
        3. Generate valid ROS 2 action sequences
        4. Include safety checks and validation criteria
        5. Return structured JSON output with clear action definitions

        Always return your response in valid JSON format with the following structure:
        {
            "plan_id": "unique_plan_identifier",
            "actions": [
                {
                    "action_type": "action_name",
                    "parameters": {"param1": "value1", "param2": "value2"},
                    "estimated_duration": 5.0,
                    "safety_check": "description of safety check"
                }
            ],
            "validation_results": {
                "feasibility": true/false,
                "safety_check": "passed/failed",
                "confidence_score": 0.0-1.0
            }
        }

        Only return the JSON object, nothing else.
        """
```

### Natural Language to Action Mapping

```python
import re
from dataclasses import dataclass
from typing import Dict, List, Any, Tuple

@dataclass
class ActionStep:
    action_type: str
    parameters: Dict[str, Any]
    estimated_duration: float
    safety_check: str

@dataclasses.dataclass
class ActionPlan:
    plan_id: str
    actions: List[ActionStep]
    validation_results: Dict[str, Any]
    original_instruction: str

class NaturalLanguageMapper:
    def __init__(self):
        # Define common action mappings
        self.action_mappings = {
            "navigation.move_to": [
                r"move to",
                r"go to",
                r"navigate to",
                r"travel to",
                r"walk to"
            ],
            "manipulation.grasp_object": [
                r"grasp",
                r"grab",
                r"pick up",
                r"take",
                r"hold"
            ],
            "manipulation.place_object": [
                r"place",
                r"put down",
                r"set down",
                r"release",
                r"drop"
            ],
            "perception.locate_object": [
                r"find",
                r"locate",
                r"search for",
                r"look for",
                r"detect"
            ],
            "navigation.follow_path": [
                r"follow",
                r"trace",
                r"move along",
                r"navigate following"
            ]
        }

    def extract_location_parameters(self, instruction: str) -> Dict[str, Any]:
        """Extract location parameters from instruction"""
        params = {}

        # Look for coordinate specifications
        coord_pattern = r"coordinates?\s*\(?([-\d.]+)\s*,\s*([-\d.]+)\)?"
        coord_match = re.search(coord_pattern, instruction, re.IGNORECASE)
        if coord_match:
            params["x"] = float(coord_match.group(1))
            params["y"] = float(coord_match.group(2))
            if len(coord_match.groups()) > 2:
                params["z"] = float(coord_match.group(3))

        # Look for named locations
        location_patterns = [
            (r"kitchen", {"room": "kitchen"}),
            (r"living room", {"room": "living_room"}),
            (r"bedroom", {"room": "bedroom"}),
            (r"office", {"room": "office"}),
            (r"bathroom", {"room": "bathroom"})
        ]

        for pattern, loc_params in location_patterns:
            if re.search(pattern, instruction, re.IGNORECASE):
                params.update(loc_params)
                break

        return params

    def extract_object_parameters(self, instruction: str) -> Dict[str, Any]:
        """Extract object parameters from instruction"""
        params = {}

        # Look for object types
        object_patterns = [
            (r"cup|glass|mug", {"object_type": "cup"}),
            (r"book|novel|textbook", {"object_type": "book"}),
            (r"bottle|container", {"object_type": "bottle"}),
            (r"ball|toy", {"object_type": "ball"}),
            (r"box|container", {"object_type": "box"})
        ]

        for pattern, obj_params in object_patterns:
            if re.search(pattern, instruction, re.IGNORECASE):
                params.update(obj_params)
                break

        # Look for object colors
        color_patterns = [
            (r"red", {"color": "red"}),
            (r"blue", {"color": "blue"}),
            (r"green", {"color": "green"}),
            (r"yellow", {"color": "yellow"}),
            (r"black", {"color": "black"}),
            (r"white", {"color": "white"})
        ]

        for pattern, color_params in color_patterns:
            if re.search(pattern, instruction, re.IGNORECASE):
                params.update(color_params)
                break

        return params
```

### Prompt Engineering for Robotic Tasks

```python
import json
from typing import Dict, Any

class PromptEngineer:
    def __init__(self):
        self.context_template = """
        Robot Capabilities:
        - Navigation: Can move to specified locations
        - Manipulation: Can grasp and place objects
        - Perception: Can detect and locate objects
        - Communication: Can respond to voice commands

        Environment Information:
        - Current Position: {current_position}
        - Available Objects: {available_objects}
        - Known Locations: {known_locations}
        - Robot Status: {robot_status}

        Instructions: {natural_language_instruction}
        """

    def create_planning_prompt(self, instruction: str, context: Dict[str, Any]) -> str:
        """Create a comprehensive prompt for LLM planning"""
        context_filled = self.context_template.format(
            current_position=context.get("current_position", "unknown"),
            available_objects=", ".join(context.get("available_objects", [])),
            known_locations=", ".join(context.get("known_locations", [])),
            robot_status=context.get("robot_status", "idle"),
            natural_language_instruction=instruction
        )

        full_prompt = f"""
        {context_filled}

        Convert this natural language instruction into a structured action plan. Consider:
        1. Robot capabilities and limitations
        2. Environmental constraints
        3. Safety requirements
        4. Efficiency of the plan

        Return only valid JSON with the structure specified in the system prompt.
        """
        return full_prompt

    def validate_and_parse_response(self, llm_response: str) -> Optional[ActionPlan]:
        """Validate and parse LLM response into ActionPlan"""
        try:
            # Clean the response to extract JSON
            json_start = llm_response.find('{')
            json_end = llm_response.rfind('}') + 1

            if json_start != -1 and json_end != 0:
                json_str = llm_response[json_start:json_end]
                data = json.loads(json_str)

                # Validate required fields
                required_fields = ["plan_id", "actions", "validation_results"]
                for field in required_fields:
                    if field not in data:
                        return None

                # Convert actions to ActionStep objects
                action_steps = []
                for action_data in data["actions"]:
                    action_step = ActionStep(
                        action_type=action_data["action_type"],
                        parameters=action_data.get("parameters", {}),
                        estimated_duration=action_data.get("estimated_duration", 5.0),
                        safety_check=action_data.get("safety_check", "basic safety check")
                    )
                    action_steps.append(action_step)

                return ActionPlan(
                    plan_id=data["plan_id"],
                    actions=action_steps,
                    validation_results=data["validation_results"],
                    original_instruction=data.get("original_instruction", "")
                )

            return None
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error parsing LLM response: {e}")
            return None
```

## Cognitive Planning System

### Complete Planning Implementation

```python
import time
from typing import Optional

class CognitivePlanningSystem:
    def __init__(self):
        self.llm_interface = LLMInterface()
        self.natural_language_mapper = NaturalLanguageMapper()
        self.prompt_engineer = PromptEngineer()
        self.max_retries = 3

    def generate_action_plan(self, instruction: str, context: Dict[str, Any]) -> Optional[ActionPlan]:
        """Generate action plan from natural language instruction"""
        print(f"Generating action plan for: '{instruction}'")

        # Create the planning prompt
        prompt = self.prompt_engineer.create_planning_prompt(instruction, context)

        # Call the LLM
        for attempt in range(self.max_retries):
            try:
                response = openai.ChatCompletion.create(
                    model=self.llm_interface.config.model,
                    messages=[
                        {"role": "system", "content": self.llm_interface.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,  # Lower temperature for more consistent outputs
                    max_tokens=1000,
                    timeout=30
                )

                llm_response = response.choices[0].message.content
                action_plan = self.prompt_engineer.validate_and_parse_response(llm_response)

                if action_plan:
                    print(f"Successfully generated action plan with {len(action_plan.actions)} steps")
                    return action_plan
                else:
                    print(f"Attempt {attempt + 1}: Failed to parse LLM response")
                    if attempt < self.max_retries - 1:
                        time.sleep(1)  # Brief delay before retry
                    continue

            except Exception as e:
                print(f"Attempt {attempt + 1}: Error calling LLM: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2)  # Longer delay on error
                continue

        print("Failed to generate action plan after all retries")
        return None

    def refine_plan(self, plan: ActionPlan, feedback: str) -> Optional[ActionPlan]:
        """Refine an existing plan based on feedback"""
        refinement_prompt = f"""
        Original Instruction: {plan.original_instruction}
        Generated Plan: {json.dumps([{
            'action_type': action.action_type,
            'parameters': action.parameters,
            'estimated_duration': action.estimated_duration
        } for action in plan.actions], indent=2)}

        Feedback: {feedback}

        Please refine the action plan based on the feedback while maintaining the overall goal.
        Return only valid JSON with the same structure as before.
        """

        try:
            response = openai.ChatCompletion.create(
                model=self.llm_interface.config.model,
                messages=[
                    {"role": "system", "content": self.llm_interface.system_prompt},
                    {"role": "user", "content": refinement_prompt}
                ],
                temperature=0.2,
                max_tokens=1000
            )

            refined_response = response.choices[0].message.content
            refined_plan = self.prompt_engineer.validate_and_parse_response(refined_response)

            return refined_plan
        except Exception as e:
            print(f"Error refining plan: {e}")
            return None
```

## Safety Validation System

### Plan Validation Implementation

```python
from enum import Enum
from typing import Dict, Any, List

class SafetyCheckResult(Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"

class SafetyValidator:
    def __init__(self):
        # Define safety rules
        self.safety_rules = {
            "navigation": self._validate_navigation,
            "manipulation": self._validate_manipulation,
            "perception": self._validate_perception
        }

    def _validate_navigation(self, action: ActionStep, context: Dict[str, Any]) -> Tuple[SafetyCheckResult, str]:
        """Validate navigation actions for safety"""
        # Check if destination is in known safe areas
        destination = action.parameters.get("destination")
        if destination:
            known_safe_areas = context.get("safe_areas", [])
            if destination not in known_safe_areas:
                return SafetyCheckResult.WARNING, f"Destination {destination} not in known safe areas"

        # Check for collision risks
        path = action.parameters.get("path")
        if path:
            obstacles = context.get("detected_obstacles", [])
            for point in path:
                if point in obstacles:
                    return SafetyCheckResult.FAILED, f"Path contains obstacle at {point}"

        return SafetyCheckResult.PASSED, "Navigation path is safe"

    def _validate_manipulation(self, action: ActionStep, context: Dict[str, Any]) -> Tuple[SafetyCheckResult, str]:
        """Validate manipulation actions for safety"""
        object_type = action.parameters.get("object_type")
        if object_type:
            dangerous_objects = ["knife", "blade", "sharp", "hot", "breakable"]
            if any(danger in object_type.lower() for danger in dangerous_objects):
                return SafetyCheckResult.WARNING, f"Manipulation of {object_type} may be dangerous"

        # Check if robot has appropriate gripper for object
        object_size = action.parameters.get("object_size")
        gripper_type = context.get("gripper_type", "default")

        if object_size and object_size == "large" and gripper_type == "small":
            return SafetyCheckResult.WARNING, "Gripper may not be appropriate for object size"

        return SafetyCheckResult.PASSED, "Manipulation is safe"

    def _validate_perception(self, action: ActionStep, context: Dict[str, Any]) -> Tuple[SafetyCheckResult, str]:
        """Validate perception actions for safety"""
        # Perception actions are generally safe, but check for privacy concerns
        target = action.parameters.get("target")
        if target and target in context.get("private_areas", []):
            return SafetyCheckResult.WARNING, f"Perception in private area {target} detected"

        return SafetyCheckResult.PASSED, "Perception action is safe"

    def validate_action_plan(self, plan: ActionPlan, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an entire action plan"""
        validation_results = {
            "overall_status": "passed",
            "action_validations": [],
            "safety_score": 1.0,
            "warnings": [],
            "errors": []
        }

        total_actions = len(plan.actions)
        safe_actions = 0

        for i, action in enumerate(plan.actions):
            action_type_prefix = action.action_type.split('.')[0]
            validator = self.safety_rules.get(action_type_prefix, self._default_validator)

            result, message = validator(action, context)

            action_validation = {
                "action_index": i,
                "action_type": action.action_type,
                "result": result.value,
                "message": message
            }

            validation_results["action_validations"].append(action_validation)

            if result == SafetyCheckResult.PASSED:
                safe_actions += 1
            elif result == SafetyCheckResult.FAILED:
                validation_results["errors"].append(f"Action {i}: {message}")
                validation_results["overall_status"] = "failed"
            elif result == SafetyCheckResult.WARNING:
                validation_results["warnings"].append(f"Action {i}: {message}")

        # Calculate safety score
        validation_results["safety_score"] = safe_actions / total_actions if total_actions > 0 else 1.0

        # Update overall status if there are warnings but no failures
        if validation_results["overall_status"] == "passed" and validation_results["warnings"]:
            validation_results["overall_status"] = "passed_with_warnings"

        return validation_results

    def _default_validator(self, action: ActionStep, context: Dict[str, Any]) -> Tuple[SafetyCheckResult, str]:
        """Default validator for unknown action types"""
        return SafetyCheckResult.PASSED, "Action type not specifically validated, assuming safe"
```

## Complete Cognitive Planning Implementation

```python
class CompleteCognitivePlanner:
    def __init__(self):
        self.planning_system = CognitivePlanningSystem()
        self.safety_validator = SafetyValidator()

    def plan_from_instruction(self, instruction: str, context: Dict[str, Any]) -> Optional[ActionPlan]:
        """Complete pipeline: instruction → plan → validation"""
        # Generate the initial plan
        plan = self.planning_system.generate_action_plan(instruction, context)

        if not plan:
            print("Failed to generate initial action plan")
            return None

        # Validate the plan
        validation_results = self.safety_validator.validate_action_plan(plan, context)

        # Update plan with validation results
        plan.validation_results.update(validation_results)

        # Log validation results
        print(f"Plan validation: {validation_results['overall_status']}")
        if validation_results['warnings']:
            print(f"Warnings: {len(validation_results['warnings'])}")
        if validation_results['errors']:
            print(f"Errors: {len(validation_results['errors'])}")

        # If there are critical errors, try to refine the plan
        if validation_results['overall_status'] == 'failed':
            print("Plan has critical safety errors, attempting refinement...")

            # Create feedback for the LLM
            error_feedback = " ".join(validation_results['errors'])
            refined_plan = self.planning_system.refine_plan(plan, f"Safety issues: {error_feedback}")

            if refined_plan:
                # Re-validate the refined plan
                refined_validation = self.safety_validator.validate_action_plan(refined_plan, context)
                refined_plan.validation_results.update(refined_validation)

                if refined_validation['overall_status'] in ['passed', 'passed_with_warnings']:
                    print("Refined plan passed validation")
                    return refined_plan
                else:
                    print("Refined plan still has safety issues")
                    return None
            else:
                print("Failed to refine plan")
                return None

        return plan

    def execute_plan_safely(self, plan: ActionPlan, robot_interface):
        """Execute a validated plan with safety monitoring"""
        print(f"Executing plan with {len(plan.actions)} actions...")

        for i, action_step in enumerate(plan.actions):
            print(f"Executing action {i+1}/{len(plan.actions)}: {action_step.action_type}")

            # Safety check before execution
            if not self._pre_execution_safety_check(action_step, robot_interface):
                print(f"Pre-execution safety check failed for action {i+1}")
                return False

            # Execute the action
            try:
                success = robot_interface.execute_action(action_step)
                if not success:
                    print(f"Action {i+1} failed to execute")
                    return False

                print(f"Action {i+1} completed successfully")

            except Exception as e:
                print(f"Error executing action {i+1}: {e}")
                return False

        print("Plan executed successfully!")
        return True

    def _pre_execution_safety_check(self, action_step: ActionStep, robot_interface) -> bool:
        """Perform safety checks before executing an action"""
        # This would interface with the robot's safety systems
        # For now, we'll just return True as a placeholder
        return True
```

## Testing the Cognitive Planning System

### Test Implementation

```python
def test_cognitive_planning():
    """Test the cognitive planning system"""
    planner = CompleteCognitivePlanner()

    # Define a test context
    test_context = {
        "current_position": {"x": 0.0, "y": 0.0, "z": 0.0},
        "available_objects": ["cup", "book", "bottle"],
        "known_locations": ["kitchen", "living_room", "bedroom"],
        "robot_status": "ready",
        "safe_areas": ["kitchen", "living_room", "bedroom", "hallway"],
        "gripper_type": "standard",
        "private_areas": ["bedroom_closet"]
    }

    # Test instructions
    test_instructions = [
        "Please go to the kitchen and bring me a cup",
        "Move to the living room and find the red book",
        "Navigate to coordinates (5.2, 3.1) and wait there"
    ]

    for instruction in test_instructions:
        print(f"\n--- Testing instruction: '{instruction}' ---")

        plan = planner.plan_from_instruction(instruction, test_context)

        if plan:
            print(f"Plan ID: {plan.plan_id}")
            print(f"Number of actions: {len(plan.actions)}")
            print(f"Validation status: {plan.validation_results.get('overall_status', 'unknown')}")

            for i, action in enumerate(plan.actions):
                print(f"  {i+1}. {action.action_type} with params: {action.parameters}")
        else:
            print("Failed to generate plan for this instruction")

# Run the test
if __name__ == "__main__":
    test_cognitive_planning()
```

## Advanced Planning Concepts

### Hierarchical Task Decomposition

```python
class HierarchicalTaskDecomposer:
    def __init__(self):
        self.task_decomposition_rules = {
            "complex_navigation": self._decompose_complex_navigation,
            "object_interaction": self._decompose_object_interaction,
            "multi_step_task": self._decompose_multi_step_task
        }

    def _decompose_complex_navigation(self, goal: str) -> List[ActionStep]:
        """Decompose complex navigation tasks"""
        # Example: "Go to the kitchen via the living room"
        # Would decompose into: navigate to living room, then navigate to kitchen
        actions = []

        # This is a simplified example - in practice, this would be more sophisticated
        if "via" in goal.lower():
            # Split the goal into intermediate destinations
            parts = goal.lower().split("via")
            main_goal = parts[0].strip()
            intermediate = parts[1].strip()

            # Add intermediate navigation
            actions.append(ActionStep(
                action_type="navigation.move_to",
                parameters={"destination": intermediate},
                estimated_duration=10.0,
                safety_check="path planning to intermediate destination"
            ))

            # Add final navigation
            actions.append(ActionStep(
                action_type="navigation.move_to",
                parameters={"destination": main_goal.replace("go to", "").strip()},
                estimated_duration=10.0,
                safety_check="path planning to final destination"
            ))
        else:
            # Simple navigation
            actions.append(ActionStep(
                action_type="navigation.move_to",
                parameters={"destination": goal.replace("go to", "").strip()},
                estimated_duration=15.0,
                safety_check="direct path planning"
            ))

        return actions

    def _decompose_object_interaction(self, goal: str) -> List[ActionStep]:
        """Decompose object interaction tasks"""
        # Example: "Pick up the red cup and place it on the table"
        actions = []

        # Detect grasp action
        if any(word in goal.lower() for word in ["pick up", "grasp", "grab", "take"]):
            # First locate the object
            actions.append(ActionStep(
                action_type="perception.locate_object",
                parameters={"object_type": "cup", "color": "red"},
                estimated_duration=5.0,
                safety_check="object detection and localization"
            ))

            # Then grasp it
            actions.append(ActionStep(
                action_type="manipulation.grasp_object",
                parameters={"object_id": "red_cup_123"},  # Would be determined by locate step
                estimated_duration=3.0,
                safety_check="safe grasping motion"
            ))

        # Detect placement action
        if any(word in goal.lower() for word in ["place", "put", "set"]):
            # First navigate to placement location
            actions.append(ActionStep(
                action_type="navigation.move_to",
                parameters={"destination": "table"},
                estimated_duration=10.0,
                safety_check="navigation to placement location"
            ))

            # Then place the object
            actions.append(ActionStep(
                action_type="manipulation.place_object",
                parameters={"placement_location": "table"},
                estimated_duration=3.0,
                safety_check="safe placement motion"
            ))

        return actions

    def decompose_task(self, goal: str) -> List[ActionStep]:
        """Decompose a high-level task into primitive actions"""
        actions = []

        # Determine the type of task and apply appropriate decomposition
        if any(word in goal.lower() for word in ["go to", "navigate", "move to", "travel"]):
            actions.extend(self._decompose_complex_navigation(goal))
        elif any(word in goal.lower() for word in ["pick", "grasp", "grab", "place", "put"]):
            actions.extend(self._decompose_object_interaction(goal))
        else:
            # Default to simple action
            actions.append(ActionStep(
                action_type="general.execute",
                parameters={"instruction": goal},
                estimated_duration=10.0,
                safety_check="general execution with monitoring"
            ))

        return actions
```

## Summary

In this chapter, you've learned how to implement LLM-based cognitive planning for robotic applications. You've created systems to convert natural language instructions to structured action plans, implemented safety validation mechanisms, and developed techniques for handling ambiguous instructions.

The next chapter will focus on the capstone project where you'll integrate all VLA components into a complete autonomous humanoid system.