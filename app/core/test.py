from langchain_core.messages import AIMessage

response = AIMessage(
    content=[
        {'type': 'thinking', 
         'thinking': 'Machine Learning (ML).\nSmall note (concise, informative, easy to understand).\n\n    *   What is it? (Definition)\n    *   How does it work? (The core concept: data $\\rightarrow$ patterns $\\rightarrow$ predictions)\n    *   Types of ML (Supervised, Unsupervised, Reinforcement).\n    *   Real-world examples (Applications).\n    *   Why is it important? (The "so what").\n\n    *   *Definition:* It\'s a subset of AI. It allows computers to learn without being explicitly programmed.\n    *   *Mechanism:* Instead of rules (if/then), it uses algorithms to find patterns in data.\n    *   *Types:*\n        *   *Supervised:* Labeled data (Teacher). Example: Spam detection.\n        *   *Unsupervised:* Unlabeled data (Finding hidden patterns). Example: Customer segmentation.\n        *   *Reinforcement:* Trial and error (Rewards/Punishments). Example: Game AI (AlphaGo).\n    *   *Examples:* Netflix recommendations, Siri/Alexa, Face ID.\n\n    *   *Heading:* Machine Learning (ML).\n    *   *Introduction:* Start with a clear, one-sentence definition.\n    *   *Core Concept:* Explain the shift from traditional programming to ML.\n    *   *The Three Main Types:* Use a bulleted list for readability.\n    *   *Applications:* Give a few relatable examples.\n    *   *Conclusion:* A brief wrap-up.'
         }, 
         {'type': 'text', 
          'text': 'Here is a concise note on **Machine Learning (ML)**:\n\n### What is Machine Learning?\nMachine Learning is a subset of **Artificial Intelligence (AI)** that focuses on building systems that can learn from data. Instead of being explicitly programmed with a set of rigid rules to perform a task, an ML model uses algorithms to identify patterns in data and make decisions or predictions based on those patterns.\n\n### How It Works\nIn traditional programming, a human provides the **rules** and the **data** to get an **answer**. In Machine Learning, a human provides the **data** and the **answers**, and the machine creates the **rules**.\n\n### Three Main Types of Machine Learning\n1. **Supervised Learning:** The model is trained on "labeled data" (data that already has the correct answer). \n   * *Example:* Teaching a computer to recognize cats by showing it thousands of pictures labeled "cat" and "not cat."\n2. **Unsupervised Learning:** The model looks at "unlabeled data" and tries to find hidden patterns or structures on its own.\n   * *Example:* Grouping customers into different segments based on their shopping habits.\n3. **Reinforcement Learning:** The model learns through trial and error by receiving rewards for correct actions and penalties for wrong ones.\n   * *Example:* An AI learning to play a video game or a robot learning to walk.\n\n### Real-World Applications\n* **Recommendation Systems:** Netflix suggesting movies or Amazon suggesting products.\n* **Healthcare:** Predicting diseases based on patient symptoms and medical imaging.\n* **Virtual Assistants:** Siri, Alexa, and Google Assistant understanding voice commands.\n* **Finance:** Detecting fraudulent credit card transactions in real-time.\n\n### Summary\nAt its core, Machine Learning is about **turning data into intelligence**, allowing computers to improve their performance over time as they are exposed to more information.'}
    ], 
    additional_kwargs={} ,
    response_metadata={
        'finish_reason': 'STOP', 
        'model_name': 'gemma-4-31b-it', 
        'safety_ratings': [], 
        'model_provider': 'google_genai'
        }, 
    id='lc_run--019f26cf-5b9b-7ed2-9137-d2e25a2af01f-0',tool_calls=[], 
    invalid_tool_calls=[], 
    usage_metadata={
        'input_tokens': 9, 
        'output_tokens': 714, 
        'total_tokens': 723, 
        'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 324}
    }
)
print(response.content[1]['text'])