# Schema: defines what data can be queried
# Graphene schema
import graphene
from graphene_django import DjangoObjectType
from books.models import Book

# Model to tell GraphQL what things can be queried
# Describing how the books will look when they are consulted
class BookType(DjangoObjectType):
    class Meta:
        model = Book
        fields = ("id", "title", "description", "created_at", "updated_at")

# To specify required data an optional data
class CreateBookMutation(graphene.Mutation):
    # Waiting for arguments (what is expected to receive)
    class Arguments:
        title = graphene.String()
        description = graphene.String()

    # Data to be returned (what will be returned)
    book = graphene.Field(BookType)

    # Own method (what will be executed)
    def mutate(self, info, title, description):
        book = Book(title=title, description=description)
        book.save()
        # Returning the instance with the book that I am receiving
        return CreateBookMutation(book=book)
    
class DeleteBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    # book = graphene.Field(BookType) To return the book
    message = graphene.String() # Returning a message instead 

    def mutate(self, info, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return DeleteBookMutation(message="Book deleted")
    
class UpdateBookMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()

    book = graphene.Field(BookType)

    def mutate(self, info, id, title, description):
        book = Book.objects.get(pk=id)
        book.title = title
        book.description = description
        book.save()
        return UpdateBookMutation(book=book)



# It's mandatory to have the next name. In GraphQL, 'Query' indicates the data that can be consulted. It's the equivalent of "get" requests
# To get data for the client from the backend (GET)
class Query(graphene.ObjectType):
    # Creating a query
    hello = graphene.String(default_value="Hi there!") # When this path is queried (it's called "hello"), we'll raturn a string
    books = graphene.List(BookType) # Returning a book list
     # Consulting a single book (field type (to be returned), expected data (along with its type)). ID = Int or String
    book = graphene.Field(BookType, id=graphene.ID())

    def resolve_books(self, info):
        return Book.objects.all()
    
    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)
    
# Mutation: Get data from the client to save it in the backend. Data to save, delete or update (POST, PUT, DELETE)
class Mutation(graphene.ObjectType):
    # create_book = graphene.Field(
    #     BookType, # Data type to be returned
    #     # Waiting for two data to create a book
    #     title=graphene.String(), 
    #     description=graphene.String()
    # ) # When a book is created, that will return the book itself to us
    create_book = CreateBookMutation.Field()
    delete_book = DeleteBookMutation.Field() # When a book is deleted, we can return the book we have deleted or any message
    update_book = UpdateBookMutation.Field()

# To use this query
schema = graphene.Schema(query=Query, mutation=Mutation)
