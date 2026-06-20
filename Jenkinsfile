pipeline{
    agent any
    environment{
        VENV_DIR = "venv"
        GCP_PROJECT = "project-cd8d3620-549d-44e4-ba7"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
        KUBECTL_AUTH_PLUGIN = "/usr/lib/google-cloud-sdk/bin"
    }
    stages{
        stage("Stage: Git checkout"){
            steps{
                script{
                    echo "pulling the code from GitHub..."
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'GitHub-token', url: 'https://github.com/amaanrzv39/Anime-Recommendation-System.git']])
                }
            }
        }
        stage("Stage: Make venv"){
            steps{
                script{
                    echo "Installing the dependencies in the virtual environment..."
                    sh'''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install dvc-gs dvc
                    '''
                }
            }
        }
        stage("Stage: DVC Pull"){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo "Pulling the data from GCS using DVC..."
                        sh'''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }
        stage("Stage: Submit code for build"){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo "Submitting code for build to GCS..."
                        sh'''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud auth configure-docker --quiet
                        gcloud builds submit --tag gcr.io/${GCP_PROJECT}/anime-recommender:latest .
                        '''
                    }
                }
            }
        }
        stage("Stage: Deploy to GKE"){
            steps{
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo "Deploying the application to GKE..."
                        sh'''
                        export PATH=$PATH:${GCLOUD_PATH}:${KUBECTL_AUTH_PLUGIN}
                        gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                        gcloud config set project ${GCP_PROJECT}
                        gcloud container clusters get-credentials autopilot-cluster-1 --region us-central1
                        kubectl apply -f deployment.yaml
                        '''
                    }
                }
            }
        }
    }
}