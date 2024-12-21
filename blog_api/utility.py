import random
from faker import Faker
from django.contrib.auth.models import User
from .models import Post, Comment

faker = Faker()

def generate_fake_data(users=5, posts=10, comments=20):
    """
    Populate the database with fake data.
    - `users`: Number of users to create.
    - `posts`: Number of posts to create.
    - `comments`: Number of comments to create.

    Returns:
        Summary of generated data.
    """
    created_users = []
    created_posts = []
    created_comments = []

    # Create Users
    for _ in range(users):
        username = faker.unique.user_name()
        email = faker.unique.email()
        first_name = faker.first_name()
        last_name = faker.last_name()
        user = User.objects.create_user(
            username=username,
            email=email,
            password='password123',
            first_name=first_name,
            last_name=last_name
        )
        created_users.append(user)

    # Create Posts
    for _ in range(posts):
        title = faker.sentence(nb_words=6)
        content = faker.paragraph(nb_sentences=10)
        author = random.choice(created_users)
        post = Post.objects.create(
            title=title,
            content=content,
            author=author
        )
        created_posts.append(post)

    # Create Comments
    for _ in range(comments):
        content = faker.sentence(nb_words=12)
        author = random.choice(created_users)
        post = random.choice(created_posts)
        parent = None

        # Add a 30% chance of creating a nested reply
        if random.random() < 0.3:
            parent_candidates = Comment.objects.filter(post=post, parent=None)
            if parent_candidates.exists():
                parent = random.choice(parent_candidates)

        comment = Comment.objects.create(
            post=post,
            author=author,
            content=content,
            parent=parent
        )
        created_comments.append(comment)

    return {
        "users": len(created_users),
        "posts": len(created_posts),
        "comments": len(created_comments),
    }
