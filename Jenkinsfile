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

        stage('Build (Docker)') {
            agent { label 'deploy' }
            steps {
                checkout scm
                
                script {
                    def shortCommit = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    // Versioning with: Jenkins' auto-incremented build ID + Git SHA 
                    env.VERSION = "1.0.${env.BUILD_NUMBER}-${shortCommit}"
                    env.IMAGE_REPO = "flask-app"
                    env.IMAGE_TAG  = "${env.IMAGE_REPO}:${env.VERSION}"
                    echo "Building image: ${env.IMAGE_TAG}"
                }

                sh '''
                mkdir -p dist
                docker build -t ${IMAGE_TAG} -f ./app/Dockerfile ./app
                echo ${IMAGE_TAG} > dist/image-tag.txt
                echo ${VERSION} > dist/version.txt
                git rev-parse HEAD > dist/git-commit.txt
                '''
                archiveArtifacts artifacts: 'dist/*', fingerprint: true
            }
        }

        stage('Main-only stage') {
            when { branch 'main' }
            agent { label 'deploy' }
            steps {
                sh 'echo "This stage only runs on main Q3 requirement"'
            }
        }
    }
}