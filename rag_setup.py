from langchain.vectorstores import Pinecone as Pinecone_vectorstore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI

embed_model = OpenAIEmbeddings(model="text-embedding-ada-002",openai_api_key="")

# From the langchain_pinecone package, import PineconeVectorStore

pinecone = Pinecone(api_key="")
text_field = 'text'
burger_index = pinecone.Index("burger-menu-index")
pizza_index = pinecone.Index("pizza-menu-index")

# Create a PineconeVectorStore from the index, the embedding model, and the text field.
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
    # Choose the appropriate vectorstore based on the query
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
    you can add that since we have that in inventory and below is the menu price which at the end you will total 
    ANY BURGER:$14
    ANY SIDES:$9
    ANY SALAD:$6
    ANY DRINK:$5
    ANY EXTRA:$2 

Contexts:
{source_knowledge}

Query: {query}"""
    return augmented_prompt

# Initialize ChatOpenAI object with the gpt-3.5-turbo model
chat_model = ChatOpenAI(model_name="gpt-3.5-turbo",openai_api_key="")

def chat(messages):
    """
    Function to invoke the ChatOpenAI model and get a response.
    """
    # Get response from the ChatOpenAI model
    response = chat_model(messages)

    # Return the AI message
    return response.content

# Initialize the conversation
messages = [
    SystemMessage(content="You are an order-taking assistant for a restaurant."),
]

# Define the conversation turns
conversation_turns = [
    "Hi AI, how are you today?",
    "I would like a Classic Chicken Burger.",
    "Yes, add extra cheese and extra ketchup.",
    "Yes, let me have a medium Coke.",
    "Actually, I changed my mind. I don't want to eat beef. Can I have a Spicy Chicken instead, go light on the onions, and add pickles?",
    "That's it, thank you."
]

# Process each turn of the conversation
for turn in conversation_turns:
    # Augment the prompt
    augmented_prompt = augment_prompt(turn)

    # Create a new HumanMessage with the augmented prompt
    prompt_message = HumanMessage(content=augmented_prompt)
    prompt_human_message = HumanMessage(content=turn)

    # Invoke a chat with GPT sending the messages plus the prompt to GPT
    response = chat(messages + [prompt_message])

    # Create a new AIMessage with the response
    ai_message = AIMessage(content=response)

    # Append AI message to the conversation
    messages.append(prompt_message)
    messages.append(ai_message)

    # Print the response
    print(f"AI: {ai_message.content}")
