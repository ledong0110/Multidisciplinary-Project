from flask_restx import Api
from .homeControllers import api as homeManagement



api = Api(
    title='Register Server',
    version='1.0',
    description='A description',
    # All API metadatas
)



api.add_namespace(homeManagement, path='/api')