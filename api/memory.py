# gpt-for-whatsapp
# Copyright (c) 2023 Jasiel Macedo
# 
# This file includes code from Auto-GPT, which is licensed
# under the MIT license. The original code can be found at https://github.com/Significant-Gravitas/Auto-GPT.

import pinecone

from api.abc import MemoryProviderSingleton
from api.utils import get_ada_embedding

from api.constants import PINECONE_API_KEY, PINECONE_API_ENVIRONMENT, PINECONE_TABLE_NAME, PINECONE_POD_TYPE, EMBED_DIM
from loguru import logger

from uuid import uuid4

class PineconeMemory(MemoryProviderSingleton):
    def __init__(self):
        pinecone_api_key = PINECONE_API_KEY
        pinecone_region = PINECONE_API_ENVIRONMENT
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_region)
        dimension = EMBED_DIM
        metric = "cosine"
        pod_type = PINECONE_POD_TYPE
        table_name = PINECONE_TABLE_NAME

        try:
            pinecone.whoami()
        except Exception as e:
            logger.error("FAILED TO CONNECT TO PINECONE")
            exit(1)

        indexes = pinecone.list_indexes()
        logger.info(f"existing indexes {indexes}")
        try :
            if table_name not in indexes:
                pinecone.create_index(table_name, dimension=dimension, metric=metric, pod_type=pod_type)
        except Exception as e:
            logger.error("FAILED TO CREATE PINECONE INDEX", e)
        self.index = pinecone.Index(table_name)

    def add(self, data, user):
        vector = get_ada_embedding(data)
        id = uuid4()
        self.index.upsert([(str(id), vector, {"raw_text": data, "user": user})], namespace=None)
        _text = f"Inserting data into memory at index: {id}:\n data: {data}"
        return _text

    def get(self, data):
        return self.get_relevant(data, 1)

    def clear(self):
        self.index.delete(deleteAll=True)
        return "Obliviated"

    def get_relevant(self, data, user, num_relevant=5):
        """
        Returns all the data in the memory that is relevant to the given data.
        :param data: The data to compare to.
        :param num_relevant: The number of relevant data to return. Defaults to 5
        """
        query_embedding = get_ada_embedding(data)
        results = self.index.query(query_embedding, top_k=num_relevant, include_metadata=True, filter={"user":user})
        sorted_results = sorted(results.matches, key=lambda x: x.score)
        return [str(item['metadata']["raw_text"]) for item in sorted_results]

    def get_stats(self):
        return self.index.describe_index_stats()

memory = PineconeMemory()