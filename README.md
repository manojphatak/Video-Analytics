# Video-Analytics

  

  

[![Kafka](https://img.shields.io/badge/streaming_platform-kafka-black.svg?style=flat-square)](https://kafka.apache.org)

  

[![Docker Images](https://img.shields.io/badge/docker_images-confluent-orange.svg?style=flat-square)](https://github.com/confluentinc/cp-docker-images)

  

[![Python](https://img.shields.io/badge/python-3.5+-blue.svg?style=flat-square)](https://www.python.org)

  

  

Horizontaly Scalable, Distributed system to churn out video feeds &amp; infer analytics

  

## Goals

Intent of this project is to build a ***Minimalistic***, ***Horizontally Scalable***, ***Distributed*** system to churn out volumes of data & provide meaningful insights into the same.

The current use case we are pursuing is that of churning CCTV footage & provide a Search Interface to query something like:

 - How many Cars and Motor Bikes passed through given area in the given time period?
 - What all the visitors cars entered in the residential complex? How much time they were parked in?
- many more...
Answers to these queries may be useful for Security or finding patterns etc.
  

## Why this project?

One can find numerous solutions for solving problems related to Computer Vision & data analytics in-general. However, most of these solutions are either in the form of "*technology*" (e.g. training a good face recognition model) or ***full blown product***, which could be over-sophisticated.

Our goal is to build something that works, which is easily testable & has minimal number of moving components, which can be used as a base for developing a full-blown product.

We do not want to re-invent the wheel. This project intends to build a minimalistic product that is usable, as well as can act as starting code for building a more complex product.

  ## Non-Goals
  This project doesn't focus on the ***Technology*** aspect. i.e. we are not focusing on, how best we can develop a license-plate recognition system. Instead, we leverage all open-source code & rather focus on orchestrating them in a highly cohesive, loosely coupled way.

## System Requirements
This is currently tested on Ubuntu-Linux.
However, only thing it expects is to have ***docker*** & ***docker-compose*** installed. Since everything runs inside the container, it should work on Windows & Mac as well (barring the helper bash scripts), though I haven't tested it.
  

## How to run
1. Change directory to that of the app
```sh
cd cctv-surveillance
```
2. Spin up Kafka Cluster
```sh
docker-compose -f ../docker-compose-kafka.yml up -d
```
3. Set the environment. e.g. filesystem path where the exported cctv footage movie files can be picked up
This can be done by editing the .env file & running it...

Edit the ".env" file to update the environment variable to work with your machine.
```sh
source .env
```
  4. Run the App, by spinning up all required services
```sh
docker-compose up -d
```
  
  ## Code Organisation
  TODO
  

## Disclaimer

This is not an official HCL ERS product

  
  

## Code Organisation

- Each top-level folder at the root acts as "an app".

- Each app consists of multiple microservices.

- An App is nothing but composition of these microservices.

- A docker-compose file is a place to "compose" the microservices to build the app.

- Individual microservices can talk to each other through Service Discovery or through external message broker "Kafka"

- Kafka acts as common message broker for all the apps.

- The code common to multiple apps, is placed either at root or in a separate folder.

TODO: We still need to come up with an effective way for multiple apps to reuse the code without stepping into each other area / breaking them.

  

## Usage: CCTV-Surveillance App

  




6. Optional: If you are experimenting with the applications & want to clean up everything befor you restart appliction...

```

docker exec kafka bash remove_all_topics.sh # Removes all kafka topics used by the app

bash restart_containers.sh # stops running containers, clear docker logs & restart them

```

  

## How does it work?

The app consists of following microservices communicating to each other through Kafka topics:

```mermaid

graph LR

A[movie-feeder] -- raw-frames --> B[motion-detector]

B[motion-detector] -- enriched frames --> C[face-detector]

C[face-detector] -- frames --> D[face-matcher]

D[face-matcher] -- frames --> E[message-aggregator]

```

>  **movie-feeder**: reads frames from the list of movie files using open-cv

  

>  **motion-detector**: Nothing happens in the scene most of the time, when we are working with cctv. This microservice, detects the frame where something happens. Discards other frames & sends these frames for further processing

  

>  **face-detector**: Checks if the given frame has a human face in it

  

>  **face-matcher**: If there is face, see if it matches with known-faces. Otherwise, update library with new face

  

>  **fileystem-consumer**: Reads recognized / matches faces & create output to file system

  

> **Disclaimer: I have tested this on CCTV feed generated by cameras installed in my housing society.

> While I works in-general, I havn't done any kind of exhaustive testing**

  

## Credits

 - Code for "Object Detection" and "Motion Detection" for CCTV is taken from following excellent tutorials by **Adrian Rosebrock**
	 - [Basic Motion Detection and Tracking using Python and OpenCV](https://www.pyimagesearch.com/2015/05/25/basic-motion-detection-and-tracking-with-python-and-opencv/)
	 - [YOLO Object Detection with OpenCV](https://www.pyimagesearch.com/2018/11/12/yolo-object-detection-with-opencv/)
- References
	- [Building a Streaming Fraud Detection System with Kafka and Python](https://florimond.dev/blog/articles/2018/09/building-a-streaming-fraud-detection-system-with-kafka-and-python/)
	- [How to install and use the python face recognition and detection library in Ubuntu 16.04](https://ourcodeworld.com/articles/read/841/how-to-install-and-use-the-python-face-recognition-and-detection-library-in-ubuntu-16-04)
  

## Run linter & style checker

```

pip install autopep8

autopep8 --in-place --aggressive --aggressive <filename>

```

  

## Feature Backlog

### Refactoring

There are a number of #TODOs annotated in the code. Its a technical debt that was taken to reach a usable system at the earlier. I plan to repay this debt

### Features

#TODO: Create JIRA issues.

### Deployment

- Horizontal Scaling

- Deploy to AWS Cloud

- Profiling
