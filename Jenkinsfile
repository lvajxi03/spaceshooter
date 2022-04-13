pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('')])])
                }
                git url: 'https://github.com/lvajxi03/spaceshooter.git/',
                branch: 'main'
            }
        }
        stage('Update tools') {
            steps {
                sh 'python -m pip install --upgrade build'
                sh 'python -m pip install --upgrade pytest pytest-cov coverage'
                sh 'python -m pip install --upgrade pylint'
            }
        }
        stage('Build') {
            steps {
                sh 'python -m build'
            }
            post {
                success {
                    archiveArtifacts 'dist/*.whl'
                    archiveArtifacts 'dist/*.tar.gz'
                }
            }
        }
        stage ('Lint') {
            steps {
                sh 'python -m pylint $(find pysrc -name "*.py")'
            }
        }
        stage ('Unit Tests') {
            steps {
                sh 'PYTHONPATH=pysrc python -m pytest pytests/ --cov'
            }
        }
        stage ('Coverage') {
            steps {
                sh 'python -m coverage html'
            }
            post {
                success {
                    archiveArtifacts 'htmlcov'
                }
            }
        }
    }
}
