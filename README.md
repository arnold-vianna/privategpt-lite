/source_documents dir is were data is stored

after adding new data run

run the ingest.py to load the data


python3 -m venv venv-name
source venv-name/bin/activate
pip install -r requirements.txt 

run the ingest.py to load the data

docker build -t arnoldvianna/privategpt-lite .
docker run -p 8501:8501 arnoldvianna/privategpt-lite

docker tag arnoldvianna/privategpt-lite arnoldvianna/privategpt-lite:latest

docker push arnoldvianna/privategpt-lite:latest

or i used  sudo docker-compose up -d 


http://localhost:8501


Step 8: Push to Docker Hub


docker tag arnoldvianna/privategpt-lite arnoldvianna/privategpt-lite:latest
docker push arnoldvianna/privategpt-lite:latest


PrivateGPT Lite is designed to run efficiently with minimal resources, requiring no GPU, making it perfect for smooth operation on CPU alone. This lightweight setup allows you to harness the power of private, local AI processing without heavy hardware demands. You can easily expand its knowledge by adding more items—such as documents, JSON files, or SQLite databases—through a simple ingestion process, updating the FAISS index to include new content. Ideal as an intelligent cheat sheet or smart index, it enables quick retrieval of commands, descriptions, or relevant information, serving as a personalized knowledge base for tasks like network administration or coding, all accessible via an intuitive Streamlit interface.