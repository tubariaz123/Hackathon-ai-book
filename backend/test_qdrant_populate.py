"""
Quick test script to populate Qdrant with basic AI/ROS content for immediate testing
"""

import uuid
from qdrant_client import QdrantClient
from qdrant_client.http import models
import cohere
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
co = cohere.Client(cohere_api_key)

# Initialize Qdrant client - using local instance now
qdrant_client = QdrantClient(path="./qdrant_data")

# Sample content about AI and ROS 2 for immediate testing
sample_contents = [
    {
        'title': 'Introduction to Artificial Intelligence',
        'url': 'https://example.com/ai-intro',
        'content': 'Artificial Intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of "intelligent agents".'
    },
    {
        'title': 'What is ROS 2?',
        'url': 'https://example.com/ros2-intro',
        'content': 'ROS 2 (Robot Operating System 2) is flexible framework for writing robot software. It is a collection of tools, libraries, and conventions that aim to simplify the task of creating complex and robust robot behavior across a wide variety of robotic platforms.'
    },
    {
        'title': 'ROS 2 Architecture',
        'url': 'https://example.com/ros2-architecture',
        'content': 'ROS 2 uses DDS (Data Distribution Service) as its underlying communication layer. It provides improved real-time performance, better security, and support for multiple DDS implementations compared to ROS 1.'
    },
    {
        'title': 'AI in Robotics',
        'url': 'https://example.com/ai-robotics',
        'content': 'Artificial Intelligence plays a crucial role in robotics, enabling robots to perceive their environment, make decisions, and perform complex tasks autonomously. Machine learning algorithms help robots adapt to new situations.'
    },
    {
        'title': 'Robot Operating System Concepts',
        'url': 'https://example.com/ros-concepts',
        'content': 'ROS provides services designed for a heterogeneous computer cluster such as hardware abstraction, device drivers, libraries, visualizers, message-passing, package management, and more.'
    }
]

def embed_text(texts):
    """Generate embeddings for texts using Cohere"""
    try:
        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type="search_document"
        )
        return response.embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []

def populate_qdrant():
    """Populate Qdrant with sample content"""
    print("Populating local Qdrant with sample AI/ROS content...")

    points = []

    for i, content_item in enumerate(sample_contents):
        print(f"Processing item {i+1}: {content_item['title']}")

        # Generate embedding for the content
        embeddings = embed_text([content_item['content']])

        if embeddings and len(embeddings) > 0:
            embedding = embeddings[0]

            # Create a point for Qdrant
            point = models.PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    'title': content_item['title'],
                    'url': content_item['url'],
                    'content': content_item['content']
                }
            )
            points.append(point)
        else:
            print(f"Failed to generate embedding for item {i+1}")

    # Upload all points to Qdrant
    if points:
        print(f"Uploading {len(points)} points to Qdrant...")
        qdrant_client.upsert(
            collection_name="rag_embedding",
            points=points
        )
        print(f"Successfully uploaded {len(points)} points to Qdrant!")

        # Verify the upload
        collection_info = qdrant_client.get_collection("rag_embedding")
        print(f"Collection now has {collection_info.points_count} points")
    else:
        print("No points were created due to embedding errors")

if __name__ == "__main__":
    populate_qdrant()
    print("Local Qdrant is now populated with sample content for immediate testing!")