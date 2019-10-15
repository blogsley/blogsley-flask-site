import graphene
from graphene import relay
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

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        summary = graphene.String()
        body = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, id, title, summary, body):
        # get the JWT
        token = decode_auth_token(info.context)
        print(token)
        # post = Post.query.get(id)
        post = graphene.Node.get_node_from_global_id(info, id)
        print(post)
        post.title = title
        post.summary = summary
        post.body = body
        db.session.commit()
        ok = True

        return ok

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        summary = graphene.String()
        body = graphene.String()
        owner_id = graphene.ID()

    id = graphene.ID()

    def mutate(self, info, title, summary, body):
        # get the JWT
        user = load_user(info)
        user_id = user.id
        print(user)
        # post = Post.query.get(id)
        post = Post(title=title, summary=summary, body=body, owner_id=user_id)
        db.session.add(post)
        db.session.commit()
        # db.session.flush()
        db.session.refresh(post)
        print(post)
        id = post.id

        return CreatePost(id=id)

class DeletePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

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
