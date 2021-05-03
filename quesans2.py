def qna_predict2(question):
    from transformers import DistilBertTokenizer, DistilBertForQuestionAnswering
    import torch
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased',return_token_type_ids = True)
    model = DistilBertForQuestionAnswering.from_pretrained('distilbert-base-uncased-distilled-squad')

    # context = "SpeeQL is a design concept store, "           "SpeeQL is located in Bangalore India,"           "We sell products which includes Ariel, Ambi pur, Duracell, Gillette, Head & Shoulders, Olay, Oral-B, Pampers, Pantene, Tide, Vicks, Whisper and Wella "           "The best brand for anti-dandruff shampoo is Head and Shoulders, "           "The product categorizations are : Beauty Segment, Grooming Segment, Health Care Segment, Snacks & Pet Care Segment, Fabric Care & Home Care Segment, Baby Care & Family Home Care Segment, "           "The Main categories of this Beauty Segment consists of Shampoo, conditioners, women's skin care, hair care products conditioners and styling, "           "Head & Shoulders is one of the best and recommended brands for anti-dandruff shampoo,"           "Head & Shoulders is available in Anti Hair Fall Shampoo, Itchy scalp care Shampoo, Complete Care for Dry Scalp Shampoo, Cool Menthol Shampoo, Men Hair Retain Shampoo, Lemon Fresh Shampoo, Silky Black Shampoo, Smooth & Silky Shampoo, "           "Olay is one of the most famous and recommended brands for beauty creams, "           "Pantene is one of the best and recommended brand of hair care conditioners."           "Oral-B is one of the best and recommended brands of toothbrush, and oral care products."           "We have shampoo in stock, "           "Shampoo\s are located in Shelf 1, "          "Baby Products are located in Shelf 12, "          "Shelf 12 is located the third aisle, "          "Shelf 1 is located the first aisle, "          "Shelf 3 is located the second aisle, "
    # question = "Where are Beauty-Products located ?"
    context = open('context.txt')
    context = context.read()
    encoding = tokenizer.encode_plus(question, context)


    input_ids, attention_mask = encoding["input_ids"], encoding["attention_mask"]

    start_scores, end_scores = model(torch.tensor([input_ids]), attention_mask=torch.tensor([attention_mask]))

    ans_tokens = input_ids[torch.argmax(start_scores) : torch.argmax(end_scores)+1]
    answer_tokens = tokenizer.convert_ids_to_tokens(ans_tokens , skip_special_tokens=True)

    print ("\nQuestion ",question)

    answer_tokens_to_string = tokenizer.convert_tokens_to_string(answer_tokens)

    print ("\nAnswer : ",answer_tokens_to_string)
    return answer_tokens_to_string
