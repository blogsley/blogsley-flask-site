import json
import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from blogsley import db
from blogsley.models.users import User
from blogsley.models.blog import Post

from blogsley.jwt import encode_auth_token, decode_auth_token

class UserNode(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node, )


class UserConnection(relay.Connection):
    class Meta:
        node = UserNode

class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    token = graphene.String()

    def mutate(self, info, username, password):
        print('Login')
        if not username:
            raise Exception('Username missing!')
        if not password:
            raise Exception('Password missing!')

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            raise Exception('No such user or invalid password!')

        # Identity can be any data that is json serializable
        access_token = encode_auth_token(sub=username, id=user.id)
        print(access_token)
        # token = json.dumps({"token": access_token.decode('utf-8')})
        token = access_token.decode('utf-8')
        print(token)
        return Login(token=token)

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        email = graphene.String()

    id = graphene.ID()

    def mutate(self, info, username, email):
        print('CreateUser')
        user = User(
            username='joe',
            first_name='Joe',
            last_name='Jackson',
            email='joe@example.com',
            role='Reader',
            about_me='I am a Reader'
        )
        user.set_password(password)
        db.session.add(u)
        db.session.commit()

        return user.id

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        username = graphene.String()
        email = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, id, username, email):
        print('UpdateUser')
        print(id)
        user = graphene.Node.get_node_from_global_id(info, id)
        print(user)
        user.username = username
        user.email = email
        user.save()
        ok = True

        return ok

class MyMutations(graphene.ObjectType):
    log_in = Login.Field()
    update_user = UpdateUser.Field()

class Query(graphene.ObjectType):
    # node = relay.Node.Field()
    user = relay.Node.Field(UserNode)
    all_users = SQLAlchemyConnectionField(UserConnection)
