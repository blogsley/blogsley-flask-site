import graphene
from graphene import relay
from graphql_relay import to_global_id
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from blogsley import db
from blogsley.models.users import User
from blogsley.models.blog import Post
from blogsley.jwt import decode_auth_token, load_user

class PostNode(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (relay.Node, )

class PostConnection(relay.Connection):
    class Meta:
        node = PostNode

class PostInput(graphene.InputObjectType):
    title = graphene.String()
    model = graphene.String()
    body = graphene.String()

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        data = PostInput(required=True)
        
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, id, data):
        # get the JWT
        token = decode_auth_token(info.context)
        print(token)
        # post = Post.query.get(id)
        post = graphene.Node.get_node_from_global_id(info, id)
        print(post)
        post.title = data.title
        post.model = data.model
        post.body = data.body
        db.session.commit()
        ok = True

        return ok

class CreatePost(graphene.Mutation):
    class Arguments:
        data = PostInput(required=True)

    id = graphene.ID()

    @staticmethod
    def mutate(self, info, data=None):
        user = load_user(info)
        user_id = user.id
        print(user)
        post = Post(title=data.title, model=data.model, body=data.body, owner_id=user_id)
        db.session.add(post)
        db.session.commit()
        # db.session.flush()
        db.session.refresh(post)
        print(post)
        #id = post.id
        id = to_global_id(PostNode._meta.name, post.id)

        return CreatePost(id=id)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, id):
        # get the JWT
        token = decode_auth_token(info.context)
        print(token)
        post = graphene.Node.get_node_from_global_id(info, id)
        print(post)
        db.session.delete(post)
        db.session.commit()
        ok = True

        return ok

class MyMutations(graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()

class Query(graphene.ObjectType):
    # node = relay.Node.Field()
    post = relay.Node.Field(PostNode)
    all_posts = SQLAlchemyConnectionField(PostConnection)
