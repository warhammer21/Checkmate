from pinecone import Pinecone, ServerlessSpec
pinecone = Pinecone(api_key="")
# Create Pinecone indices for burgers and pizzas
burger_index_name = "burger-menu-index"
pizza_index_name = "pizza-menu-index"

if burger_index_name not in pinecone.list_indexes():
    pinecone.create_index(burger_index_name, dimension=1536, metric='cosine',
                          spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
        )
if pizza_index_name not in pinecone.list_indexes():
    pinecone.create_index(pizza_index_name, dimension=1536, metric='cosine',
                          spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
                          )

# t = pinecone.list_indexes()
# burger_index = pinecone.Index(burger_index_name)
# pizza_index = pinecone.Index(pizza_index_name)
# print(pinecone.list_indexes())

# pinecone.delete_index('llama-2-rag')
# pinecone.delete_index(pizza_index_name)

t = pinecone.list_indexes()
print(t)
