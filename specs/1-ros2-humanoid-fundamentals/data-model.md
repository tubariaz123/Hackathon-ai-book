# Data Model: ROS 2 Fundamentals for Humanoid Robotics

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
- **language**: String - Programming language (C++, Python, etc.)
- **robot_type**: String - Type of robot the example applies to (humanoid, etc.)

### Exercise Entity
- **title**: String - Title of the exercise
- **description**: String - Detailed description of the exercise
- **difficulty**: String - Difficulty level (beginner, intermediate, advanced)
- **expected_outcome**: String - What the user should achieve

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