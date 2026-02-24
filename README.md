# Cloud Deadlock Detector ⛅🔒

A comprehensive web application designed to simulate, detect, and visualize deadlocks in distributed cloud systems. The application provides a user-friendly interface to build a process-resource graph and utilizes a robust algorithm on the backend to accurately identify deadlock cycles.

## 🚀 Features

*   **Interactive Graph Construction:** Add processes and resources, and create request/allocation edges between them intuitive UI.
*   **Real-time Deadlock Detection:** Instantly analyze the constructed graph to determine if a deadlock state exists.
*   **Visual Representation:** Generates and displays a clear visual representation of the Resource Allocation Graph (RAG), highlighting circular waits.
*   **Cloud Ready Architecture:** Designed with scalable cloud principles. Supports AWS S3 integration for graph image hosting and optimized performance.
*   **Modern Tech Stack:** Built with a resilient FastAPI (Python) backend and a responsive React (Vite) frontend stylized with Tailwind CSS.

## 🛠️ Technology Stack

**Frontend:**
*   [React](https://react.dev/) (v19)
*   [Vite](https://vitejs.dev/) - Next Generation Frontend Tooling
*   [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
*   [Axios](https://axios-http.com/) - Promise-based HTTP client

**Backend:**
*   [FastAPI](https://fastapi.tiangolo.com/) - High-performance web framework for APIs
*   [Uvicorn](https://www.uvicorn.org/) - ASGI web server implementation for Python
*   [NetworkX](https://networkx.org/) - Python package for complex networks and graph theory (used for cycle detection)
*   [SQLAlchemy](https://www.sqlalchemy.org/) - Database toolkit and Object Relational Mapper (ORM)
*   [SQLite](https://sqlite.org/) (Configurable to MySQL)
*   [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - AWS SDK for Python (S3 Integration)
*   [Matplotlib](https://matplotlib.org/) - Comprehensive library for creating static, animated, and interactive visualizations in Python

## 🏃 Getting Started (Local Development)

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   **Node.js** (v18+ recommended) and **npm** or **yarn**
*   **Python** (v3.9+ recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/7085ashishraj/cloud-deadlock-app.git
cd cloud-deadlock-app
```

### 2. Backend Setup

1.  Navigate into the backend directory:
    ```bash
    cd backend
    ```
2.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```
3.  Activate the virtual environment:
    *   **Windows:** `venv\Scripts\activate`
    *   **macOS/Linux:** `source venv/bin/activate`
4.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```
5.  Create a `.env` file in the `backend` directory (optional natively, but required for AWS S3 image generation feature):
    ```env
    AWS_ACCESS_KEY_ID=your_aws_access_key
    AWS_SECRET_ACCESS_KEY=your_aws_secret_key
    AWS_REGION=your_aws_region
    S3_BUCKET_NAME=your_s3_bucket_name
    ```
6.  Start the FastAPI development server:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://localhost:8000`. You can access the interactive Swagger documentation at `http://localhost:8000/docs`.

### 3. Frontend Setup

1.  Open a new terminal window and navigate to the frontend directory:
    ```bash
    cd frontend
    ```
2.  Install the Node.js dependencies:
    ```bash
    npm install
    ```
3.  Start the Vite development server:
    ```bash
    npm run dev
    ```
    The application will typically be accessible at `http://localhost:5173`.

## ☁️ Deployment (AWS EC2 / Ubuntu)

The project includes a ready-to-use deployment script optimized for Ubuntu EC2 instances. It handles the installation of Node.js, Python, Nginx, configures PM2 for process management, and sets up Nginx as a reverse proxy.

1.  Provision an Ubuntu EC2 instance on AWS and SSH into it.
2.  Clone the repository.
3.  Navigate to the project root and execute the deployment script:
    ```bash
    bash deploy.sh
    ```
    *Note: Ensure your EC2 security groups are configured to allow inbound HTTP (Port 80) and HTTPS (Port 443) traffic.*

## 📸 Screenshots

*(You can add screenshots of your application here to make the Readme more appealing.)*

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.
