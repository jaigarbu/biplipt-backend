import graphene


class FeaturingInput(graphene.InputObjectType):
   name = graphene.String(required=True)
   nativeName = graphene.String()
   dns = graphene.String()