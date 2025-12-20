// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1: The Robotic Nervous System (ROS 2)',
      items: [
        'ros2-humanoid-fundamentals/intro-to-ros2',
        'ros2-humanoid-fundamentals/communication-model',
        'ros2-humanoid-fundamentals/robot-structure-urdf',
      ],
    },
    {
      type: 'category',
      label: 'Module 2: The Digital Twin (Gazebo & Unity)',
      items: [
        'digital-twin-sim/intro',
        'digital-twin-sim/physics-simulation-gazebo',
        'digital-twin-sim/digital-twins-hri-unity',
        'digital-twin-sim/sensor-simulation-validation',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'ai-robot-brain/index',
        {
          type: 'category',
          label: 'Isaac Sim: Synthetic Data Generation',
          items: [
            'ai-robot-brain/isaac-sim/introduction',
            'ai-robot-brain/isaac-sim/synthetic-data',
            'ai-robot-brain/isaac-sim/configuration-examples',
            'ai-robot-brain/isaac-sim/troubleshooting',
            {
              type: 'category',
              label: 'Tutorials',
              items: [
                'ai-robot-brain/isaac-sim/tutorials/setup-environment',
                'ai-robot-brain/isaac-sim/tutorials/generate-data',
              ],
            },
          ],
        },
        {
          type: 'category',
          label: 'Isaac ROS: Perception & Navigation',
          items: [
            'ai-robot-brain/isaac-ros/perception-overview',
            'ai-robot-brain/isaac-ros/vslam-navigation',
            'ai-robot-brain/isaac-ros/configuration-examples',
            'ai-robot-brain/isaac-ros/troubleshooting',
            {
              type: 'category',
              label: 'Tutorials',
              items: [
                'ai-robot-brain/isaac-ros/tutorials/perception-pipeline',
                'ai-robot-brain/isaac-ros/tutorials/vslam-implementation',
              ],
            },
          ],
        },
        {
          type: 'category',
          label: 'Nav2: Humanoid Path Planning',
          items: [
            'ai-robot-brain/nav2-humanoid/path-planning',
            'ai-robot-brain/nav2-humanoid/humanoid-constraints',
            'ai-robot-brain/nav2-humanoid/troubleshooting',
            'ai-robot-brain/nav2-humanoid/performance-optimization',
            {
              type: 'category',
              label: 'Tutorials',
              items: [
                'ai-robot-brain/nav2-humanoid/tutorials/nav2-configuration',
                'ai-robot-brain/nav2-humanoid/tutorials/movement-execution',
              ],
            },
          ],
        },
        {
          type: 'category',
          label: 'Reference Materials',
          items: [
            'ai-robot-brain/terminology',
            'ai-robot-brain/cross-references',
            'ai-robot-brain/integration-guide',
            'ai-robot-brain/learning-objectives',
            'ai-robot-brain/assessment-questions',
            'ai-robot-brain/quick-reference',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action (VLA)',
      items: [
        'vla-integration/index',
        {
          type: 'category',
          label: 'Voice-to-Action',
          items: [
            'vla-integration/voice-to-action/index',
            'vla-integration/voice-to-action/whisper-implementation',
            'vla-integration/voice-to-action/intent-extraction',
          ],
        },
        {
          type: 'category',
          label: 'LLM-Based Cognitive Planning',
          items: [
            'vla-integration/llm-cognitive-planning',
          ],
        },
        {
          type: 'category',
          label: 'Capstone: Autonomous Humanoid',
          items: [
            'vla-integration/capstone-autonomous-humanoid',
          ],
        },
        {
          type: 'category',
          label: 'Evaluation and Testing Framework',
          items: [
            'vla-integration/evaluation-framework',
          ],
        },
      ],
    },
  ],
};

export default sidebars;