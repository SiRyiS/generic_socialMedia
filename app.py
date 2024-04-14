from flask import Flask, request
from flask_graphql import GraphQLView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from schema import schema as graphql_schema

app = Flask(__name__)
app.debug = True

# database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# engine and database URI
engine = create_engine('sqlite:///mydatabase.db')
Base.metadata.create_all(bind=engine)

# session creation
Session = sessionmaker(bind=engine)

@app.teardown_appcontext
def shutdown_session(exception=None):
    session = Session()
    if session:
        session.close()

class CustomGraphQLView(GraphQLView):
    def dispatch_request(self):
        access_key = request.headers.get('Access-Key')  # extract access key from headers
        with Session() as session:
            request_json = request.get_json(force=True)
            return self.schema.execute(
                request_json['query'],
                context={'session': session, 'access_key': access_key},  # pass key
                variables=request_json.get('variables'),
                operation_name=request_json.get('operationName')
            ).to_dict()

# graphql endpoint
app.add_url_rule('/graphql', view_func=CustomGraphQLView.as_view('graphql', schema=graphql_schema, graphiql=True))

if __name__ == '__main__':
    app.run() # you can specify an IP and port here, example: "app.run(host='0.0.0.0', port=5000)"
