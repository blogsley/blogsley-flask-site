import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from blogsley import db
from blogsley.models.users import User
from blogsley.models.images import Image
from blogsley.jwt import decode_auth_token, load_user

class ImageNode(SQLAlchemyObjectType):
    class Meta:
        model = Image
        interfaces = (relay.Node, )


class ImageConnection(relay.Connection):
    class Meta:
        node = ImageNode

class CreateImage(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        path = graphene.String()
        owner_id = graphene.ID()

    id = graphene.ID()

    def mutate(self, info, title, summary, body):
        # get the JWT
        user = load_user(info)
        user_id = user.id
        print(user)
        # post = Post.query.get(id)
        image = Image(title=title, path=path, owner_id=user_id)
        db.session.add(image)
        db.session.commit()
        # db.session.flush()
        db.session.refresh(image)
        print(image)
        id = image.id

        return CreateImage(id=id)

class UpdateImage(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, id, title):
        # get the JWT
        token = decode_auth_token(info.context)
        print(token)
        # post = Post.query.get(id)
        image = graphene.Node.get_node_from_global_id(info, id)
        print(image)
        image.title = title
        db.session.commit()
        ok = True

        return ok

class DeleteImage(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        # get the JWT
        token = decode_auth_token(info.context)
        print(token)
        image = graphene.Node.get_node_from_global_id(info, id)
        print(image)
        db.session.delete(image)
        db.session.commit()
        ok = True

        return ok

class MyMutations(graphene.ObjectType):
    create_image = CreateImage.Field()
    update_image = UpdateImage.Field()
    delete_image = DeleteImage.Field()

class Query(graphene.ObjectType):
    # node = relay.Node.Field()
    image = relay.Node.Field(ImageNode)
    all_images = SQLAlchemyConnectionField(ImageConnection)
