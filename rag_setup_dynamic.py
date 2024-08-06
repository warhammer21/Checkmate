from langchain.vectorstores import Pinecone as Pinecone_vectorstore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI

embed_model = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key="")

pinecone = Pinecone(api_key="")
text_field = 'text'
burger_index = pinecone.Index("burger-menu-index")
pizza_index = pinecone.Index("pizza-menu-index")

vectorstore_burger = Pinecone_vectorstore(
    burger_index,
    embed_model.embed_query,
    text_field
)
vectorstore_pizza = Pinecone_vectorstore(
    pizza_index,
    embed_model.embed_query,
    text_field
)

def augment_prompt(query: str):
    """
    Augments the prompt with data from the vector database.
    """
    if 'burger' in query.lower():
        vectorstore = vectorstore_burger
    elif 'pizza' in query.lower():
        vectorstore = vectorstore_pizza
    else:
        vectorstore = None

    if vectorstore:
        results = vectorstore.similarity_search(query, k=1)
        source_knowledge = "\n".join([x.page_content for x in results])
    else:
        source_knowledge = "No relevant menu items found."

    augmented_prompt = f"""Using the Contexts of menu below, answer the query. 
    you are an ordering assistant and the Contexts are the menu choices based on the query asked  
    you need to go over the Contexts and take the customer's order and if they ask for anything extra like extra cheese or extra ketchup
    you can add that since we have that in inventory and below is the menu price which at the end you will total.
    also iF any type of pizza is requested make sure to confirm size or Inches or since prices differ, customers can also 
    use call inch as " so be mindfull  
    Prices 
    ANY BURGER:$14
    ANY SIDES:$9
    ANY SALAD:$6
    ANY DRINK:$5
    ANY EXTRA:$2 
    12" PIZZA: $16
    14" PIZZA: $23
    18" PIZZA: $28
    STARTERS GARLIC BREAD:$7
    STARTERS ANY SIZE FRIES: $7
    STARTER ANY WINGS: $8

Contexts:
{source_knowledge}

Query: {query}"""
    return augmented_prompt

chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key="")

def chat(messages):
    """
    Function to invoke the ChatOpenAI model and get a response.
    """
    response = chat_model(messages)
    return response.content

# Initialize the conversation
messages = [
    SystemMessage(content="You are an order-taking assistant for a restaurant."),
]

# Start dynamic input loop
while True:
    user_input = input("CX: ")
    if user_input.lower() in ["exit", "quit", "done"]:
        break

    # Augment the prompt with the user's input
    augmented_prompt = augment_prompt(user_input)
    prompt_message = HumanMessage(content=augmented_prompt)
    prompt_human_message = HumanMessage(content=user_input)

    # Invoke a chat with GPT
    response = chat(messages + [prompt_message])
    ai_message = AIMessage(content=response)

    # Append AI message to the conversation
    messages.append(prompt_message)
    messages.append(ai_message)

    # Print the response
    print(f"AI: {ai_message.content}")
