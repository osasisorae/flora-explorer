import os
from decouple import config
from databank import Databank
from langchain.utilities import ApifyWrapper
from langchain.docstore.document import Document
from langchain.indexes import VectorstoreIndexCreator


# Initialize environment keys
os.environ["OPENAI_API_KEY"] = config('OPENAI_API_KEY')
os.environ["APIFY_API_TOKEN"] = config('APIFY_API_TOKEN')

# Initialize Databank
bank = Databank()


class Educator:
    """This is a chat bot, powered by Apify and langchain. 
    Current set to get information from several websites. 
    Focused on answering questions related to indonesian native floral.
    """
    def __init__(self):
       
        # initilaize apifywrapper
        self.apify = ApifyWrapper()
        
        # Call the Actor to obtain text from the crawled webpages
        self.loader = self.apify.call_actor(
            actor_id="apify/website-content-crawler",
            run_input={"startUrls": bank.links, "maxCrawlPages": 10, "crawlerType": "cheerio"},
            dataset_mapping_function=lambda item: Document(
                page_content=item["text"] or "", metadata={"source": item["url"]}
            ),
        )

        # Create a vector store based on the crawled data
        self.index = VectorstoreIndexCreator().from_loaders([self.loader])

    def query_vector(self, message: str) -> str:
        return self.index.query(message)