# ascii-image-service
An example service which listens for images in firebase and converts them to ascii

## Requirements
1. Docker / Docker Compose installed and configured. (See documentation [here](https://docs.docker.com/engine/installation/))
2. [Firebase Account](https://firebase.google.com) - To use Storage you need to generate an Admin SDK file, Project Settings -> Service Accounts -> Generate New Private Key
3. ```.env``` file with the following content
```
API_KEY=""
AUTH_DOMAIN=""
DATABASE_URL=""
PROJECT_ID=""
STORAGE_BUCKET=""
MESSAGING_SENDER_ID=""
```

## What it does
This service listens for any files that are added to a Firebase Storage bucket. When a file is added, the service pulls the file down and generates an ASCII representation of that file and uploads it back to the Firebase Storage bucket with the prefix ```ascii-```

Since the Storage resource of Firebase does not have a stream api available, we use a simple polling technique to check for new files.

#### Before
![](https://firebasestorage.googleapis.com/v0/b/cs5450-lab4.appspot.com/o/images%2F17_11_23_23_42_011699?alt=media&token=626c0828-353a-4891-a316-a8e316b28a71)

#### After
![](https://firebasestorage.googleapis.com/v0/b/cs5450-lab4.appspot.com/o/ascii-images%2F17_11_23_23_42_011699?alt=media&token=60256b2f-1be7-4791-bcf6-ec5934b64bcb)

## How to run it
```
$ docker-compose build .
$ docker-compose up
```
Or use the helper script
```
$ ./run.sh
```


## How this can be improved
1. Currently the way we determine whether we have processed a file is by seeing if we have that file in the ```/images/*``` subdirectory. This is not scalable. Think of a better way to keep track of which files have been converted so that we do not have to convert all the files on every update.
2. Converting from image to ascii to image requires a downsample where we lose the aspect ratio. Think of a way to maintain the aspect ratio of the original image. 
3. We are currently polling for new data, this can result in unecessary API calls. Think of a way to make use of the ```streaming``` API as a proxy to notifying of new files. Or think of a different way to be updated that a new file is available
4. Perform a type check to make sure you are actually processing a valid image file
5. Use ```jpg``` to reduce the footprint of the processed image
