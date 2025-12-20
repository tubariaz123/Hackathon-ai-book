import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/docs',
    component: ComponentCreator('/docs', '096'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '5b5'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '92f'),
            routes: [
              {
                path: '/docs/ai-robot-brain/',
                component: ComponentCreator('/docs/ai-robot-brain/', '974'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/assessment-questions',
                component: ComponentCreator('/docs/ai-robot-brain/assessment-questions', 'f43'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/cross-references',
                component: ComponentCreator('/docs/ai-robot-brain/cross-references', 'c53'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/integration-guide',
                component: ComponentCreator('/docs/ai-robot-brain/integration-guide', '42b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-ros/configuration-examples',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-ros/configuration-examples', '038'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-ros/perception-overview',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-ros/perception-overview', '746'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-ros/troubleshooting',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-ros/troubleshooting', 'bdb'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-ros/tutorials/perception-pipeline',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-ros/tutorials/perception-pipeline', '216'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-ros/tutorials/vslam-implementation',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-ros/tutorials/vslam-implementation', 'a14'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-ros/vslam-navigation',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-ros/vslam-navigation', '126'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-sim/configuration-examples',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-sim/configuration-examples', 'e85'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-sim/introduction',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-sim/introduction', 'c14'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-sim/synthetic-data',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-sim/synthetic-data', '559'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-sim/troubleshooting',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-sim/troubleshooting', '016'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-sim/tutorials/generate-data',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-sim/tutorials/generate-data', '275'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/isaac-sim/tutorials/setup-environment',
                component: ComponentCreator('/docs/ai-robot-brain/isaac-sim/tutorials/setup-environment', '4d0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/learning-objectives',
                component: ComponentCreator('/docs/ai-robot-brain/learning-objectives', '5b6'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/nav2-humanoid/humanoid-constraints',
                component: ComponentCreator('/docs/ai-robot-brain/nav2-humanoid/humanoid-constraints', '007'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/nav2-humanoid/path-planning',
                component: ComponentCreator('/docs/ai-robot-brain/nav2-humanoid/path-planning', '786'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/nav2-humanoid/performance-optimization',
                component: ComponentCreator('/docs/ai-robot-brain/nav2-humanoid/performance-optimization', '32e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/nav2-humanoid/troubleshooting',
                component: ComponentCreator('/docs/ai-robot-brain/nav2-humanoid/troubleshooting', 'dd4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/nav2-humanoid/tutorials/movement-execution',
                component: ComponentCreator('/docs/ai-robot-brain/nav2-humanoid/tutorials/movement-execution', 'bad'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/nav2-humanoid/tutorials/nav2-configuration',
                component: ComponentCreator('/docs/ai-robot-brain/nav2-humanoid/tutorials/nav2-configuration', '11c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/quick-reference',
                component: ComponentCreator('/docs/ai-robot-brain/quick-reference', '06b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ai-robot-brain/terminology',
                component: ComponentCreator('/docs/ai-robot-brain/terminology', '266'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/digital-twin-sim/digital-twins-hri-unity',
                component: ComponentCreator('/docs/digital-twin-sim/digital-twins-hri-unity', 'aab'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/digital-twin-sim/intro',
                component: ComponentCreator('/docs/digital-twin-sim/intro', 'd5e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/digital-twin-sim/physics-simulation-gazebo',
                component: ComponentCreator('/docs/digital-twin-sim/physics-simulation-gazebo', 'df2'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/digital-twin-sim/sensor-simulation-validation',
                component: ComponentCreator('/docs/digital-twin-sim/sensor-simulation-validation', 'f47'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'aed'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ros2-humanoid-fundamentals/communication-model',
                component: ComponentCreator('/docs/ros2-humanoid-fundamentals/communication-model', '63e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ros2-humanoid-fundamentals/intro-to-ros2',
                component: ComponentCreator('/docs/ros2-humanoid-fundamentals/intro-to-ros2', '1f8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/ros2-humanoid-fundamentals/robot-structure-urdf',
                component: ComponentCreator('/docs/ros2-humanoid-fundamentals/robot-structure-urdf', '338'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-integration/',
                component: ComponentCreator('/docs/vla-integration/', '961'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-integration/capstone-autonomous-humanoid',
                component: ComponentCreator('/docs/vla-integration/capstone-autonomous-humanoid', '284'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-integration/evaluation-framework',
                component: ComponentCreator('/docs/vla-integration/evaluation-framework', '2c1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-integration/llm-cognitive-planning',
                component: ComponentCreator('/docs/vla-integration/llm-cognitive-planning', '690'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-integration/spec',
                component: ComponentCreator('/docs/vla-integration/spec', 'c02'),
                exact: true
              },
              {
                path: '/docs/vla-integration/voice-to-action/',
                component: ComponentCreator('/docs/vla-integration/voice-to-action/', 'b69'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-integration/voice-to-action/intent-extraction',
                component: ComponentCreator('/docs/vla-integration/voice-to-action/intent-extraction', '4ad'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/vla-integration/voice-to-action/whisper-implementation',
                component: ComponentCreator('/docs/vla-integration/voice-to-action/whisper-implementation', '761'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '6db'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
