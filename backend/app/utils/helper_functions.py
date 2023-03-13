from sentence_transformers.util import cos_sim

def dict_to_list(a_dict: dict, key: str) -> list:
        """Converts a dictionary to a list

        Args:
            a_dict (dict): Dictionary to be converted to list
            key (string): Key field of the dictionary

        Returns:
            list : List of values of the key field
        """
        result_list = []

        for dict_value in a_dict:
            result_list.append(dict_value[key])
        
        return result_list


def prepare_response(response: dict, model: classmethod, query_encode: list) -> dict:
        """Prepares the final response for the frontend

        Args:
            response (dict): Response from the database
            model (class): Sentence transformer model
            query_encode (list): Embeddings of entered question

        Returns:
            dict : Final response for the frontend
        """
        encoded_question = model.encode(dict_to_list(response, "question"))

        sim_scores = cos_sim(encoded_question, query_encode).tolist()

        ques_sim_score_list = []

        for res,score in zip(response,sim_scores):
                ques_sim_score_list.append({
                        "id":str(res["id"]),
                        "question":res["question"],
                        "sim_score":round(score[0],2),
                        "subject": res["subject"]
                })
            
        return ques_sim_score_list

def search_query(result: list, collection, output_fields: list):
    ids = result.ids

    res = collection.query(
        expr = f"id in {ids}",
        output_fields=output_fields,
        consistency_level="Strong"
    )

    return res;