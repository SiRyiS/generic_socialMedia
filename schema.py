# The schema interacts with a database and the app.
# Intentional vulnerabilites are included in the resolve_posts and access key validation is bypassed for demonstration.

import graphene
from sqlalchemy import create_engine
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import User as UserModel, Post as PostModel, Comment as CommentModel, Like as LikeModel
from models import Base, User, Post, Comment, Like

def validate_access_key(access_key):
    # comparing the access key with a hardcoded value for DEMONSTRATION ONLY!
    return access_key == "valid_access_key"

# defining the User GraphQL object
class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (graphene.relay.Node, )  # specifying interfaces for user

    # defining fields
    posts = graphene.List(lambda: Post, limit=graphene.Int())
    comments = graphene.List(lambda: Comment, limit=graphene.Int())
    likes = graphene.List(lambda: Like, limit=graphene.Int())

    # fetching likes
    def resolve_likes(self, info, limit=None):
        access_key = info.context.get('access_key')
        if access_key != self.access_key:
            raise Exception("Access denied")
        session = info.context.get('session')
        query = session.query(LikeModel).filter_by(user_id=self.id)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    # fetching posts
    def resolve_posts(self, info, limit=None):
        # intentional vulnerability in place for DEMONSTRATION of bypassing access key validation.
        session = info.context.get('session')
        query = session.query(PostModel).filter_by(user_id=self.id)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

    # fetching comments
    def resolve_comments(self, info, limit=None):
        access_key = info.context.get('access_key')
        if access_key != self.access_key:
            raise Exception("Access denied")
        session = info.context.get('session')
        query = session.query(CommentModel).filter_by(user_id=self.id)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

# post object
class Post(SQLAlchemyObjectType):
    class Meta:
        model = PostModel
        interfaces = (graphene.relay.Node, )

    # defining fields
    comments = graphene.List(lambda: Comment, limit=graphene.Int())
    likes = graphene.List(lambda: Like, limit=graphene.Int())

    # fetching likes associated with posts
    def resolve_likes(self, info, limit=None):
        access_key = info.context.get('access_key')
        if access_key != self.access_key:
            raise Exception("Access denied")
        session = info.context.get('session')
        query = session.query(LikeModel).filter_by(post_id=self.id)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

# comment object
class Comment(SQLAlchemyObjectType):
    class Meta:
        model = CommentModel
        interfaces = (graphene.relay.Node, )

    # defining fields
    likes = graphene.List(lambda: Like, limit=graphene.Int())

    # fetching likes associated with comments
    def resolve_likes(self, info, limit=None):
        access_key = info.context.get('access_key')
        if access_key != self.access_key:
            raise Exception("Access denied")
        session = info.context.get('session')
        query = session.query(LikeModel).filter_by(comment_id=self.id)
        if limit is not None:
            query = query.limit(limit)
        return query.all()

# like object
class Like(SQLAlchemyObjectType):
    class Meta:
        model = LikeModel
        interfaces = (graphene.relay.Node, )  

    user = graphene.Field(User)

    # fetching user associated with likes
    def resolve_user(self, info):
        access_key = info.context.get('access_key')
        if access_key != self.user.access_key:
            raise Exception("Access denied")
        session = info.context.get('session')
        user = session.query(UserModel).filter_by(id=self.user_id).first()
        if not user:
            raise Exception("User not found")
        return user

# post mutation
class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)  
        content = graphene.String(required=True)

    post = graphene.Field(Post)

    # post mutation function 
    def mutate(self, info, title, content):
        access_key = info.context.get('access_key')
        session = info.context.get('session')

        user = session.query(UserModel).filter(UserModel.access_key == access_key).first()  # querying user by access key

        if not user:  
            raise Exception("Access denied: Invalid access key")  

        new_post = PostModel(title=title, content=content, user_id=user.id) 
        session.add(new_post)
        session.commit() 

        return CreatePost(post=new_post)

# comment mutation 
class CreateComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)  
        content = graphene.String(required=True)

    comment = graphene.Field(Comment)

    # comment mutation function 
    def mutate(self, info, post_id, content):
        access_key = info.context.get('access_key') 
        session = info.context.get('session')

        user = session.query(UserModel).filter(UserModel.access_key == access_key).first() 

        if not user:  # checking if user exists
            raise Exception("Access denied: Invalid access key")  

        post = session.query(PostModel).filter_by(id=post_id).first()
        if not post:
            raise Exception("Post not found")

        new_comment = CommentModel(content=content, user_id=user.id, post_id=post_id)
        session.add(new_comment)
        session.commit()

        return CreateComment(comment=new_comment)

# like mutation 
class CreateLike(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int() 
        comment_id = graphene.Int()

    like = graphene.Field(Like)

    # like mutation function
    def mutate(self, info, post_id=None, comment_id=None):
        print("Mutation started") 
        access_key = info.context.get('access_key')
        session = info.context.get('session')
        user = session.query(User).filter_by(access_key=access_key).first()
        if not user: 
            raise Exception("Access denied: Invalid access key")
        if post_id:
            post = session.query(Post).filter_by(id=post_id).first() 
            if not post:
                raise Exception("Post not found")
            new_like = Like(user_id=user.id, post_id=post_id)
        elif comment_id:
            comment = session.query(Comment).filter_by(id=comment_id).first()
            if not comment:  
                raise Exception("Comment not found")  
            new_like = Like(user_id=user.id, comment_id=comment_id)
        else:
            raise Exception("Specify either post_id or comment_id")
        session.add(new_like) 
        session.commit()
        print("Mutation finished")
        return CreateLike(like=new_like)

# deleting post mutation
class DeletePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True) 

    success = graphene.Boolean() 

    # delete post mutation function 
    def mutate(self, info, post_id):
        access_key = info.context.get('access_key')  
        session = info.context.get('session') 

        user = session.query(UserModel).filter(UserModel.access_key == access_key).first()

        if not user:  
            raise Exception("Access denied: Invalid access key")  

        post = session.query(PostModel).filter_by(id=post_id).first()  
        if not post:  
            raise Exception("Post not found")  

        if post.user_id != user.id:  
            raise Exception("Access denied: You are not the owner of this post") 

        session.delete(post)  
        session.commit()

        return DeletePost(success=True)  

# delete a comment
class DeleteComment(graphene.Mutation):
    class Arguments:
        comment_id = graphene.Int(required=True)  

    success = graphene.Boolean()

    # deleting a comment mutation function 
    def mutate(self, info, comment_id):
        access_key = info.context.get('access_key')  
        session = info.context.get('session') 

        user = session.query(UserModel).filter(UserModel.access_key == access_key).first() 

        if not user: 
            raise Exception("Access denied: Invalid access key")  

        comment = session.query(CommentModel).filter_by(id=comment_id).first()  
        if not comment:  
            raise Exception("Comment not found")  

        if comment.user_id != user.id:  
            raise Exception("Access denied: You are not the owner of this comment")  

        session.delete(comment)  
        session.commit()  

        return DeleteComment(success=True)  

# mutation fields
class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()  
    create_comment = CreateComment.Field()  
    create_like = CreateLike.Field()
    delete_post = DeletePost.Field()
    delete_comment = DeleteComment.Field()

# query class for fields
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()  

    user = graphene.Field(User, id=graphene.Int(required=True)) 
    posts = graphene.List(Post, ids=graphene.List(graphene.Int, required=True))

    # query posts by id
    def resolve_posts(self, info, ids):
        access_key = info.context.get('access_key') 
        if not access_key:  
            raise Exception("Access denied: Missing access key")

        session = info.context.get('session') 

        # fetch posts with list of ids
        posts = session.query(PostModel).filter(PostModel.id.in_(ids)).all()

        return posts 

    # query user by id
    def resolve_user(self, info, id):
        access_key = info.context.get('access_key')  
        if not access_key:  
            raise Exception("Access denied: Missing access key") 
        
        session = info.context.get('session')  
        user = session.query(UserModel).filter_by(id=id).first() 
        
        if not user:  
            raise Exception("User not found")  
        
        # uncomment the 2 lines below to enforce access key validation
        #if access_key != user.access_key:
        #    raise Exception("Access denied: Invalid access key")
        
        return user  

    all_users = SQLAlchemyConnectionField(User)  

    # query all users
    def resolve_all_users(self, info):
        access_key = info.context.get('access_key') 
        if not access_key:  
            raise Exception("Access denied: Missing access key")

        # validate key
        valid_access_key = validate_access_key(access_key)

        if not valid_access_key: 
            raise Exception("Access denied: Invalid access key")

        session = info.context.get('session')  
        
        return session.query(UserModel).all() 

schema = graphene.Schema(query=Query, mutation=Mutation)
