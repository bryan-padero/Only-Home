from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

# SQLAlchemy DB
db = SQLAlchemy(metadata=metadata)

# Flask CKEditor
ckeditor = CKEditor()

# Flask Migrate
migrate = Migrate()

# Flask Login Manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "danger"

# Flask Bootstrap
bootstrap = Bootstrap()
