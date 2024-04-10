# Flask GraphQL API with SQLAlchemy

This is a simple command line GraphQL API built using Flask and SQLAlchemy for database interaction. It allows users to create, read, update, and delete posts, comments, and likes.

## Usage
1. Populate the database with sample data, run the following command:

    ```bash
    python populate_data.py
    ```
    
2. Run the Flask application:

    ```bash
    python app.py
    ```

3. Access the GraphQL endpoint at `http://localhost:5000/graphql`. Here you can execute queries and mutations.


## Project Structure

- **app.py**: Flask application setup and GraphQL endpoint definition.
- **models.py**: SQLAlchemy model definitions for User, Post, Comment, and Like.
- **schema.py**: GraphQL schema definition using Graphene SQLAlchemy.
- **populate_data.py**: Script to populate the database with sample data.

## Example Queries
- **Schema w/ Metadata**:
```bash
curl -X POST -H "Content-Type: application/json" -H "Access-Key: 50441f01-8b54-4ea1-a0c1-88c02dd97bc0" --data "{\"query\": \"{ __type(name: \\\"Post\\\") { description fields { name description type { name kind ofType { name kind }}}}}\"}" http://localhost:5000/graphql
```
