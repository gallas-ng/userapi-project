# **UserAPI DevOps Project**

## 1. Project Overview

The UserAPI project is a complete, end-to-end DevOps solution designed to demonstrate modern software delivery practices, covering application development, automated testing, continuous integration, infrastructure as code, containerization, and Kubernetes orchestration.

The system is built around a simple yet extensible User Management API implemented in Python (FastAPI) and backed by PostgreSQL. The API exposes full CRUD operations and includes a `/health` endpoint for automated validation and monitoring as well as routes documentation with SwaggerUI.

This project implements:
- Continuous Testing  
- Continuous Integration (CI)  
- Infrastructure as Code (IaC) with Vagrant + Ansible  
- Docker image creation and Docker Compose orchestration  
- Kubernetes deployment via Minikube  
- Full project documentation and reproducible deployment steps  

## 2. Description of Tasks Completed

### 2.1 Architecture Overview

This project follows a modular DevOps-oriented structure designed to demonstrate the full CI/CD lifecycle, containerization, orchestration, and infrastructure-as-code practices.

Below is an overview of the final project structure:

``` code
userapi-project
├── .github
│   └── workflows
│       ├── ci.yml
│       └── docker-publish.yml
├── .gitignore
├── docker-compose.yaml
├── iac
│   ├── playbooks
│   │   ├── roles
│   │   │   ├── app
│   │   │   │   └── tasks
│   │   │   │       └── main.yml
│   │   │   ├── db
│   │   │   │   ├── handlers
│   │   │   │   │   └── main.yml
│   │   │   │   └── tasks
│   │   │   │       └── main.yml
│   │   │   ├── health
│   │   │   │   └── tasks
│   │   │   │       └── main.yml
│   │   │   └── python
│   │   │       └── tasks
│   │   │           └── main.yml
│   │   └── site.yml
│   └── Vagrantfile
├── images
├── k8s
│   ├── configmap.yaml
│   ├── namespace.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── secret.yaml
│   ├── userapi-deployment.yaml
│   └── userapi-service.yaml
├── README.md
└── userapi
    └── src
        ├── app
        │   ├── crud.py
        │   ├── db.py
        │   ├── main.py
        │   ├── requirements.txt
        │   ├── schemas.py
        │   ├── tests
        │   │   ├── test_api_crud.py
        │   │   ├── test_api_health.py
        │   │   ├── test_unit_basic.py
        │   │   ├── __init__.py
        │   ├── __init__.py
        └── Dockerfile
```

### 2.2 Detailed Work Description

#### A -  Application Development

- FastAPI CRUD application for user management. 

  <img src="images/home.png" alt="API Home" width="300"/>

- PostgreSQL database integration using `asyncpg`.
- Includes:
  - health check endpoint

    <img src="images/health.png" alt="API Health" width="600"/>

  - fully isolated routers
  - database models
  - error handling
- see : `/userapi/src/app` for more details
- As FastAPI comes with Swagger Doc API, navigate to `/docs` after deploying the app to try functions.

    <img src="images/swaggerui.png" alt="API Swaggeui" width="600"/>


#### B - Automated Testing
Tests implemented:
- **Unit Tests** – validation logic, utilities
- **API Tests** – endpoints with test client
- **Database Tests** – connection & integration
- see : `/userapi/src/app/tests` 

  <img src="images/tests.png" alt="API tests" width="600"/>


#### C - Continuous Integration (CI)
- GitHub Actions workflow: 
    - app workflow: `.github/workflows/ci.yml`
    - app image workflow: `.github/workflows/docker-publish.yml`
- Automated steps:
  - install dependencies
  - run tests

  <img src="images/ci.png" alt="API ci" width="600"/>

  - build Docker image after change
  - push to Docker Hub on `master`

  <img src="images/docker_ci.png" alt="API Docker ci" width="600"/>


#### D - Containerization (Docker)
- Dockerfile:
  - light Python base image
  - installs dependencies
  - exposes port 8000
  - starts FastAPI with Uvicorn

  <img src="images/docker_image.png" alt="API image" width="300"/>

  - Image pushed to Docker Hub:
  - `https://docker.io/gallasng/userapi:latest`

  <img src="images/docker_hub.png" alt="API docker hub" width="600"/>

#### E - Infrastructure as Code (Vagrant + Ansible)
  - Vagrant VM: Ubuntu 22.04
  - Ansible provisioning:
  - install Python & PostgreSQL
  - deploy application via sync folder
  - systemd service created

  <img src="images/vagrant.png" alt="API iac" width="600"/>

  - health check verification

  <img src="images/vagrant_check.png" alt="API iac check" width="600"/>

#### F - Kubernetes Deployment
Resources created:
- namespace: `userapi`
- deployments:
  - **userapi**
  - **postgres**

  <img src="images/pods.png" alt="API pods"/>

- services:
  - ClusterIP for postgres
  - NodePort for userapi

  <img src="images/node_ports.png" alt="API Node ports"/>

- Verified deployment 

  <img src="images/minikube.png" alt="API Minikube test" width="400"/>

## 3. Instructions to Run the Project
Clone the project (run the following commands at project root)
### 3.1 Run Locally (without Docker)
  * Make sure to have a running instance of postgres with:
 user = vagrant
 password = password
 db = userdb
 port = 5432
 - orelse you can edit `db.py` with your own existing variables
```bash
cd userapi
python -m venv venv
.venv\Source\activate

cd userapi\src
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API URL:
http://localhost:8000

### 3.2 Run Using Docker Compose
```bash
docker-compose up --build
```
API URL:
http://localhost:8000

### 3.3 Build Image Manually
``` bash
docker build -t userapi /userapi/src/
```
### 3.4 Run with Vagrant + Ansible 
[Install Vagrant](https://developer.hashicorp.com/vagrant/downloads/) following the instructions depending on your OS.
```bash
cd iac
vagrant up
```
You should be able to access the app through the VM (eg. ssh) using curl and locally at http://localhost:8000/ .
``` bash
vagrant ssh
curl localhost:8000/health
```
### 3.5 Deploy on Kubernetes (Minikube) 
[Install Minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) following the instructions depending on your OS.
1. Start your cluster 
```bash
minikube start
```

2. Apply namespace and config
```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
```
3. Apply deployments
```bash
kubectl apply -f k8s/postgres-deployment.yaml
kubectl apply -f k8s/userapi-deployment.yaml
```
4. Apply services
```bash
kubectl apply -f k8s/postgres-service.yaml
kubectl apply -f k8s/userapi-service.yaml
```

5. Get NodePort
```bash
kubectl get svc -n userapi

Expected output:
userapi   NodePort   ... 8000:30080/TCP
```

5. Get you minikube Ip
```bash
minikube ip

Expected output:
192.168.59.1**
```

6. Access the app with the forwarded port and your minikube ip :

    http://192.168.59.101:30080/health `(replace with your own minikube ip)`
    
    http://192.168.59.101:30080/docs  `(see the swagger ui API)`

## 4. Links
Docker Hub Image:
https://hub.docker.com/r/gallasng/userapi

GitHub Repository:
https://github.com/gallas-ng/userapi-project


## 5. Authorship
**Project completed by:**
 - **Falilou Niang - Katy Mayoro Fall**
 - **@Data ScienceTech Institute**
 - **Course: DevOps – DSTI**
 - **Year: 2025**

>All code, automation scripts, tests, and documentation were developed as part of the academic requirements of the DevOps module.
