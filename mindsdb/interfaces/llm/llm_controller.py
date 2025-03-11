from mindsdb.interfaces.storage import db
from mindsdb.utilities.config import Config


class LLMDataController:
    '''Handles CRUD operations at the database level for LLM Data'''

    def __init__(self) -> None:
        '''Initializes the LLMDataController with configuration settings.'''
        self.config = Config()

    def add_llm_data(self, input_data: str, output_data: str, model_id: int) -> db.LLMData:
        '''
        Adds LLM input and output data to the database.
        Parameters:
            input_data (str): The input to the LLM.
            output_data (str): The output from the LLM.
            model_id (int): The ID of the model/agent to filter the data.
        Returns:
            LLMData: The created LLMData object.
        '''
        new_llm_data = db.LLMData(
            input=input_data,
            output=output_data,
            model_id=model_id
        )
        db.session.add(new_llm_data)
        db.session.commit()
        return new_llm_data

    def delete_llm_data(self, llm_data_id: int):
        '''
        Deletes LLM an entry of data from the database with a specific id.
        Parameters:
            llm_data_id (int): The ID of the LLM data to delete.
        '''
        llm_data = self.get_llm_data(llm_data_id)
        if (llm_data is None):
            raise ValueError("LLM Data not found")

        db.session.delete(llm_data)
        db.session.commit()

    def list_all_llm_data(self, model_id: int) -> list:
        '''
        Lists all LLM data entries for a specific model.
        Parameters:
            model_id (int): The ID of the model/agent to filter the data.
        Returns:
            List[Dict]: A list of all LLMData objects in the database for the specified model.
        '''
        llm_data_objects = db.session.query(db.LLMData).filter_by(model_id=model_id).all()
        return [{'input': llm_data.input, 'output': llm_data.output} for llm_data in llm_data_objects]

    def get_llm_data(self, llm_data_id: int) -> db.LLMData:
        '''
        Retrieves a specific LLM data entry by ID.
        Parameters:
            llm_data_id (int): The ID of the LLM data to retrieve.
        Returns:
            LLMData: The LLMData object, or None if not found.
        '''
        return db.session.query(db.LLMData).filter_by(model_id=llm_data_id).first()

    def add_notebook_llm_data(self, 
                            input_data: str, 
                            output_data: str, 
                            model_id: int,
                            context_data: dict = None) -> db.LLMData:
        '''
        Adds notebook-specific LLM data with context information.
        Parameters:
            input_data (str): The input query or prompt
            output_data (str): The generated output
            model_id (int): The ID of the model/agent
            context_data (dict): Additional context (files, repo state, etc)
        Returns:
            LLMData: The created LLM data object
        '''
        llm_data = db.LLMData(
            input=input_data,
            output=output_data,
            model_id=model_id,
            metadata={
                "type": "notebook",
                "context": context_data or {}
            }
        )
        db.session.add(llm_data)
        db.session.commit()
        return llm_data

    def get_notebook_context(self, llm_data_id: int) -> dict:
        '''
        Retrieves notebook-specific context for an LLM data entry.
        Parameters:
            llm_data_id (int): The ID of the LLM data
        Returns:
            dict: The context data if available, empty dict otherwise
        '''
        llm_data = self.get_llm_data(llm_data_id)
        if not llm_data:
            return {}
        metadata = getattr(llm_data, 'metadata', {})
        if not isinstance(metadata, dict):
            return {}
        return metadata.get('context', {})
