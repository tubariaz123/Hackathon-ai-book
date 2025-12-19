---
title: Generating Synthetic Training Data
sidebar_position: 2
---

# Generating Synthetic Training Data

This tutorial will guide you through creating synthetic training data for humanoid robot perception models using Isaac Sim. You'll learn how to set up data recording, configure annotations, and generate diverse datasets.

## Prerequisites

Before starting this tutorial, you should have:
- Completed the Isaac Sim environment setup tutorial
- A basic scene with a humanoid robot and sensors
- Understanding of synthetic data concepts

## Step 1: Enable Synthetic Data Extension

1. In Isaac Sim, go to **Window** → **Extensions**
2. Search for "Synthetic Data" in the extensions list
3. Enable the **Isaac/Isaac Synthetic Data/Isaac Synthetic Data** extension
4. The Synthetic Data panel should now appear in your interface

## Step 2: Configure Camera Sensors for Data Generation

1. Select your RGB camera in the scene
2. In the **Property** panel, under **Isaac Sensors**, ensure **Isaac Camera Sensors** is enabled
3. Expand the camera settings and configure:
   - **Resolution**: Set to your desired output size (e.g., 640x480)
   - **Sensor Type**: RGB, Depth, or both
   - **Sensor Position**: Verify mounting position on the robot

## Step 3: Set Up Annotation Generation

### Semantic Segmentation
1. In the Synthetic Data panel, find your camera
2. Expand the **Annotation** section
3. Enable **Semantic Segmentation**
4. Assign semantic labels to objects in your scene:
   - Select each object in the scene
   - In the **Property** panel, expand **Semantic Labels**
   - Assign appropriate labels (e.g., "robot", "human", "obstacle", "ground")

### Bounding Boxes
1. In the Synthetic Data panel, enable **Bounding Box 2D** annotation
2. This will generate 2D bounding boxes around labeled objects

### Instance Segmentation
1. Enable **Instance Segmentation** for per-instance masks
2. Each unique object instance will get its own mask

## Step 4: Configure Domain Randomization

Domain randomization helps bridge the sim-to-real gap:

### Material Randomization
1. In the Synthetic Data panel, enable **Domain Randomization**
2. Add material randomization:
   - Randomize textures on walls and floors
   - Vary material properties like roughness and metallic values
   - Create diverse environmental appearances

### Lighting Randomization
1. Add lighting randomization:
   - Vary light intensities and colors
   - Randomize light positions
   - Change time-of-day lighting conditions

### Object Placement Randomization
1. Configure random object placement:
   - Randomize positions of obstacles
   - Vary object scales within reasonable ranges
   - Randomize orientations

## Step 5: Set Up Data Recording

### Create Data Capture Script
1. In the Synthetic Data panel, configure the **Data Capture** settings
2. Set the output directory for your generated data
3. Configure the data format (typically PNG for images, JSON for annotations)

### Recording Parameters
1. **Frame Rate**: Set appropriate recording rate (e.g., 1-10 FPS for static scenes, higher for dynamic scenes)
2. **Sequence Length**: Define how many frames to capture per sequence
3. **Annotations**: Select which annotation types to generate

## Step 6: Execute Data Generation

### Manual Recording
1. Position your robot in the starting configuration
2. Click the **Play** button to start simulation
3. In the Synthetic Data panel, start data capture
4. Move your robot around the environment to capture diverse viewpoints
5. Stop data capture when finished

### Automated Recording
1. Create a simple navigation script for your robot
2. Program the robot to follow a path that captures diverse viewpoints
3. Set up automatic data capture during the navigation

## Step 7: Validate Generated Data

### Quality Checks
1. Review a sample of generated images:
   - Verify image quality and resolution
   - Check that semantic segmentation is accurate
   - Ensure bounding boxes align properly

2. Validate annotation accuracy:
   - Compare segmentation masks to original objects
   - Verify bounding box coordinates
   - Check that instance segmentation is correct

### Quantity Requirements
1. Ensure you have sufficient data for your training needs
2. Verify data diversity across different scenarios
3. Check that edge cases are adequately represented

## Step 8: Organize and Export Data

### Data Structure
Organize your data in a standard structure:
```
dataset/
├── images/
│   ├── rgb/
│   └── depth/
├── annotations/
│   ├── segmentation/
│   ├── bounding_boxes/
│   └── instances/
└── metadata.json
```

### Format Conversion
If needed, convert data to your ML framework's expected format:
- Convert annotations to COCO or Pascal VOC format
- Resize images if needed
- Normalize depth data

## Best Practices

### Data Diversity
- Capture data from multiple viewpoints
- Include various lighting conditions
- Vary object configurations and positions
- Include dynamic and static scenarios

### Quality Assurance
- Regularly validate generated data quality
- Implement automated validation checks
- Compare synthetic vs. real data distributions
- Monitor for artifacts or unrealistic elements

### Performance Optimization
- Balance visual fidelity with generation speed
- Use appropriate scene complexity
- Optimize sensor configurations for your needs

## Troubleshooting

### Common Issues and Solutions

**Low-Quality Annotations:**
- Verify semantic labels are correctly assigned
- Check that objects have proper collision geometry
- Ensure annotation extension is properly configured

**Performance Issues:**
- Reduce scene complexity during data generation
- Lower rendering resolution temporarily
- Disable non-essential visual effects

**Insufficient Diversity:**
- Increase domain randomization parameters
- Add more environmental variations
- Create multiple scene configurations

## Next Steps

Continue to learn about Isaac Sim configuration examples and best practices to optimize your synthetic data generation pipeline.