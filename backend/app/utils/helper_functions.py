from sentence_transformers.util import cos_sim


a_dict = {
        "question":"some question"
}


def dict_to_list(a_dict,key):
        result_list = []

        for dict_value in a_dict:
            result_list.append(dict_value[key])
        
        return result_list


def similarity_score_calculator(response, model,query_encode):
        
        encoded_question = model.encode(dict_to_list(response,"question"))

        sim_scores = cos_sim(encoded_question,query_encode).tolist()

        ques_sim_score_list = []

        for res,score in zip(response,sim_scores):
                ques_sim_score_list.append({
                        "id":str(res["id"]),
                        "question":res["question"],
                        "sim_score":round(score[0],2),
                        "subject": res["subject"]
                })
            
        return ques_sim_score_list