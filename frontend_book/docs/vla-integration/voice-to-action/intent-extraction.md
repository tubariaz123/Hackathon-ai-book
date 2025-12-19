---
title: "Intent Extraction for Robots"
sidebar_position: 3
---

# Intent Extraction for Robots

This section covers how to extract robot-appropriate intents from natural language commands. We'll explore techniques for understanding what the user wants the robot to do based on spoken or written input.

## Understanding Intent Extraction

Intent extraction is the process of identifying the underlying purpose or goal expressed in natural language. For robotics, this means converting human commands into specific robot actions or behaviors.

### Key Components of Intent Extraction

1. **Entity Recognition**: Identifying objects, locations, and parameters mentioned in commands
2. **Action Classification**: Determining what type of action the robot should perform
3. **Parameter Extraction**: Extracting specific details like distances, directions, or object properties
4. **Context Awareness**: Understanding commands based on the current situation

## Rule-Based Intent Extraction

Simple rule-based systems work well for structured robot commands:

```python
import re
from typing import Dict, List, Tuple

class RuleBasedIntentExtractor:
    def __init__(self):
        # Define command patterns
        self.patterns = {
            'navigation': [
                (r'move\s+(forward|backward|ahead)', ('MOVE', {'direction': r'\1'})),
                (r'go\s+(forward|backward|left|right)', ('NAVIGATE', {'direction': r'\1'})),
                (r'go\s+to\s+(.+)', ('GO_TO', {'location': r'\1'})),
                (r'move\s+to\s+(.+)', ('GO_TO', {'location': r'\1'})),
                (r'turn\s+(left|right)', ('TURN', {'direction': r'\1'})),
                (r'rotate\s+(left|right)', ('ROTATE', {'direction': r'\1'})),
            ],
            'manipulation': [
                (r'(pick|take|grab|get)\s+up\s+(.+)', ('PICK_UP', {'object': r'\2'})),
                (r'(put|place|set)\s+(down|on)\s+(.+)', ('PUT_DOWN', {'object': r'\3'})),
                (r'grasp\s+(.+)', ('GRASP', {'object': r'\1'})),
                (r'drop\s+(.+)', ('DROP', {'object': r'\1'})),
            ],
            'social': [
                (r'follow\s+(me|.+)', ('FOLLOW', {'target': r'\1'})),
                (r'wait\s+(here|there)', ('WAIT', {'location': r'\1'})),
                (r'stop', ('STOP', {})),
                (r'pause', ('PAUSE', {})),
            ]
        }

    def extract_intent(self, text: str) -> Tuple[str, Dict]:
        """
        Extract intent and parameters from text using rule patterns
        """
        text_lower = text.lower().strip()

        for category, pattern_list in self.patterns.items():
            for pattern, (action, param_template) in pattern_list:
                match = re.search(pattern, text_lower)
                if match:
                    # Extract parameters based on regex groups
                    params = {}
                    for key, value_pattern in param_template.items():
                        if isinstance(value_pattern, str) and value_pattern.startswith('\\'):
                            group_num = int(value_pattern[1:])
                            params[key] = match.group(group_num)
                        else:
                            params[key] = value_pattern

                    return action, params

        # Default to unknown if no pattern matches
        return 'UNKNOWN', {'original_text': text}

    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract named entities from text
        """
        entities = []

        # Location entities
        location_patterns = [
            r'(kitchen|living room|bedroom|office|garage|bathroom)',
            r'(table|chair|sofa|counter|shelf|cupboard)',
            r'(door|window|hallway|entrance|exit)'
        ]

        for pattern in location_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                entities.append(('LOCATION', match.group()))

        # Object entities
        object_patterns = [
            r'(block|ball|cup|book|pen|phone|bottle)',
            r'(red|blue|green|yellow|black|white|large|small)\s+\w+'
        ]

        for pattern in object_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                entities.append(('OBJECT', match.group()))

        return entities
```

## Machine Learning Approach

For more sophisticated intent extraction, use machine learning models:

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import torch

class MLIntentExtractor:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        """
        Initialize ML-based intent extractor
        """
        # Use a pre-trained model fine-tuned for intent classification
        self.classifier = pipeline(
            "text-classification",
            model="microsoft/DialoGPT-medium",  # Replace with intent-specific model
            tokenizer="microsoft/DialoGPT-medium"
        )

        # Define robot-specific intents
        self.intent_labels = {
            'navigate_to_location': ['go to', 'move to', 'travel to', 'walk to'],
            'grasp_object': ['pick up', 'grasp', 'take', 'get'],
            'manipulate_object': ['put down', 'place', 'set', 'release'],
            'follow_entity': ['follow', 'accompany', 'come with'],
            'stop_action': ['stop', 'halt', 'pause', 'freeze'],
            'greet_human': ['hello', 'hi', 'greetings', 'hey'],
            'answer_question': ['what', 'where', 'when', 'who', 'how']
        }

    def classify_intent_ml(self, text: str) -> Tuple[str, float]:
        """
        Classify intent using machine learning
        """
        result = self.classifier(text)
        return result['label'], result['score']

    def extract_with_entities(self, text: str):
        """
        Extract intent with entity recognition
        """
        intent, confidence = self.classify_intent_ml(text)

        # Extract entities using regex as backup
        entities = self._extract_entities_regex(text)

        return {
            'intent': intent,
            'confidence': confidence,
            'entities': entities,
            'original_text': text
        }

    def _extract_entities_regex(self, text: str):
        """
        Fallback entity extraction using regex
        """
        entities = []
        # Implementation similar to rule-based extractor
        return entities
```

## Hybrid Approach

Combine rule-based and ML approaches for robust intent extraction:

```python
class HybridIntentExtractor:
    def __init__(self):
        self.rule_extractor = RuleBasedIntentExtractor()
        self.ml_extractor = MLIntentExtractor()

    def extract_intent_hybrid(self, text: str, ml_threshold=0.7) -> Dict:
        """
        Extract intent using hybrid approach
        """
        # Try rule-based extraction first (fast and reliable for known patterns)
        rule_intent, rule_params = self.rule_extractor.extract_intent(text)

        if rule_intent != 'UNKNOWN':
            # Rule-based extraction succeeded
            return {
                'intent': rule_intent,
                'parameters': rule_params,
                'method': 'rule_based',
                'confidence': 1.0,
                'entities': self.rule_extractor.extract_entities(text)
            }

        # Fall back to ML extraction
        ml_result = self.ml_extractor.extract_with_entities(text)

        if ml_result['confidence'] > ml_threshold:
            return {
                'intent': ml_result['intent'],
                'parameters': ml_result.get('entities', {}),
                'method': 'ml_based',
                'confidence': ml_result['confidence'],
                'entities': ml_result['entities']
            }

        # If ML confidence is low, return UNKNOWN
        return {
            'intent': 'UNKNOWN',
            'parameters': {'original_text': text},
            'method': 'unknown',
            'confidence': 0.0,
            'entities': []
        }
```

## Context-Aware Intent Processing

Consider the robot's current state and environment when processing intents:

```python
class ContextAwareIntentProcessor:
    def __init__(self):
        self.intent_extractor = HybridIntentExtractor()
        self.current_context = {}

    def set_context(self, context: Dict):
        """
        Set current context including robot state, location, etc.
        """
        self.current_context = context

    def process_intent_with_context(self, text: str) -> Dict:
        """
        Process intent considering current context
        """
        basic_extraction = self.intent_extractor.extract_intent_hybrid(text)

        # Enhance extraction with context
        enhanced_result = self._apply_context(
            basic_extraction,
            self.current_context
        )

        return enhanced_result

    def _apply_context(self, extraction: Dict, context: Dict) -> Dict:
        """
        Apply contextual information to refine intent extraction
        """
        intent = extraction['intent']
        params = extraction['parameters'].copy()

        # Example context applications
        if intent == 'GO_TO' and 'location' in params:
            # Resolve relative locations based on current position
            if params['location'] in ['here', 'there']:
                params['location'] = self._resolve_relative_location(
                    params['location'],
                    context
                )

        elif intent == 'FOLLOW' and 'target' in params:
            # Resolve pronouns based on context
            if params['target'] == 'me':
                params['target'] = context.get('operator_id', 'human_operator')

        # Add context information to result
        extraction['parameters'] = params
        extraction['context_applied'] = True
        extraction['resolved_context'] = context.copy()

        return extraction

    def _resolve_relative_location(self, location: str, context: Dict) -> str:
        """
        Resolve relative locations like 'here'/'there' based on context
        """
        if location == 'here' and 'current_location' in context:
            return context['current_location']
        elif location == 'there' and 'pointed_location' in context:
            return context['pointed_location']
        else:
            return location
```

## Integration with Robot Systems

Integrate intent extraction with the broader robot system:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from your_robot_interfaces.msg import RobotCommand

class IntentProcessingNode(Node):
    def __init__(self):
        super().__init__('intent_processing_node')

        # Create subscribers and publishers
        self.command_subscriber = self.create_subscription(
            String,
            'recognized_commands',
            self.command_callback,
            10
        )

        self.robot_command_publisher = self.create_publisher(
            RobotCommand,
            'robot_action_plan',
            10
        )

        # Initialize intent processor
        self.intent_processor = ContextAwareIntentProcessor()

        # Maintain robot context
        self.robot_context = {
            'current_location': 'unknown',
            'battery_level': 100,
            'current_task': 'idle',
            'available_actions': ['navigate', 'grasp', 'manipulate', 'communicate']
        }

        self.get_logger().info('Intent processing node initialized')

    def command_callback(self, msg):
        """
        Process incoming natural language commands
        """
        try:
            # Update context
            self.intent_processor.set_context(self.robot_context)

            # Extract intent
            result = self.intent_processor.process_intent_with_context(msg.data)

            if result['intent'] != 'UNKNOWN':
                # Convert to robot command
                robot_cmd = self._convert_to_robot_command(result)

                # Publish robot command
                self.robot_command_publisher.publish(robot_cmd)

                self.get_logger().info(
                    f'Processed intent: {result["intent"]} '
                    f'with confidence: {result["confidence"]:.2f}'
                )
            else:
                self.get_logger().warning(f'Unknown intent for command: {msg.data}')

        except Exception as e:
            self.get_logger().error(f'Error processing command: {e}')

    def _convert_to_robot_command(self, intent_result: Dict) -> RobotCommand:
        """
        Convert intent result to robot command message
        """
        cmd = RobotCommand()
        cmd.action_type = intent_result['intent']
        cmd.confidence = intent_result['confidence']

        # Convert parameters to command fields
        for key, value in intent_result['parameters'].items():
            setattr(cmd, key, str(value))

        cmd.original_text = intent_result['parameters'].get('original_text', '')

        return cmd
```

## Testing Intent Extraction

Test your intent extraction system with various command types:

```python
def test_intent_extraction():
    """
    Test intent extraction with various robot commands
    """
    processor = ContextAwareIntentProcessor()

    test_commands = [
        "Move forward 2 meters",
        "Go to the kitchen",
        "Pick up the red ball",
        "Follow me",
        "Stop immediately",
        "Turn left and wait"
    ]

    for command in test_commands:
        result = processor.process_intent_with_context(command)
        print(f"Command: '{command}'")
        print(f"Intent: {result['intent']}")
        print(f"Parameters: {result['parameters']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print("-" * 40)

if __name__ == "__main__":
    test_intent_extraction()
```

This implementation provides a comprehensive approach to intent extraction for robotics applications, combining rule-based and machine learning methods with contextual awareness for robust performance.