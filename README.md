# GeekSocks
Hi! My name is Oleg. I work as DevOps teamlead in fintech.
This is my playground repo.

## What's inside
Project is based on static webpage with a gallery of funny socks 🤪
It run's on my custom k8s cluster hosted on Yandex cloud.
Here is a list of services and features:

 - geeksocks. Image with static content (html+js).
 - geeksocks-mail-producer. Microservice (Flask based) that receives user messages from website and put them in rabbitmq (mtls enabled). Service has defense (pretty dumb, actually) from frod, based on flask_limiter. 
 - geeksocks-mail. This microservice receives messages from rabbitmq and send them via mailgun. It is based on https://github.com/ractf/mail-usv but slightly changed. 
 - cert-manager used to create certs and keys for mtls connection between services and rabbitmq. Also it communicates with letsencrypt to obtain certificates for website.
 - s3 bucket used as pv for storing images.
 - Also there is a CI pipeline on Gitlab but I plan to completely rewrite it

Future plans

 - [ ] Production ready config for rmq, flask app and so on
 - [ ] Redis for flask_limiter
 - [ ] Make docker images smaller (a lot of extra files there now)
 - [ ] Rewrite site - create admin zone and get store items from DB
 - [ ] Monitoring
 - [ ] Tekton for ci/cd
 - [ ] Clean repo from trash and make in ~~great again~~ pretty
 - [ ] Connect IoT device to rabbit

### PS
Don't take this  seriously, this is just a sandbox for my experiments
