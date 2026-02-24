import boto3
import os
import networkx as nx
import matplotlib.pyplot as plt
import io
import uuid
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(env_path, override=True)


def generate_and_upload_graph(graph: nx.DiGraph) -> str:
    """
    Generates a matplotlib diagram of the graph, uploads it to S3 (or falls back locally),
    and returns a public URL.
    """
    # 1. Draw Graph
    plt.figure(figsize=(8, 6))
    
    # Custom coloring based on node type
    color_map = []
    for node in graph:
        node_type = graph.nodes[node].get('type')
        if node_type == 'process':
            color_map.append('skyblue')
        else:
            color_map.append('lightgreen')
            
    pos = nx.spring_layout(graph, seed=42)
    nx.draw(graph, pos, with_labels=True, node_color=color_map, 
            node_size=2000, font_weight='bold', font_size=12,
            arrowsize=20)
    
    # 2. Save to Buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight")
    buf.seek(0)
    plt.close()
    
    filename = f"graph_{uuid.uuid4().hex[:8]}.png"
    
    # 3. Upload to S3 (if properly configured)
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "cloud-deadlock-visuals")
    
    if AWS_ACCESS_KEY and AWS_SECRET_KEY: # Only try to upload if we explicitely passed or know we have credentials
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
        )
        s3_client.upload_fileobj(
            buf, 
            AWS_BUCKET_NAME, 
            filename,
            ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read'}
        )
        # Return S3 URL
        return f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{filename}"
    else:
        raise Exception("AWS Credentials missing from environment!")
        
    # 4. Fallback: Save Locally for Development
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_DIR = os.path.join(BASE_DIR, "static")
    os.makedirs(STATIC_DIR, exist_ok=True)
    local_path = os.path.join(STATIC_DIR, "latest_graph.png")
    with open(local_path, "wb") as f:
        f.write(buf.getvalue())
        
    # Return local API URL for the image
    return "/static/latest_graph.png"
