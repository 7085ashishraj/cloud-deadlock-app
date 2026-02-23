import boto3
import os
import networkx as nx
import matplotlib.pyplot as plt
import io
import uuid

# Configuration (In production, load these from .env)
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", "cloud-deadlock-visuals")

# Initialize S3 Client gracefully
try:
    if AWS_ACCESS_KEY and AWS_SECRET_KEY:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
        )
    else:
        s3_client = boto3.client('s3') # Triggers default AWS profile if configured
except Exception:
    s3_client = None

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
    try:
        if s3_client and AWS_ACCESS_KEY: # Only try to upload if we explicitely passed or know we have credentials
            s3_client.upload_fileobj(
                buf, 
                AWS_BUCKET_NAME, 
                filename,
                ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read'}
            )
            # Return S3 URL
            return f"https://{AWS_BUCKET_NAME}.s3.amazonaws.com/{filename}"
    except Exception as e:
        print(f"S3 Upload failed: {e}. Falling back to local storage.")
        
    # 4. Fallback: Save Locally for Development
    os.makedirs("static", exist_ok=True)
    local_path = os.path.join("static", "latest_graph.png")
    with open(local_path, "wb") as f:
        f.write(buf.getvalue())
        
    # Return local API URL for the image
    return "http://localhost:8000/static/latest_graph.png"
