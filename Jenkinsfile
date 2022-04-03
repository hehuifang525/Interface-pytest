pipeline{
    agent{
        label 'image_build'
    }
    environment{
       IMAGE_NAME   = "registry.otrs365.cn/test/sc-pytest"
    }
    options {
        disableConcurrentBuilds()
    }
    stages{
        stage('Image build'){
            steps{
                sh label: '', script: '''
                cd ${WORKSPACE}

                # get commint id
                commit_id=$(cat .git/HEAD)

                # image name
                image_name=${IMAGE_NAME}

                # image tag name
                image_tag=$(. scripts/image-tag.sh | sed  "s/head/${BRANCH_NAME}/")
                
                # docker build
                docker build --pull . -t "${image_name}:${image_tag}"

                # docker push
                docker push ${image_name}:${image_tag}

                # update latest
                if [[ "${BRANCH_NAME}" == "master" ]]; then
                    docker tag ${image_name}:${image_tag} ${image_name}:latest
                    docker push ${image_name}:latest
                fi
                '''
            }
        }
        
    }
    post{
        cleanup{
            cleanWs cleanWhenAborted: false, cleanWhenFailure: false
        }
    }
}

