# Order-Taking Assistant Module

## Summary

The Order-Taking Assistant Module is designed to handle customer interactions for a restaurant, dynamically processing orders and providing responses based on menu data.

## How It Works

### Integration with Pinecone and OpenAI

- **Pinecone**: Used for vector storage and retrieval, storing menu data for burgers and pizzas.
- **OpenAI Embeddings**: Employed to convert text into vectors for similarity search.

### Dynamic Prompt Augmentation

- **Prompt Enhancement**: Based on the customer's query, the module retrieves relevant menu data from Pinecone. This data is used to generate an enhanced prompt for the AI model, ensuring it has the context necessary to provide accurate responses.
- **Contextual Information**: The system handles various menu items and their prices, including burgers, pizzas, drinks, and sides, adjusting responses according to the customer's requests.

### Chat Model Interaction

- **ChatOpenAI**: Utilizes the GPT-3.5-turbo model to process the augmented prompts and generate responses.
- **Dynamic Conversation**: The module supports continuous interaction, taking user input dynamically and updating the conversation context based on each new input.

### Order Processing

- **Menu Handling**: The module is designed to handle specific queries about menu items, confirm sizes, and address extra requests (e.g., additional toppings).
- **Confirmation and Summary**: At the end of the conversation, the system summarizes the order and provides a final confirmation, including the total cost and preparation time.

## Logical Steps

1. **Initialization**: Sets up the Pinecone index and OpenAI embeddings.
2. **Dynamic Prompting**: Adjusts prompts based on user input to include relevant context from the menu.
3. **AI Response Generation**: Uses ChatOpenAI to generate responses based on the augmented prompt and ongoing conversation.
4. **Interactive Session**: Continuously processes user input, providing real-time responses and handling the ordering process until the session is completed.

This approach ensures that the assistant can handle complex ordering scenarios with dynamic user input, providing accurate and contextually relevant responses throughout the interaction.

## Running the Script

To run the `rag_setup_dynamic.py` script, make sure you have the required Pinecone and OpenAI API keys configured. You can execute the script from your terminal using the following command:

```bash
python rag_setup_dynamic.py
