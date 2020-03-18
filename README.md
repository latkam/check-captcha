# check-captcha
Free and open source [CAPTCHA](https://en.wikipedia.org/wiki/CAPTCHA).

## Current state
- basic interface for requesting CAPTCHAs and verifying responses to them
- most of the backend and database infrastructure in place
- partly completed minimal working example with sample data
  - missing server to server authentication
  - missing bigger backend-frontend separation
  - missing automatic frontend generation
  
## Run
#### Windows
```
> set FLASK_APP=checkcaptcha
> set FLASK_ENV=development
> flask init-db
> flask run
```
#### Linux / Mac
```
$ export FLASK_APP=checkcaptcha
$ export FLASK_ENV=development
$ flask init-db
$ flask run
```
  
## Authors
Original prototype made by Matěj Latka, David Mašek, Tomáš Koranda, Kristýna Klesnilová and Karolína Lhotská during [HackFit](https://www.facebook.com/events/fakulta-informa%C4%8Dn%C3%ADch-technologi%C3%AD-%C4%8Dvut/hackfit/182355853127779/) hackaton.

### Made with / Thanks to
- [Flask](https://github.com/pallets/flask)
- Sample image datasets: [1](https://www.kaggle.com/tongpython/cat-and-dog), [2](https://www.kaggle.com/ashishsaxena2209/animal-image-datasetdog-cat-and-panda)
- [Boostrap](https://github.com/twbs/bootstrap)
