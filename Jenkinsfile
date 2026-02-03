pipeline {
    agent none

    stages {
        stage('Checkout') {
            agent { label 'test'}
            steps {
                // Get code from whichever branch the trigger came from
                checkout scm 
                echo "Branch: ${BRANCH_NAME}"
            }
        }

        stage('End-to-End Test') {
            agent { label 'test'}
            steps {
                sh 'echo "TODO: end to end test will run here in Q7"'
            }
        }

        stage('Build (placeholder)') {
            agent { label 'deploy' }
            steps {
                sh 'echo "TODO: build artifact / docker image in Q4"'
            }
        }

        stage('Main-only stage') {
            when { branch 'main' }
            agent { label 'deploy' }
            steps {
                sh 'echo "This stage only runs on main Q3 requirement"'
            }
        }

        post {
        always {
            archiveArtifacts artifacts: 'build/libs/**/*.jar', fingerprint: true
            junit 'build/reports/**/*.xml'
        }
    }
}