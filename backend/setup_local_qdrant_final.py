"""
Setup script for local Qdrant instance to replace the cloud one.
This script creates a local Qdrant instance that doesn't require cloud connectivity.
"""

import os
import subprocess
import time
from pathlib import Path
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_local_qdrant():
    """Setup local Qdrant instance"""

    # Create local storage directory
    local_storage_path = Path("qdrant_data")
    local_storage_path.mkdir(exist_ok=True)

    print("Setting up local Qdrant instance...")

    # Connect to local Qdrant (will create if doesn't exist)
    try:
        client = QdrantClient(path="./qdrant_data")  # Local persistent instance
        print("Connected to local Qdrant instance successfully!")

        # Check if collection exists, if not create it
        collection_name = "rag_embedding"

        try:
            # Try to get collection info
            collection_info = client.get_collection(collection_name)
            print(f"Collection '{collection_name}' already exists with {collection_info.points_count} points")
        except:
            # Collection doesn't exist, create it
            print(f"Creating collection '{collection_name}'...")

            from qdrant_client.http import models

            client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=1024,  # Cohere embeddings are 1024-dimensional
                    distance=models.Distance.COSINE
                )
            )
            print(f"Collection '{collection_name}' created successfully!")

        # Update the .env file to use local instance
        update_env_files()

        print("")
        print("SUCCESS: Local Qdrant setup completed!")
        print("Please restart your backend server to use the local Qdrant instance")
        print("The system will now use local storage instead of cloud Qdrant")

    except Exception as e:
        print(f"Error setting up local Qdrant: {e}")
        return False

    return True

def update_env_files():
    """Update environment files to use local Qdrant"""

    # Update backend .env file
    backend_env_path = Path("backend/.env")
    if backend_env_path.exists():
        env_content = backend_env_path.read_text()

        # Replace QDRANT_URL with local instance
        if "QDRANT_URL=" in env_content:
            # Find the line and replace it
            lines = env_content.split('\n')
            updated_lines = []
            for line in lines:
                if line.startswith('QDRANT_URL='):
                    updated_lines.append('QDRANT_URL=http://localhost:6333')  # Local instance
                else:
                    updated_lines.append(line)
            new_env_content = '\n'.join(updated_lines)
            backend_env_path.write_text(new_env_content)
            print("Updated backend/.env to use local Qdrant")

    # Update root .env file
    root_env_path = Path("../.env")
    if root_env_path.exists():
        env_content = root_env_path.read_text()

        # Replace QDRANT_URL with local instance
        if "QDRANT_URL=" in env_content:
            lines = env_content.split('\n')
            updated_lines = []
            for line in lines:
                if line.startswith('QDRANT_URL='):
                    updated_lines.append('QDRANT_URL=http://localhost:6333')  # Local instance
                else:
                    updated_lines.append(line)
            new_env_content = '\n'.join(updated_lines)
            root_env_path.write_text(new_env_content)
            print("Updated .env to use local Qdrant")

if __name__ == "__main__":
    print("Setting up local Qdrant instance to solve connectivity issues...")
    setup_local_qdrant()