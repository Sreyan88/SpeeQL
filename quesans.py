def qna_predict(question):
    from transformers import pipeline
    import tqdm
    nlp = pipeline("question-answering")
    context = open('context.txt', 'r')
    return nlp(question=question, context=context)
