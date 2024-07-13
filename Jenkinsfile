pipeline {
    agent any
    environment {
        DOCKER_IMAGE='my-docker-image:latest'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url : 'https://github.com/vishal-savnani/my-first-deb-ci.git'
            }
        }
    
        stage('Build docker image'){
            steps {
                script {
                    docker.build("${env.DOCKER_IMAGE}",'-f Dockerfile .')
                }
            }
        }
        stage('Build Debian Package') {
            steps {
                script {
                    docker.image("${env.DOCKER_IMAGE}").inside {
                        sh '''

                        #move to source directory

                        cd src

                        #install depdencies

                        apt-get-update

                        apt-get-install -y build-essential devscripts debhelper

                        #build the package

                        dpkg-buildpackage -us -uc -n

                        #move the build package to roott

                        mv ../*.deb ../
                        '''
                    }
                }
            }
        }
    }

        post {
            always {
                archiveArtifacts artifacts: '*.deb', allowEmptyArchive: true
            }
        }
}