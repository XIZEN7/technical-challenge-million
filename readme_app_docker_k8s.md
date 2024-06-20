# Technical Challenge Million

This repository contains the code for Technical Challenge Million and UP.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/XIZEN7/technical-challenge-million
    ```

2. **Navigate to the project directory**:

    ```bash
    cd technical-challenge-million
    ```

3. **Make sure you have Docker and Docker Compose installed on your system**. If you don't have them installed, you can find instructions to install them [here](https://docs.docker.com/get-docker/) and [here](https://docs.docker.com/compose/install/).

4. **Build the Docker image**:

    ```bash
    docker-compose build
    ```

5. **Start the application using Docker Compose**:

    ```bash
    docker-compose up -d
    ```

6. If deploying to Kubernetes, ensure the Kubernetes namespace `tech-prod` exists:

   ```bash
   kubectl create namespace tech-prod || true

7. Deploy the application using Kubernetes:
    ```bash
    kubectl apply -f k8s.yaml
    ```
The application will start running in the Docker container. You can access the application in your web browser at `http://localhost:8080`.

8. **To stop the application**:

    - Press `Ctrl + C` in the terminal where Docker Compose is running.
    - Alternatively, you can run the following command to stop the application and remove the Docker containers:

        ```bash
        docker-compose down
        ```
    - To delete the Kubernetes deployment (if deployed):
        ```bash
        kubectl delete -f k8s.yaml
        ```

## API Endpoints

- `/`: Home page of the application.
- `/upload_csv_form`: Page to upload CSV files.
- `/upload_csv`: Endpoint to upload CSV files to the application.
- `/metrics/departments_above_mean`: Endpoint to get data about departments above the mean.
- `/metrics/hired_by_department_and_job`: Endpoint to get data about hires by department and job.

## Testing

To run the tests:

1. Activate your virtual environment (if not already active).
    - Create virtual environment
    ```bash
    python -m venv venv
    ```
    - Activate virtual environment
    ```bash
    source venv/bin/activate
    ```
    - Desactivate virtual environment
    ```bash
    deactivate
    ```
2. Run the tests using pytest:

    ```bash
    pytest test/
    ```
