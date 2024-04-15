# Generic GraphQL Social Media App

This is a simple command line graphQL API built using Flask and SQLAlchemy. You can use it to create, read, update, and delete posts, comments, and likes.

## Intended Vulnerabilties for testing and demonstration purposes:
- Vulnerabilities lie in the `resolve_posts` and `resolve_user` method of the `User` class. The `access_key` is not implemented before querying the `PostModel` and the check is turned off for the `UserModel`.
```python
[TRUNCATED]
def resolve_posts(self, info, limit=None):
    # intentional vulnerability in place for DEMONSTRATION of bypassing access key validation.
    session = info.context.get('session')
    query = session.query(PostModel).filter_by(user_id=self.id)
    if limit is not None:
        query = query.limit(limit)
    return query.all()
[TRUNCATED]
def resolve_user(self, info, id): access_key = info.context.get('access_key')
[TRUNCATED]
    # uncomment the 2 lines below to enforce access key validation
    #if access_key != user.access_key:
     #raise Exception("Access denied: Invalid access key")
[TRUNCATED]
```

## Set up
1. You can populate the database with sample data by running the populate_data.py script:

    ```bash
    python populate_data.py
    ```
    
2. Then run the Flask app, with the otger files in tbe same directory:

    ```bash
    python app.py
    ```

3. By default you should be able to access the graphQL endpoint at `http://localhost:5000/graphql`. Using the command line you can use a tool like `cURL` or whatever to execute queries and mutations.

## Project structure should look similar to this:

- **app.py**: Flask application setup and endpoint definition.
- **models.py**: SQLAlchemy model definitions.
- **schema.py**: graphQL schema definition.
- **populate_data.py**: script to populate the database with sample data.

## A few example queries to get started, you play around and figure out more or messsage me.
- **Schema w/ Metadata**:
```bash
curl -X POST -H "Content-Type: application/json" -H "Access-Key: 50441f01-8b54-4ea1-a0c1-88c02dd97bc0" --data "{\"query\": \"{ __type(name: \\\"Post\\\") { description fields { name description type { name kind ofType { name kind }}}}}\"}" http://localhost:5000/graphql
```
- **Schema**:
```bash
curl -X POST -H "Content-Type: application/json" -H "Access-Key: 50441f01-8b54-4ea1-a0c1-88c02dd97bc0" --data "{\"query\": \"{ __schema { queryType { fields { name args { name type { name kind ofType { name } } } } } } }\"}" http://localhost:5000/graphql
```
- **User, Post, Comment, Like**:
```bash
curl -X POST -H "Content-Type: application/json" -H "Access-Key: 50441f01-8b54-4ea1-a0c1-88c02dd97bc0" --data "{\"query\": \"{ user(id: 8) { id name email posts { id title content } comments { id content } likes { id userId } } }\"}" http://localhost:5000/graphql
```
- **Add a Post**:
```bash
curl -X POST -H "Content-Type: application/json" -H "Access-Key: 50441f01-8b54-4ea1-a0c1-88c02dd97bc0" --data "{\"query\": \"mutation { createComment(postId: 1, content: \\\"This is a new comment11\\\") { comment { id content } } }\"}" http://localhost:5000/graphql
```

**DON'T** contact me about building scraping scripts or bots. I may upload generic versions used to go after this set up for demonstration only eventually.