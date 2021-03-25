pipeline {
    agent none
    options { skipDefaultCheckout(false) }
    stages {
        stage('Docker build') {
            agent any
            steps {
                sh 'docker build -t base-pjt-back:latest ./back'
	    	    sh 'docker build -t base-pjt-front:latest ./front/jjal'
            }
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
		        sh 'docker run -it -d -p 8000:8000 -v /content:/content --name base-pjt-back base-pjt-back:latest'
		        sh 'docker run -it -d -p 80:80 -p 443:443 --name base-pjt-front base-pjt-front:latest'
            }
        }
    }
}
