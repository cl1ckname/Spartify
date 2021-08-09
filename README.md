# Spartify

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/cl1ckname/Spartify.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/cl1ckname/Spartify/context:python)

Spartify is a collaborative queue management service on  [Spotify](https://www.spotify.com/)

## Why?

Usually, in a large group of friends, exactly one person turns on the music. This is logical because there is only one person who is the source of the music. From my own experience I can say that this person is constantly asked to "turn on __this__ track", add an album to the queue, turn it down / up. Or vice versa, the whole company wants to listen to some artist, but the __host__ does not include him in any. These and other problems should be solved by Spartify.

![Doge](https://media.giphy.com/media/jTHtY5651ipk5agEuH/giphy.gif)

## To do

 - [x] Append README.md
 - [x] Add the ability to add tracks to your queue using the site
 - [x] Ability to create a lobby and get a pin code for it
 - [x] Add settings for lobbies
    - [ ] Add more settings to lobbies
       - [ ] Ban list for tracks
       - [ ] Limit on the number of tracks for each user
 - [x] Registration for premium Spotify users and simple users 
 - [ ] Add votes for the next track
 - [ ] Add lobby privileges
 - [ ] Ability add playlists and albums to queue
 - [ ] Creating a beautiful frontend
 - [ ] Upload the application to stable hosting
 - [ ] Play music in big campaigns with ease!
 - [x] Build the application into a Docker container
 - [ ] Realize API
 - [ ] ~~Make a lot of money~~
    - [ ] ~~Make a some money~~
        - [x] ~~Make a little money~~
 - [ ] Write a lot of tests
 - [ ] Add unusual statistic for users on dashboard

## Docker
To build spartify into a docker container, you need to create file:
.env.dev:
  ```
  SOCIAL_AUTH_SPOTIFY_KEY=<your_spotify_app_key>
  SOCIAL_AUTH_SPOTIFY_SECRET=<your_spotify_secret_key>
  SECRET_KEY=<django_secret>
  SQL_ENGINE=django.db.backends.postgresql
  SQL_DATABASE=<datebase>
  SQL_USER=<postgre_user>
  SQL_PASSWORD=<postgre_password>
  SQL_HOST=<postgre_host>
  SQL_PORT=5432
  DATABASE=postgres
  DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
  ``` 
in the root folder of the project.
Build command: `docker-compose up -d --build`

## About other Spartify projects

Recently I stumbled upon several projects of the same name by chance. I haven't heard of any of them, but the name and purpose coincide with some. I hope their developers will not be offended by me. I consider it necessary to leave links to their repositories:
* https://github.com/ysomad/spartify
* https://github.com/blixt/spartify
* https://github.com/rphammy/Spartify
* https://github.com/YuhuaBillChen/Spartify

## Help

If you want to help the project, then I'm looking for:
* designers
* layout designers
* mentors
  * (open to tips and code reviews)
* just not indifferent

### Contacts
[![https://vk.com/clickname](https://img.shields.io/badge/вконтакте-%232E87FB.svg?&style=for-the-badge&logo=vk&logoColor=white)](https://vk.com/clickname)
[![https://twitter.com/Cl1ckName](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/Cl1ckName)
[![20002mc@gmail.com](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:20002mc@gmail.com)