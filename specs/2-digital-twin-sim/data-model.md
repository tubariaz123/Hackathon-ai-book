# Data Model: Digital Twin Simulation (Gazebo & Unity)

## Educational Content Structure

### Chapter Entity
- **name**: String - The title of the chapter
- **id**: String - Unique identifier for the chapter
- **content**: Markdown - The main content of the chapter
- **learning_objectives**: Array<String> - List of learning objectives for the chapter
- **prerequisites**: Array<String> - Prerequisites needed before reading
- **examples**: Array<Example> - Code or conceptual examples included in the chapter
- **exercises**: Array<Exercise> - Practice exercises for the user

### Example Entity
- **title**: String - Title of the example
- **description**: String - Brief description of what the example demonstrates
- **code**: String - The actual code or command
- **technology**: String - Technology used (Gazebo, Unity, etc.)
- **robot_type**: String - Type of robot the example applies to (humanoid, etc.)

### Exercise Entity
- **title**: String - Title of the exercise
- **description**: String - Detailed description of the exercise
- **difficulty**: String - Difficulty level (beginner, intermediate, advanced)
- **expected_outcome**: String - What the user should achieve

## Simulation Environment Structure

### Gazebo Simulation Entity
- **name**: String - Name of the simulation environment
- **physics_properties**: Object - Mass, friction, collision properties
- **robot_model**: String - Reference to URDF model
- **world_description**: String - SDF world file content
- **sensor_configurations**: Array<SensorConfig> - Sensor setup for the simulation

### Unity Digital Twin Entity
- **name**: String - Name of the digital twin environment
- **visual_properties**: Object - Materials, lighting, textures
- **robot_model**: String - 3D model asset reference
- **interaction_systems**: Array<String> - HRI mechanisms implemented
- **rendering_settings**: Object - Quality and performance settings

### Sensor Configuration Entity
- **type**: String - Sensor type (lidar, camera, imu, etc.)
- **parameters**: Object - Specific sensor parameters
- **simulation_model**: String - How the sensor is modeled in simulation
- **output_format**: String - Format of sensor data output
- **accuracy_metrics**: Object - Simulation accuracy specifications

## Docusaurus Documentation Structure

### Document Entity
- **id**: String - Unique document ID for Docusaurus
- **title**: String - Title displayed in navigation and page
- **sidebar_label**: String - Label used in sidebar navigation
- **slug**: String - URL slug for the document
- **custom_edit_url**: String - Optional URL for editing the document
- **description**: String - Meta description for SEO

### Sidebar Category
- **type**: String - Always "category" for category items
- **label**: String - Display name for the category
- **items**: Array<String|Category> - List of document IDs or nested categories
- **collapsed**: Boolean - Whether the category is collapsed by default