import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import time
import logging
import uuid

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Cohere client
cohere_api_key = os.getenv("COHERE_API_KEY")
if not cohere_api_key:
    raise ValueError("COHERE_API_KEY environment variable is required")
co = cohere.Client(cohere_api_key)

# Initialize Qdrant client
qdrant_url = os.getenv("QDRANT_URL")
qdrant_api_key = os.getenv("QDRANT_API_KEY")
if not qdrant_url or not qdrant_api_key:
    raise ValueError("QDRANT_URL and QDRANT_API_KEY environment variables are required")
qdrant_client = QdrantClient(
    url=qdrant_url,
    api_key=qdrant_api_key,
    timeout=60.0,  # Set timeout to 60 seconds
)


def get_all_urls(root_url, max_pages=100):
    """
    Crawl the Docusaurus site and return all discovered URLs.

    Args:
        root_url (str): The root URL to start crawling from
        max_pages (int): Maximum number of pages to crawl

    Returns:
        list: List of discovered URLs
    """
    logger.info(f"Starting to crawl from {root_url}")
    urls = set()
    to_visit = [root_url]
    visited = set()

    root_domain = urlparse(root_url).netloc

    while to_visit and len(urls) < max_pages:
        current_url = to_visit.pop(0)

        if current_url in visited:
            continue

        visited.add(current_url)

        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            urls.add(current_url)

            # Find all links on the page
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(current_url, href)

                # Only follow links within the same domain
                if urlparse(absolute_url).netloc == root_domain:
                    if absolute_url not in visited and absolute_url not in to_visit:
                        to_visit.append(absolute_url)

        except Exception as e:
            logger.error(f"Error crawling {current_url}: {str(e)}")
            continue

    logger.info(f"Discovered {len(urls)} URLs")
    return list(urls)


def extract_text_from_url(url):
    """
    Extract text content from a given URL.

    Args:
        url (str): URL to extract text from

    Returns:
        dict: Dictionary containing title and content
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Extract title
        title = soup.title.string if soup.title else "No Title"

        # Extract main content (try to focus on main content areas)
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='container') or soup

        # Get text content
        text = main_content.get_text(separator=' ', strip=True)

        # Clean up text (remove extra whitespace)
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return {
            'url': url,
            'title': title,
            'content': text
        }
    except Exception as e:
        logger.error(f"Error extracting text from {url}: {str(e)}")
        return {
            'url': url,
            'title': 'Error',
            'content': ''
        }


def chunk_text(text, chunk_size=512, overlap=50):
    """
    Split text into chunks of specified size with overlap.

    Args:
        text (str): Text to chunk
        chunk_size (int): Size of each chunk (in characters)
        overlap (int): Overlap between chunks (in characters)

    Returns:
        list: List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # Move start position by (chunk_size - overlap)
        start = end - overlap

        # If the remaining text is less than chunk_size, take it as the last chunk
        if len(text) - start < chunk_size:
            if start < len(text):
                chunks.append(text[start:])
            break

    return chunks


def embed(texts):
    """
    Generate embeddings for a list of texts using Cohere.

    Args:
        texts (list): List of texts to embed

    Returns:
        list: List of embedding vectors
    """
    try:
        response = co.embed(
            texts=texts,
            model="embed-english-v3.0",  # Using a standard Cohere embedding model
            input_type="search_document"  # Appropriate for document search
        )
        return response.embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        return []


def create_collection(collection_name="rag_embedding"):
    """
    Create a Qdrant collection for storing embeddings.

    Args:
        collection_name (str): Name of the collection to create
    """
    try:
        # Check if collection already exists
        try:
            qdrant_client.get_collection(collection_name)
            logger.info(f"Collection '{collection_name}' already exists")
            return
        except:
            pass  # Collection doesn't exist, so we'll create it

        # Create the collection
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Cohere embeddings are 1024-dimensional for embed-english-v3.0
                distance=models.Distance.COSINE
            )
        )
        logger.info(f"Created collection '{collection_name}' successfully")
    except Exception as e:
        logger.error(f"Error creating collection '{collection_name}': {str(e)}")
        raise


def save_chunk_to_qdrant(collection_name, chunk_id, embedding, metadata):
    """
    Save a text chunk with its embedding to Qdrant.

    Args:
        collection_name (str): Name of the collection
        chunk_id (str): Unique ID for this chunk
        embedding (list): Embedding vector
        metadata (dict): Metadata to store with the chunk
    """
    try:
        qdrant_client.upsert(
            collection_name=collection_name,
            points=[
                models.PointStruct(
                    id=chunk_id,
                    vector=embedding,
                    payload=metadata
                )
            ]
        )
        logger.info(f"Saved chunk {chunk_id} to Qdrant")
    except Exception as e:
        logger.error(f"Error saving chunk {chunk_id} to Qdrant: {str(e)}")
        raise


def search_similar_content(query_text, collection_name="rag_embedding", limit=5):
    """
    Search for content similar to the query text in Qdrant.

    Args:
        query_text (str): Text to search for similar content
        collection_name (str): Name of the collection to search in
        limit (int): Number of results to return

    Returns:
        list: List of similar content with metadata and scores
    """
    try:
        # Generate embedding for the query text
        query_embeddings = embed([query_text])
        if not query_embeddings or len(query_embeddings) == 0:
            logger.error("Error generating embedding for query text")
            return []

        query_vector = query_embeddings[0]

        # Perform search in Qdrant using query_points
        search_results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,  # Include metadata
            with_vectors=False  # We don't need the vectors back
        )

        # Format results
        results = []
        for hit in search_results.points:
            result = {
                'id': hit.id,
                'score': hit.score,
                'payload': hit.payload,
                'url': hit.payload.get('url', 'N/A'),
                'title': hit.payload.get('title', 'N/A'),
                'content_snippet': hit.payload.get('content', '')[:200] + '...' if len(hit.payload.get('content', '')) > 200 else hit.payload.get('content', '')
            }
            results.append(result)

        logger.info(f"Found {len(results)} similar results for query: '{query_text[:50]}...'")
        return results

    except Exception as e:
        logger.error(f"Error searching for similar content: {str(e)}")
        return []


def search_with_filters(query_text, collection_name="rag_embedding", limit=5, filters=None):
    """
    Search for content with optional filters.

    Args:
        query_text (str): Text to search for similar content
        collection_name (str): Name of the collection to search in
        limit (int): Number of results to return
        filters (dict): Optional filter conditions

    Returns:
        list: List of similar content with metadata and scores
    """
    try:
        # Generate embedding for the query text
        query_embeddings = embed([query_text])
        if not query_embeddings or len(query_embeddings) == 0:
            logger.error("Error generating embedding for query text")
            return []

        query_vector = query_embeddings[0]

        # Build filter if provided
        qdrant_filter = None
        if filters:
            conditions = []
            for key, value in filters.items():
                # Create a 'must' condition for each filter
                condition = models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value)
                )
                conditions.append(condition)

            if conditions:
                qdrant_filter = models.Filter(must=conditions)

        # Perform search in Qdrant with filters using query_points
        search_results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            query_filter=qdrant_filter,  # Apply filters
            limit=limit,
            with_payload=True,  # Include metadata
            with_vectors=False  # We don't need the vectors back
        )

        # Format results
        results = []
        for hit in search_results.points:
            result = {
                'id': hit.id,
                'score': hit.score,
                'payload': hit.payload,
                'url': hit.payload.get('url', 'N/A'),
                'title': hit.payload.get('title', 'N/A'),
                'content_snippet': hit.payload.get('content', '')[:200] + '...' if len(hit.payload.get('content', '')) > 200 else hit.payload.get('content', '')
            }
            results.append(result)

        logger.info(f"Found {len(results)} filtered results for query: '{query_text[:50]}...'")
        return results

    except Exception as e:
        logger.error(f"Error searching for similar content with filters: {str(e)}")
        return []


def query_points_search(query_text, collection_name="rag_embedding", limit=5):
    """
    Advanced search using the newer query_points method.

    Args:
        query_text (str): Text to search for similar content
        collection_name (str): Name of the collection to search in
        limit (int): Number of results to return

    Returns:
        list: List of similar content with metadata and scores
    """
    try:
        # Generate embedding for the query text
        query_embeddings = embed([query_text])
        if not query_embeddings or len(query_embeddings) == 0:
            logger.error("Error generating embedding for query text")
            return []

        query_vector = query_embeddings[0]

        # Perform query using the newer query_points method
        query_results = qdrant_client.query_points(
            collection_name=collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True,  # Include metadata
            with_vectors=False  # We don't need the vectors back
        )

        # Format results
        results = []
        for point in query_results.points:
            result = {
                'id': point.id,
                'score': point.score,
                'payload': point.payload,
                'url': point.payload.get('url', 'N/A'),
                'title': point.payload.get('title', 'N/A'),
                'content_snippet': point.payload.get('content', '')[:200] + '...' if len(point.payload.get('content', '')) > 200 else point.payload.get('content', '')
            }
            results.append(result)

        logger.info(f"Found {len(results)} results using query_points for: '{query_text[:50]}...'")
        return results

    except Exception as e:
        logger.error(f"Error querying points: {str(e)}")
        return []


def main():
    """
    Main function to execute the entire process:
    1. Get all URLs from the Docusaurus site
    2. Extract text from each URL
    3. Chunk the text
    4. Generate embeddings
    5. Store in Qdrant
    """
    logger.info("Starting the URL ingestion, embedding, and storage process")

    # Configuration
    root_url = os.getenv("ROOT_URL", "https://hackathon-ai-book-fawn.vercel.app/")
    collection_name = "rag_embedding"
    chunk_size = int(os.getenv("CHUNK_SIZE", "512"))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "50"))

    # Step 1: Create collection in Qdrant
    create_collection(collection_name)

    # Step 2: Get all URLs from the site
    urls = get_all_urls(root_url)

    # Step 3: Process each URL
    for i, url in enumerate(urls):
        logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

        # Extract text from the URL
        page_data = extract_text_from_url(url)

        if not page_data['content']:
            logger.warning(f"No content extracted from {url}")
            continue

        # Chunk the content
        chunks = chunk_text(page_data['content'], chunk_size, chunk_overlap)

        # Process each chunk
        for j, chunk in enumerate(chunks):
            # Generate embedding
            embeddings = embed([chunk])

            if not embeddings or len(embeddings) == 0:
                logger.warning(f"No embeddings generated for chunk {j} of {url}")
                continue

            embedding = embeddings[0]  # Get the first (and should be only) embedding

            # Prepare metadata
            metadata = {
                'url': page_data['url'],
                'title': page_data['title'],
                'chunk_index': j,
                'original_content_length': len(page_data['content']),
                'chunk_length': len(chunk)
            }

            # Generate a unique ID for this chunk
            # Use a UUID to ensure valid format for Qdrant
            chunk_id = str(uuid.uuid4())  # Generate a unique UUID

            # Save to Qdrant
            save_chunk_to_qdrant(collection_name, chunk_id, embedding, metadata)

            # Be respectful to APIs - add a small delay
            time.sleep(0.1)

    logger.info("Completed the URL ingestion, embedding, and storage process")

    # Example search usage (uncomment to test after ingestion)
    # print("\n--- Testing search functionality ---")
    # sample_query = "What is AI?"
    # results = search_similar_content(sample_query, collection_name=collection_name, limit=3)
    # for i, result in enumerate(results):
    #     print(f"Result {i+1}: Score: {result['score']:.4f}, Title: {result['title']}, URL: {result['url']}")


if __name__ == "__main__":
    main()