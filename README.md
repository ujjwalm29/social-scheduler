# Social Scheduler :rocket: :rocket:

Presenting, social scheduler, a platform for content creators to schedule content, collaborate with their teams and make their content searchable. :sunglasses:

## Features

There are 3 main features :

- **Collaborate with teams** : Afraid of giving direct access of your social media account to various people? Fret not! With social scheduler, you will be able to collaborate with your team without giving direct access to your social media account. Suggest changes, post comments, watch previews, approve requests and a lot more from anywhere in the world :world_map:!

- **Schedule content** : Want to schedule all your content from a single platform? Social scheduler helps you schedule all your content in advance so you can make money :money_mouth_face: while you sleep :sleeping:

- **Make your content searchable** : You put out this banger tweet. But who the hell remembers it? And we know that X(twitter), LinkedIn and Instagram search SUCKS! Social scheduler guarantees to make your content super searchable with accurate precision :dart:

## Development

I am embracing the build in public culture for this project.

## Tech Stack

Although my primary backend tech stack is Java, Spring Boot and Postgresql, I wanted to try out new languages. I recently heard about massive performance improvements undertaken in the python programming language. I started reading more about it and stumbled upon FastAPI, which claims to be almost as performant as Golang. I decided to try out FastAPI and the python ecosystem and hence the tech stack for this project is python, FastAPI, SQLAlechmy(python ORM) and Postgresql.

## Features implemented

### Backend

- Database and FastAPI setup
- Signup and Login(Authentication) using JWT tokens
- Creation of projects by content creators
- Send email invite to other users to join their project(social media managers, editors, analysts etc.)
- Project members can create "content" pieces inside the app.
- All photos and videos in the content entities get uploaded to AWS S3 using time bounded presigned URLs.

## License

Don't steal my shit.
