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

class ImageInput(graphene.InputObjectType):
    title = graphene.String()
    filename = graphene.String()
    src = graphene.String()

class CreateImage(graphene.Mutation):
    class Arguments:
        data = ImageInput(required=True)

    id = graphene.ID()

    @staticmethod
    def mutate(self, info, data=None):
        user = load_user(info)
        user_id = user.id
        print(user)
        # post = Post.query.get(id)
        image = Image(title=data.title, filename=data.filename, src=data.src, owner_id=user_id)
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
        data = ImageInput(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, id=None, data=None):
        # get the JWT
        token = decode_auth_token(info.context)
        print(token)
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

    @staticmethod
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
