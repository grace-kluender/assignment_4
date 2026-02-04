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

        stage('SonarQube + Quality Gate') {
            agent { label 'deploy' }
            steps {
                checkout scm

                withSonarQubeEnv('sonarqube') {
                    sh '''
                        set -e
                        echo "Running SonarScanner in Docker..."

                        # Run scanner in a named container so we can copy report-task.txt out
                        docker rm -f sonar-scanner || true

                        docker run --name sonar-scanner \
                        -e SONAR_HOST_URL="$SONAR_HOST_URL" \
                        -e SONAR_TOKEN="$SONAR_AUTH_TOKEN" \
                        -v "$WORKSPACE:/usr/src" \
                        sonarsource/sonar-scanner-cli

                        echo "Copying report-task.txt into Jenkins workspace..."
                        docker cp sonar-scanner:/usr/src/.scannerwork/report-task.txt "$WORKSPACE/report-task.txt" || true
                        docker rm -f sonar-scanner || true

                        echo "Report-task.txt copied? (listing)"
                        ls -la "$WORKSPACE" | grep report-task || true
                    '''
                }

                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
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