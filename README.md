<p align=center>
  <br>
  <a href="https://github.com/arnold-vianna?tab=repositories" target="_blank"><img src="https://avatars.githubusercontent.com/u/113808475?v=4"/></a>
  <br>
  <span>check out my website <a href="https://arnold-vianna.github.io/">arnold-vianna.github.io</a></span>
  <br>
</p>



#  PrivateGPT Lite — Ask Your Documents Locally



<img src="https://i.imgur.com/5R9qHpK.png" title="source: imgur.com" /></a>

## Key Features 

- ⚙️ 100% CPU-only — no GPU or cloud required  

- 📚 Easily ingest `.json`, `.txt`, or `.sqlite` files  

- 🔍 FAISS-powered local semantic search  

- 📖 Query your knowledge base using a Streamlit interface 

- 🧠 Perfect for cheat sheets, command lookup, network admin, coding docs  

- 🔐 Keeps all your data private and offline  

- 🚀 Run from Docker or source 


## via dockerhub command

 ```console
sudo docker run -d -p 8501:8501 arnoldvianna/privategpt-lite
```

## Setup 


```console
# Clone the repo
git clone https://github.com/arnoldvianna/privategpt-lite.git
cd privategpt-lite
```

```console
# Build the Docker image
docker build -t privategpt-lite .
```

```console
# Run the container
docker run -p 8501:8501 arnoldvianna/privategpt-lite:latest
```




##  💡 Use Cases



    🔧 Personal sysadmin or dev cheat sheet

    📚 Index and search your own documentation

    🚫 Offline, private alternative to ChatGPT

    👨‍💻 Smart helper for learning, coding, or reverse engineering






##  Runing

* Qr  image is saved to the sane dir ad the app.py

* place the path to the URL in line 77

* place the path to the logo in line 78