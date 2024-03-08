from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_swagger_ui import get_swaggerui_blueprint
from database import ConnectPostgresQL, OrdersClass, OrdersTable


# Create a Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456789@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Conexão com o banco de dados
host_postgres = 'postgresql://postgres:123456789@localhost:5432/postgres'
sql = ConnectPostgresQL(host_postgres)

# Configurações do Swagger
api = Api(app)

# Definição do parser para os argumentos da consulta
parser = reqparse.RequestParser()
parser.add_argument('client_name', type=str, help='Nome do cliente')


# Definição do modelo de dados para a resposta da API
order_fields = {
    'id': fields.Integer,
    'nome_do_cliente': fields.String,
    'produto': fields.String,
    # Adicione outros campos conforme necessário
}

  

class UserData(Resource):
    @marshal_with(order_fields)
    def get(self, client_name):
        args = parser.parse_args()
        client_name = args['client_name']
        orders = OrdersTable.query.filter_by(nome_do_cliente=client_name).all()
        
        return orders
        

# Adicionando a rota da API
api.add_resource(UserData, '/orders')


# Configurando a documentação do Swagger
SWAGGER_URL = '/api/docs'
API_URL = '/swagger.json'

@app.route(API_URL)
def swagger_json():
    return jsonify(app.config['SWAGGER'])

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'User Data API'
    }
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    # Configuração da documentação Swagger
    app.config['SWAGGER'] = {
        "swagger": "2.0",
        "info": {
            "title": "User Data API",
            "description": "API para obter informações de faturamento",
            "version": "1.0"
        },
        "basePath": "/",
        "schemes": [
            "http",
            "https"
        ],
        "paths": {
            "/user/{user_id}": {
                "get": {
                    "summary": "Obter dados de um usuário pelo ID",
                    "description": "Retorna os dados de um projeto com base no ID fornecido.",
                    "produces": [
                        "application/json"
                    ],
                    "parameters": [
                        {
                            "in": "path",
                            "name": "user_id",
                            "description": "ID do usuário a ser obtido",
                            "required": True,
                            "type": "string",
                            "example": "1"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Operação bem-sucedida",
                            "schema": {
                                "type": "object",
                                "properties": {
                                                                    
                                    "nome_cliente": {
                                        "type": "string"
                                    },
                                    
                                     "projeto": {
                                        "type": "integer"
                                    },
                                }
                            }
                        },
                        "404": {
                            "description": "Usuário não encontrado"
                        }
                    }
                }
            }
        }
    }

    app.run(debug=True)
