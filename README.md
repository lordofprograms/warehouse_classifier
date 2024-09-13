## WAREHOUSE SIZE CLASSIFIER
To build docker container:
```
docker build -t warehouse-optimizer .
```
To run docker container:
```
 docker run -p 8000:8000 warehouse-optimizer
```

Also, this API is served, here is the docs:
http://3.127.80.31:8000/docs

It was served in a simple way:
1) Clone git repo
2) Build docker container
3) Run it in detached mode, just add `-d` flag to the command above