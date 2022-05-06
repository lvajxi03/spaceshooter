pipeline {
    agent any

    stages {
        stage('Clean') {
            steps {
                sh 'git clean -f -d -x .'
            }
        }
        stage('Checkout') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('')])])
                }
                git url: 'https://github.com/lvajxi03/spaceshooter.git/',
                branch: 'main'
            }
        }
        stage('Update version') {
	    steps {
                sh 'sed -i "s/%TAG%/0.0.0.0/g" README.md'
	        sh 'sed -i "s/%TAG%/0.0.0.0/g" setup.cfg'
                sh 'sed -i "s/%TAG%/0.0.0.0/g" setup.py'
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
	stage ('Install') {
	    steps {
                sh 'python -m pip uninstall spaceshooter || exit 0'
                sh 'python -m pip install dist/spaceshooter*.whl'
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
                    archiveArtifacts 'htmlcov/*'
                }
            }
        }
    }
}
