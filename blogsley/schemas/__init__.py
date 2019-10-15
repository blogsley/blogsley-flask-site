import graphene
import blogsley.schemas.users
import blogsley.schemas.blog
import blogsley.schemas.images

class MyMutations(users.MyMutations, blog.MyMutations, images.MyMutations):
    pass
class Query(users.Query, blog.Query, images.Query):
    pass

schema = graphene.Schema(query=Query, mutation=MyMutations)
