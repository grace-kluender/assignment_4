pipeline {
    agent none
    
    environment {
        // Secret Text credential in Jenkins that stores your Slack Incoming Webhook URL
        SLACK_WEBHOOK = credentials('slack-webhook')
        SLACK_CHANNEL = '#all-devops'
    }

    stages {
        stage('Checkout') {
            agent { label 'test'}
            steps {
                // Get code from whichever branch the trigger came from
                checkout scm 
                echo "Branch: ${BRANCH_NAME}"
            }
        }

        stage('SonarQube + Quality Gate') {
            agent { label 'deploy' }
            steps {
                checkout scm
                script {
                    withCredentials([string(credentialsId: '70bbda20-e8b7-46be-95b7-955d0cbc407a', variable: 'SONAR_TOKEN')]) {
                        sh '''
                            docker run --rm \
                                --platform linux/amd64 \
                                --network assignment_4_backend \
                                -e SONAR_HOST_URL=http://sonarqube:9000 \
                                -e SONAR_TOKEN=${SONAR_TOKEN} \
                                -v "$(pwd)":/usr/src \
                                sonarsource/sonar-scanner-cli \
                                -Dsonar.qualitygate.wait=true \
                                -Dsonar.qualitygate.timeout=300
                        '''
                    }
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

    post {
        success {
            node('deploy') {
                withCredentials([string(credentialsId: 'slack-webhook', variable: 'SLACK_WEBHOOK')]) {
                    sh '''
                        curl -X POST -H "Content-type: application/json" \
                        --data "{\"text\":\"✅ SUCCESS: ${JOB_NAME} #${BUILD_NUMBER} (${BRANCH_NAME})\\n${BUILD_URL}\"}" \
                        "$SLACK_WEBHOOK"
                    '''
                }
            }
        }

        failure {
            node('deploy') {
                withCredentials([string(credentialsId: 'slack-webhook', variable: 'SLACK_WEBHOOK')]) {
                    sh '''
                        curl -X POST -H "Content-type: application/json" \
                        --data "{\"text\":\"❌ FAILURE: ${JOB_NAME} #${BUILD_NUMBER} (${BRANCH_NAME})\\nConsole: ${BUILD_URL}console\"}" \
                        "$SLACK_WEBHOOK"
                    '''
                }
            }   
        }
    }
}
