pipeline {
    agent none
    options { skipDefaultCheckout(true) }
    stages {
        stage('Build and Test') {
            agent {
                docker {
                    image 'maven:3-alpine'
                    args '-v /root/.m2:/root/.m2'
                }
            }
            options { skipDefaultCheckout(false) }
            steps {
                sh 'mvn -B -DskipTests -f ./backend/pom.xml clean package'
            }
        }
        stage('Docker build') {
            agent any
            steps {
                //sh 'docker build -t backend:latest ./test'
	    	    sh 'docker build -t frontend:latest ./jjal'
            }
        stage('Docker Container rm') {
	    agent any
	    steps {
	        
                sh 'docker ps -f name=base-pjt-back -q | xargs --no-run-if-empty docker container stop'
                sh 'docker container ls -a -fname=base-pjt-back -q | xargs -r docker container rm'
		sh 'docker ps -f name=base-pjt-front -q | xargs --no-run-if-empty docker container stop'
		sh 'docker container ls -a -fname=base-pjt-front -q | xargs -r docker container rm'
                sh 'docker ps -a -f "status=exited" -q | xargs -r docker container rm'
		sh 'docker rmi $(docker images -f "dangling=true" -q)'
	    }
	}
        stage('Docker run') {
            agent any
            steps {
		sh 'docker run -d --name base-pjt-back -v /volumes/data:/volumes/data --network base-pjt-net base-pjt-back:latest'
		sh 'docker run -d --name base-pjt-front -p 80:80 -p 443:443 -v /volumes/nginx/keys:/usr/keys -v /volumes/data:/volumes/data --network base-pjt-net base-pjt-front:latest'
            }
        }
    }
}
