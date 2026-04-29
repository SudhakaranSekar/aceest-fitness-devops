# ACEest Fitness & Gym - v3.2.4 (Final)

## CI/CD Pipeline - DevOps Assignment (CSIZG514/SEZG514)

### Architecture
- **App**: Flask Web Application (Python)
- **Testing**: Pytest (18 test cases)
- **CI**: Jenkins Pipeline
- **Code Quality**: SonarQube
- **Containerization**: Docker
- **Registry**: Docker Hub
- **Orchestration**: Kubernetes (Minikube)

### Deployment Strategies
1. Rolling Update
2. Blue-Green Deployment
3. Canary Release
4. A/B Testing
5. Shadow Deployment

### How to Run
```bash
pip install -r requirements.txt
python app.py
```
Open: http://localhost:5000
Login: admin / admin

### Run Tests
```bash
pytest test_app.py -v
```

### Docker
```bash
docker build -t aceest-fitness:v3.2.4 .
docker run -p 5000:5000 aceest-fitness:v3.2.4
```
