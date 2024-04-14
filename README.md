# Flask GraphQL API with SQLAlchemy

This is a simple command line GraphQL API built using Flask and SQLAlchemy for database interaction. It allows users to create, read, update, and delete posts, comments, and likes.

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

## Usage
1. Populate the database with sample data by running the populate_data.py script:

    ```bash
    python populate_data.py
    ```
    
2. Run the Flask application:

    ```bash
    python app.py
    ```

3. By default you should be able to access the GraphQL endpoint at `http://localhost:5000/graphql`. Using the command line you can use a tool like `cURL` to execute queries and mutations.

## Structure

- **app.py**: Flask application setup and endpoint definition.
- **models.py**: SQLAlchemy model definitions.
- **schema.py**: GraphQL schema definition.
- **populate_data.py**: Script to populate the database with sample data.

## Example Queries
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
curl -X POST -H "Content-Type: application/json" -H "Access-Key: 50441f01-8b54-4ea1-a0c1-88c02dd97bc0" --data "{\"query\": \"mutation { createComment(postId: 1, content: \\\"This is a new comment11\\\") { comment { id content } } }\"}" http://localhost:5000/graphql```
