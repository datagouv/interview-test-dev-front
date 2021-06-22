# Interview Exercise

## Introduction

The purpose of this interview exercise is to assess your ability to code a simple [vue.js][] interface.

Your goal is to to build a simple [vue.js][] Single Page Application that queries an existing python [flask][] API. This SPA can live independantly from the API, (ie run on a different server/port).

Upon completion, please upload your code on your github/gitlab/... You might need to upload a repo for the backend (cf 5. below) and the frontend. Please do not fork the backend repository on github since it would point other candidates directly to your solution.

After the exercise is completed, we will take the time to discuss what has been done. There's not a single way to do things right, and we're aware of that. Please code what you feel would be naturally elegant and simple for you, not what you think we might expect.

If you're stuck on something related to the backend, please reach out to us.

## Exercise

The exercise is divided between the following steps:
1. First, create a single page app that displays a random hash returned by the `/dummy-hash` API route.
2. Add a page to connect to the `/hash` route. The user will need to submit a string and pick a hash algorithm between `md5`, `sha1` and `sha256`.
3. Add an option to the previous page to show hashes from all three hashes algorithms at a time.
4. Add a registration and login system (using `register/`, `login/` and `logout/` routes).
5. Finally, modify the existing API to add a `me/` route that returns the current user (based on token header) and create a corresponding profile page on the vue app.

## Constraints

Please, use the [French Government Design System][] for styling (also see [dev doc](https://gouvfr.atlassian.net/wiki/spaces/DB/pages/223019574/D+veloppeurs)).

## Usage

In order to launch the [flask][] API, you can run the following:

``` python
python3 -m venv pyenv
source pyenv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask run
```

You can curl `localhost:5000/api/dummy-hash` to make sure everything works properly.

[vue.js]: https://vuejs.org/
[flask]: https://flask.palletsprojects.com/en/2.0.x/
[French Government Design System]: https://www.systeme-de-design.gouv.fr/
