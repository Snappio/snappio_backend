# Snappio Backend | [DEMO](https://api-snappio.onrender.com/api/v1/users/)
Backend for the Snappio, a _social media / chat application_ built with **flutter** (frontend) and **django rest framework** (backend).

### Features include:
- Realtime chatting with web-sockets _(django channels)_
- JWT Authentication with strict user permissions
- Post images with captions, to be shown on user feeds
- Event-planning and communities __[WIP]__

_While most of the features are already up and running, this project is under development and new features would be added._

## Demo

The api is hosted on [Render](https://render.com/).

To see the api in action, [click here](https://api-snappio.onrender.com/docs/redoc/) to open the hosted instance.

**NOTE**: Since the web service is hosted on _free tier_, it can take upto **a minute** for the first request to be fulfilled.

## API Reference
_For full API documentation, refer to [swagger docs](https://api-snappio.onrender.com/docs/swagger/)._

Few of the available apis are listed below:

#### Get all users

```http
  GET /api/v1/users/
```

#### Get user details

```http
  GET /api/v1/users/profile/
```

| Authorization | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `Bearer Token` | **Required**. Access token for logged in user |

#### Get post details

```http
  GET /api/v1/posts?username=${username}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. Posts of user to fetch |

#### Connect with WebSocket
- User Chat:
```
  WS /ws/user/${username}/
```
- Room Chat:
```
  WS /ws/rooms/${roomid}/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username`      | `string` | **Required**. Valid username of existing user to chat with |
| `roomid`      | `string` | **Required**. ID of room for more than 2 users to join |




## Deployment

This project uses poetry for python package management and docker for abstracting the deployment process.

For docker compose V2:
```bash
  docker compose up -d
```
This will start the container and the server will listen for requests on default http **PORT 80**.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file, also stated in the .env.example file in the repository.

`DJANGO_SECRET` for django's cryptographic signing.

`POSTGRES_URL` url for the connected POSTGRESQL database.

`REDIS_URL` url for the connected REDIS instance used for websocket protocol.
