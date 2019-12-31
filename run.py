from app.api.app import application
from config import DEBUG

application.run(host='0.0.0.0', port='8000', debug=DEBUG)