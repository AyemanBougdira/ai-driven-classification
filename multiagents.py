
import os
from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
from trendsdb import subtrends

config_list = [
    {
        "model": "openai/gpt-oss-20b:free",
        "api_key": os.environ["OPENROUTER_API_KEY"],  # use env var
        "base_url": "https://openrouter.ai/api/v1",
    }
]

llm_config = {
    "config_list": config_list
}


def Agents4trends(Company, Scrapped_data):


    message = f"Trends for {Scrapped_data}"
    relevant_memories = subtrends.query(
        query_texts=[message],
        n_results=5
    )

    if relevant_memories["documents"] and len(relevant_memories["documents"][0]) > 0:
        memories_str = "\n".join(
            f"trend{i}: {doc}" for i, doc in enumerate(relevant_memories["documents"][0])
        )
        print(memories_str)


    # The Number Agent always returns the same numbers.
    orchestrator_agent = ConversableAgent(
        name="orchestrator",
        system_message="You are going to orchestrate multi agents to produce Company Classification Trends for {Company}",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # The Adder Agent adds 1 to each number it receives.
    company_analyser = ConversableAgent(
        name="company_analyser",
        system_message=f"""You are a Content Analyzer Agent specializing in understanding French and international 
        companies' business models, products, and services.
                Your Role:
            - Receive and Analyze the scraped company website data provided
            - Extract and structure key business information
            - Identify core activities, technologies, and market focus
                This is the scrapped data: {Scrapped_data}
        """,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )




    # The Multiplier Agent multiplies each number it receives by 2.
    Trend_matcher = ConversableAgent(
        name="Trend_matcher",
        system_message=f"""
        You are a Trend Matcher Agent that specializes in matching companies to this industry trends {memories_str}

            Your Role:
            - Receive company data from the orhestrator Agent
            - Receive the ChromaDB vector database to find relevant trends
            - Perform semantic matching between company characteristics and trend definitions
            - Identify 3 relevant trends 

            
            NOTE: The trends must be from this informations: {memories_str}
    """,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # The Subtracter Agent subtracts 1 from each number it receives.
    validator_agent = ConversableAgent(
        name="validator_Agent",
        system_message=f"""You have to choose a final trend with your final judgement (the trend must be the same as presented on this list: {memories_str})

          
    """,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    # final_trend = ConversableAgent(
    #     name="Final_Agent",
    #     system_message="""You will be given 5 trends: {memories_str}
    #     Based on the informations given form the orchestrator agent choose one trend from only this trends here
    #     Note: I wanna the trend you give to be the same as presented in the 5 trends""",
    #     llm_config=llm_config,
    #     human_input_mode="NEVER",
    # )


    # recall_agent=ConversableAgent(
    #     name="Recall_agent",
    #     system_message="""Recall the final trend (choose frome this list: {memories_str})""",
    #     llm_config=llm_config,
    #     human_input_mode="Never"
    # )

    # Start a sequence of two-agent chats.
    # Each element in the list is a dictionary that specifies the arguments
    # for the initiate_chat method.
    chat_results = orchestrator_agent.initiate_chats(
        [
            {
                "recipient": company_analyser,
                "message": "Analyse this company",
                "max_turns": 1,
                "summary_method": "last_msg",
            },
            {
                "recipient": Trend_matcher,
                "message": "Identify multiple relevant trends",
                "max_turns": 1,
                "summary_method": "last_msg",
            },
            {
                "recipient": validator_agent,
                "message": "Give the final trend ",
                "max_turns": 1,
                "summary_method": "last_msg",
            },
            # {
            #     "recipient": final_trend,
            #     "message": "Choose one trend for the company",
            #     "max_turns": 1,
            #     "summary_method": "last_msg",
            # },

            # {
            #     "recipient": recall_agent,
            #     "message": "give only the final trend given",
            #     "max_turns": 1,
            #     "summary_method": "last_msg",
            # },
        ]
    )

    return (
        chat_results[0].summary,  # Company analysis
        chat_results[1].summary,  # Trends matcher
        chat_results[2].summary,  # Final trend from validator
    )

    # print("Company Analysis: ", chat_results[0].summary)
    # print("Potentail trends: ", chat_results[1].summary)
    # print("Validation report: ", chat_results[2].summary)
    # print("final trend: ", chat_results[3].summary)


# Agents4trends("https://www.zola.fr/", """"Avec un seul et même outil, vous gérez :; Gérez vos entretiens; Pilotez la formation; Gérez les compétences; Exploitez vos people review; Sondez vos équipes; Créez une culture du feedback; Zola s'intègre à votre écosystème; La sécurité de vosdonnées, notre priorité.; Enfin un outil de talent management adapté aux PME et ETI; Ces ressources pourraient vous être utiles :; Questions fréquentes sur les logiciels RH de gestion des talents","Zola est le logiciel RH qui vous permet de gérer les entretiens, la formation et le développement des compétences de vos salariés."

#               """)
