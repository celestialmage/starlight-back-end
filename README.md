# Starlight Backend API

This is the backend API for **Starlight**, a social media platform where users can post content, reply, like, and follow each other. It is built with **Flask**, **SQLAlchemy**, and **JWT Authentication**, and is designed to be used with the Starlight frontend.

## Tech Stack & Modules

**Core Framework & Server**

* **Flask** — Web framework for handling HTTP requests.
* **Flask Blueprints** — Organizes routes into modular files.

**Database & ORM**

* **Flask SQLAlchemy** — ORM for database interactions.
* **Flask Migrate** — Handles database migrations.
* **PostgreSQL** (or other SQL databases) — Backing database.
* **Declarative Base Models** — Using SQLAlchemy ORM `Mapped` types.

**Authentication & Security**

* **Flask-JWT-Extended** — Handles JWT access and refresh tokens.
* **Google OAuth2** — For login via Google credentials.
* **Werkzeug** — HTTP exception handling.
* **Flask-CORS** — Enables cross-origin requests.

**Utilities**

* **Requests** — Makes HTTP requests to external APIs (Google token verification).
* **SQLAlchemy ORM helpers** — `relationship`, `mapped_column`, etc.

## Project Structure

```
starlight/
├── __init__.py             # App factory and blueprint registration
├── db.py                   # SQLAlchemy and Migrate instances
├── models/
|   ├── base.py                 # Declarative base for SQLAlchemy models
│   ├── user.py             # User model
│   ├── post.py             # Post model
│   ├── reply.py            # Reply model
│   ├── like.py             # Like model
│   ├── follow.py           # Follow model
├── routes/
│   ├── google_routes.py    # Google OAuth login & refresh
│   ├── user_routes.py      # User profile actions
│   ├── post_routes.py      # Post CRUD & timelines
│   ├── reply_routes.py     # Reply CRUD
│   ├── like_routes.py      # Like/unlike posts
│   ├── follow_routes.py    # Follow/unfollow users
│   ├── route_utils.py      # Helper functions for validation
```

## Models

**User**

* Fields: `id`, `username`, `bio`, `display_name`, `email`
* Relationships: `posts`, `likes`, `replies`, `following`, `followers`
* Unique constraint: `id`, `username`, `email`

**Post**

* Fields: `id`, `user_id`, `text`, `image`, `time_posted`
* Relationships: `liked_by` (users), `replies`
* Unique constraint: `id`

**Reply**

* Fields: `id`, `user_id`, `post_id`, `text`, `image`, `time_posted`
* Unique constraint: `id`

**Like**

* Fields: `id`, `post_id`, `user_id`
* Unique constraint: `(user_id, post_id)`

**Follow**

* Fields: `id`, `follower_id`, `followed_id`
* Unique constraint: `(follower_id, followed_id)`

## Authentication

All protected routes require a **Bearer token** in the `Authorization` header:

```
Authorization: Bearer <ACCESS_TOKEN>
```

Tokens are generated using Google OAuth2 login and JWT:

* **Access Token** — Expires in 15 minutes
* **Refresh Token** — Expires in 30 days

## Routes & Endpoints

### Google Authentication (`/api`)

#### `POST /api/login`

*Logs in a user via Google OAuth2.*

**Body:**

```json
{
    "credential": "<GOOGLE_ID_TOKEN>"
}
```

**Response:**

```json
{
    "access_token": "...",
    "refresh_token": "...",
    "user_found": true
}
```

#### `POST /api/refresh`

*Refreshes an access token using a valid refresh token.*

**Response:**

```json
{
    "access_token": "..."
}
```

### Posts (`/posts`)

#### `POST /posts`

*Creates a new post for the authenticated user.*

**Body:**

```json
{
    "text": "Hello world!",
    "image": "optional.jpg"
}
```

**Response:**

```json
{
    "post": {
        "id": 1,
        "user_id": "user123",
        "text": "Hello world!",
        "image": "optional.jpg",
        "time_posted": "2025-08-14T14:00:00Z",
        "reply_count": 0,
        "like_count": 0,
        "user": { ... },
        "user_liked": false
    }
}
```

#### `DELETE /posts/<post_id>`

*Deletes a post owned by the authenticated user.*

**Response:** 204 No Content

#### `GET /posts/user/<user_id>`

*Fetches all posts by a specific user.*

**Response:**

```json
{
    "posts": [ ... ]
}
```

#### `GET /posts/<post_id>`

*Fetches a single post with its replies.*

**Response:**

```json
{
    "post": {
        "id": 1,
        "user_id": "user123",
        "text": "...",
        "replies": [ ... ],
        "user": { ... }
    }
}
```

#### `GET /posts/timeline`

*Fetches the authenticated user’s timeline (their posts and followed users’ posts).*

**Response:**

```json
{
    "posts": [ ... ]
}
```

### Replies (`/replies`)

#### `POST /replies/post/<post_id>`

*Creates a reply on a specific post.*

**Body:**

```json
{
    "text": "Nice post!"
}
```

**Response:**

```json
{
    "reply": {
        "id": 1,
        "user_id": "user123",
        "post_id": 10,
        "text": "Nice post!",
        "time_posted": "2025-08-14T14:05:00Z",
        "user": { ... }
    }
}
```

#### `DELETE /replies/<reply_id>`

*Deletes a reply owned by the authenticated user.*

**Response:** 204 No Content

#### `GET /replies/post/<post_id>`

*Fetches all replies for a specific post.*

**Response:**

```json
{
    "replies": [ ... ]
}
```

### Likes (`/likes`)

#### `GET /likes`

*Fetches all likes of the authenticated user.*

**Response:**

```json
{
    "likes": [ ... ]
}
```

#### `POST /likes/<post_id>`

*Likes a specific post for the authenticated user.*

**Response:**

```json
{
    "like": {
        "id": 1,
        "post_id": 10,
        "user_id": "user123"
    }
}
```

#### `DELETE /likes/<post_id>`

*Removes a like from a specific post for the authenticated user.*

**Response:** 204 No Content

### Follows (`/follows`)

#### `POST /follows/<followed_user_id>`

*Follows a user by ID for the authenticated user.*

**Response:**

```json
{
    "follow": {
        "id": 1,
        "follower_id": "user123",
        "followed_id": "user456"
    }
}
```

#### `DELETE /follows/<followed_user_id>`

*Unfollows a user by ID for the authenticated user.*

**Response:** 204 No Content

## Error Responses

| Status | Meaning                            |
| ------ | ---------------------------------- |
| 400    | Invalid request data               |
| 401    | Unauthorized / Invalid token       |
| 403    | Forbidden (not the resource owner) |
| 404    | Resource not found                 |
| 409    | Conflict (duplicate like/follow)   |

## Running Locally

```bash
pip install -r requirements.txt
export SQLALCHEMY_DATABASE_URI="postgresql://user:pass@localhost/dbname"
export JWT_SECRET_KEY="your_jwt_secret"
flask db upgrade
flask run
```

## Notes

* All datetime fields are returned in ISO 8601 format.
* Relationships are serialized into nested objects when appropriate.
* The API is designed for the Starlight frontend but is reusable by other clients.
