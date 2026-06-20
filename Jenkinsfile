pipeline{
    agent any
    stages{
        stage("Stage: Git checkout"){
            steps{
                script{
                    echo "pulling the code from GitHub..."
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'GitHub-token', url: 'https://github.com/amaanrzv39/Anime-Recommendation-System.git']])
                }
            }
        }
    }
}