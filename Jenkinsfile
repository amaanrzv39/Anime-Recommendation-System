pipeline{
    agent any
    environment{
        VENV_DIR = "venv"
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
                    shs'''
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
                        shs'''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }
    }
}