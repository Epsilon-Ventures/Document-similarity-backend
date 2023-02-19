from sentence_transformers.util import cos_sim


a_dict = {
        "question":"some question"
}


def dict_to_list(a_dict,key):
        result_list = []

        for dict_value in a_dict:
            result_list.append(dict_value[key])
        
        return result_list


def similarity_score_calculator(questions, model,query_encode):
        
        encoded_question = model.encode(dict_to_list(questions,"question1"))

        sim_scores = cos_sim(encoded_question,query_encode).tolist()

        ques_sim_score_list = []

        for question,score in zip(questions,sim_scores):
                ques_sim_score_list.append({
                        "question":question["question1"],
                        "sim_score":round(score[0],2),
                        "id":question["id"]
                })
            
        return ques_sim_score_list