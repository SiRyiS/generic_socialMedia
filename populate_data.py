# Script populates test data (posts, comments, and likes).

import random
import uuid
from app import Session
from models import User, Post, Comment, Like 

def create_users(session):
    users_data = [
        {"name": "John Doe", "email": "john@example.com", "username": "johndoe"},
        {"name": "Jane Smith", "email": "jane@example.com", "username": "janesmith"},
        {"name": "Alice Johnson", "email": "alice@example.com", "username": "alicej"},
        {"name": "Bob Brown", "email": "bob@example.com", "username": "bobb"},
        {"name": "Emma Davis", "email": "emma@example.com", "username": "emmad"},
        {"name": "Michael Wilson", "email": "michael@example.com", "username": "michaelw"},
        {"name": "Olivia Taylor", "email": "olivia@example.com", "username": "oliviat"},
        {"name": "James Martinez", "email": "james@example.com", "username": "jamesm"},
        {"name": "Sophia Anderson", "email": "sophia@example.com", "username": "sophiaa"},
        {"name": "William Garcia", "email": "william@example.com", "username": "williamg"}
    ]
    for user_data in users_data:
        user_data['access_key'] = str(uuid.uuid4())
        user = User(**user_data)
        session.add(user)
    session.commit()

def create_posts_comments_likes(session):
    users = session.query(User).all()

    for user in users:
        for _ in range(5):
            post = Post(title=f"Post by {user.name}", content=f"This is a post by {user.name}", user_id=user.id)
            session.add(post)
            session.commit()

            for _ in range(2):
                comment = Comment(content=f"Comment on post by {user.name}", user_id=random.choice(users).id, post_id=post.id)
                session.add(comment)
                session.commit()

                like_post = Like(user_id=random.choice(users).id, post_id=post.id)
                session.add(like_post)
                session.commit()

            post_comments = session.query(Comment).filter_by(post_id=post.id).all()
            for comment in post_comments:
                like_comment = Like(user_id=random.choice(users).id, post_id=post.id)
                session.add(like_comment)
                session.commit()

if __name__ == '__main__':
    session = Session()
    create_users(session)
    create_posts_comments_likes(session)
    session.close()
