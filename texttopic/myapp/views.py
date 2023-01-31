from . import text_to_picture
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .response_class import ResponseClass
import random

from functools import reduce
import spacy
import re
nlp = spacy.load("en_core_web_sm")

############################################## Fahads Code ###########################

Add_question = "Anand has 27 stickers. He bought 5 more. How many stickers does he have?" 
Sub_question = "Anand has 27 stickers. He gives 5 stickers to Sita. How many stickers does Anand left?"
Multi_question = "Anand has 27 stickers. He bought each of 5 rupees. What is the total cost?"
Div_question = "Anand has 9 stickers. He distrubted among 3 children. How much stickers does each child got?"


def subs():
    Subtrahend  = random.randint(1,5)
    Minuend  = random.randint(6,10)
    return Subtrahend ,Minuend 

def division():
    lst = [6,8,9,10,12,15,16,18,20,21,24,25]
    Dividend = random.choice(lst)
    while True:
        Divisor = random.randint(2,7)
        
        if Dividend%Divisor == 0:
            return Divisor,Dividend

def random_question_generator_add():
    names_list = ["Anil","Sunil","Shyam","Ronit","Vinshnu","Fahad","Nitin","Josh","Rahul","Amit"]
    objects_list = ["Balls","Bats","Rubbers","Books","Apples","Oranges"]
    text = Add_question
    
    doc = nlp(Add_question)

    for token in doc:
        if token.pos_ == "PROPN":
            text = re.sub(token.text, names_list[random.randint(0,len(names_list)-1)], text)
        elif token.pos_ == "NUM": 
            text = re.sub(token.text, str(random.randint(1,8)), text)  
        elif token.pos_ == "NOUN" and token.dep_ == "dobj" :
            text = re.sub(token.text, objects_list[random.randint(0,len(objects_list)-1)], text) 
        else:
            pass   
    
    doc = nlp(text)
    lst = []
    for token in doc:
        if token.pos_ == "NUM":
            num = str(token)
            num = int(num)
            lst.append(num)   
    #multiplication = reduce((lambda x, y: x * y), lst)
    return text, sum(lst)

def random_question_generator_multi():
    names_list = ["Anil","Sunil","Shyam","Ronit","Vinshnu","Fahad","Nitin","Josh","Rahul","Amit"]
    objects_list = ["Ball","Bat","Pencil","Rubber","Books","Apples","Oranges"]
    text = Multi_question
    
    doc = nlp(Multi_question)

    for token in doc:
        if token.pos_ == "PROPN":
            text = re.sub(token.text, names_list[random.randint(0,len(names_list)-1)], text)
        elif token.pos_ == "NUM": 
            text = re.sub(token.text, str(random.randint(1,8)), text)  
        elif token.pos_ == "NOUN" and token.dep_ == "dobj" :
            text = re.sub(token.text, objects_list[random.randint(0,len(objects_list)-1)], text) 
        else:
            pass   
    
    doc = nlp(text)
    lst = []
    for token in doc:
        if token.pos_ == "NUM":
            num = str(token)
            num = int(num)
            lst.append(num)   
    multiplication = reduce((lambda x, y: x * y), lst)
    return text, multiplication  

def random_question_generator_subtract():
    names_list = ["Anil","Sunil","Shyam","Ronit","Vinshnu","Fahad","Nitin","Josh","Rahul","Amit"]
    objects_list = ["Ball","Bat","Pencil","Rubber","Books","Apples","Oranges"]
    text = Sub_question
    
    doc = nlp(Sub_question)
    Subtrahend , Minuend = subs()

    text = text.replace("27", str(Minuend)) 
    text = text.replace("5", str(Subtrahend)) 

    for token in doc:
        if token.pos_ == "PROPN":
            text = re.sub(token.text, names_list[random.randint(0,len(names_list)-1)], text)
        elif token.pos_ == "NOUN" and token.dep_ == "dobj" :
            text = re.sub(token.text, objects_list[random.randint(0,len(objects_list)-1)], text) 
        else:
            pass 

    difference = Minuend - Subtrahend   
    return text , difference

def random_question_generator_divide():
    names_list = ["Anil","Sunil","Shyam","Ronit","Vinshnu","Fahad","Nitin","Josh","Rahul","Amit"]
    objects_list = ["Ball","Bat","Pencil","Rubber","Books","Apples","Oranges"]
    text = Div_question
    
    Divisor, Dividend = division()
    #print(Dividend,Divisor)
    text = text.replace("9", str(Dividend)) 
    text = text.replace("3", str(Divisor))
    text = text.replace("Anand", names_list[random.randint(0,len(names_list)-1)]) 
    text = text.replace("stickers", objects_list[random.randint(0,len(objects_list)-1)])
    quotient = Dividend/Divisor  
    #print(quotient)
    return text, quotient

def question(question_type, question_number ):
    #print("Hey")
    if question_type == "addition":
        lst_add = []
        for i  in range(question_number):
            question_add = {}
            text, addition = random_question_generator_add()
            obj_extractor = numbers_and_object_extracor(text)
            question_add.update({'Question':text})
            question_add.update({'Answer':addition})
            # obj_extractor = numbers_and_object_extracor(text)
            question_add.update({'Objects':obj_extractor})
            lst_add.append(question_add)
        return lst_add
    elif question_type == "multiplication":
        lst_multi = []
        for i  in range(question_number):
            question_multi = {}
            text, multiplication = random_question_generator_multi()
            question_multi.update({'Question':text})
            question_multi.update({'Answer':multiplication})
            obj_extractor = numbers_and_object_extracor(text)
            question_multi.update({'Objects':obj_extractor})
            lst_multi.append(question_multi)
            #lst_multi.append(random_question_generator_add_and_multi(question_name ))
        return lst_multi
    elif question_type == "subtraction":
        lst_sub = []
        for i  in range(question_number):
            question_sub = {}
            text, difference = random_question_generator_subtract()
            question_sub.update({'Question':text})
            question_sub.update({'Answer':difference})
            obj_extractor = numbers_and_object_extracor(text)
            question_sub.update({'Objects':obj_extractor})
            lst_sub.append(question_sub)
            #lst_sub.append(random_question_generator_subtract(question_name ))
        return lst_sub
    elif question_type == "division":
        lst_div = []
        for i  in range(question_number):
            question_div = {}
            text, quotient = random_question_generator_divide()
            quotient = int(quotient)
            question_div.update({'Question':text})
            question_div.update({'Answer':quotient})
            obj_extractor = numbers_and_object_extracor(text)
            question_div.update({'Objects':obj_extractor})
            lst_div.append(question_div)
            #lst_div.append(random_question_generator_divide(question_name ))
        #print(lst_div)
        return lst_div

#ans = question("/","10 div 2",15)
#print(ans)


############################################## Fahads Code-end #######################

################################################ number_and_object_extractor ###########
def numbers_and_object_extracor(question):
    doc = nlp(question)

    num_list = []
    object_list = []
    dicts = {}

    for token in doc:
        
        if token.pos_ == "NUM": 
            num_list.append(token.text)  
        elif (token.pos_ == "PROPN" and token.dep_ == "dobj") or (token.pos_ == "NOUN" and token.dep_ == "dobj"):
            object_list.append(token.text) 
        else:
            pass  

    if len(num_list) == len(object_list):
        for i in range(len(num_list)):
            dicts[num_list[i]] = object_list[i]
    else:
        for i in range(len(num_list)):
            dicts[num_list[i]] = object_list[0]


    return dicts    
################################################ number_and_object_extractor-end #######

################################ Fraction_Section_Functions ################################
def fraction_question( ):
    question_set = {
        1:
        {
            1:{"question":"What fraction of people have Green hats?","option_01":"3/15","option_02":"1/5","option_03":"4/15","option_04":"3/16","ans":"3/15"},
            2:{"question":"What fraction of people have Red hats?","option_01":"3/15","option_02":"4/15","option_03":"5/15","option_04":"3/16","ans":"4/15"},
            3:{"question":"What fraction of people have Blue hats?","option_01":"4/15","option_02":"1/5","option_03":"4/16","option_04":"3/15","ans":"3/15"},
            4:{"question":"What fraction of people have Yellow hats?","option_01":"3/15","option_02":"1/5","option_03":"4/15","option_04":"3/16","ans":"3/15"},
            5:{"question":"What fraction of people have Black hats?","option_01":"3/15","option_02":"1/5","option_03":"2/15","option_04":"3/16","ans":"2/15"},
        },
        2:
        {
            1:{"question":"What fraction of people have Green hats?","option_01":"3/15","option_02":"1/5","option_03":"4/15","option_04":"None","ans":"None"},
            2:{"question":"What fraction of people have Red hats?","option_01":"3/15","option_02":"2/12","option_03":"5/15","option_04":"3/16","ans":"2/12"},
            3:{"question":"What fraction of people have Blue hats?","option_01":"4/15","option_02":"1/5","option_03":"5/12","option_04":"3/15","ans":"5/12"},
            4:{"question":"What fraction of people have Yellow hats?","option_01":"3/15","option_02":"1/5","option_03":"4/12","option_04":"3/16","ans":"4/12"},
            5:{"question":"What fraction of people have Orange hats?","option_01":"3/15","option_02":"1/12","option_03":"2/15","option_04":"3/16","ans":"2/15"},
        },
        3:
        {
            1:{"question":"What fraction of people have Green hats?","option_01":"3/13","option_02":"1/5","option_03":"4/13","option_04":"3/16","ans":"4/13"},
            2:{"question":"What fraction of people have Red hats?","option_01":"3/13","option_02":"1/13","option_03":"5/15","option_04":"3/16","ans":"1/13"},
            3:{"question":"What fraction of people have Blue hats?","option_01":"4/15","option_02":"4/13","option_03":"4/16","option_04":"3/15","ans":"4/13"},
            4:{"question":"What fraction of people have Yellow hats?","option_01":"1/13","option_02":"1/5","option_03":"4/13","option_04":"3/16","ans":"1/13"},
            5:{"question":"What fraction of people have Black hats?","option_01":"3/13","option_02":"1/5","option_03":"1/13","option_04":"3/16","ans":"1/13"},
        },
        4:
        {
            1:{"question":"What fraction of people have Green hats?","option_01":"3/14","option_02":"6/14","option_03":"4/14","option_04":"3/16","ans":"3/14"},
            2:{"question":"What fraction of people have Red hats?","option_01":"1/14","option_02":"1/13","option_03":"5/15","option_04":"3/16","ans":"1/14"},
            3:{"question":"What fraction of people have Blue hats?","option_01":"4/15","option_02":"6/14","option_03":"4/16","option_04":"3/15","ans":"6/14"},
            4:{"question":"What fraction of people have Yellow hats?","option_01":"1/13","option_02":"1/5","option_03":"2/14","option_04":"3/16","ans":"2/14"},
            5:{"question":"What fraction of people have Purple hats?","option_01":"2/14","option_02":"1/5","option_03":"1/13","option_04":"3/16","ans":"2/14"},
        }, }

    random_image = random.randint(1,4) 
    random_question = random.randint(1,5)    

    output_dict = {
        "image": random_image,
        "question":question_set[random_image][random_question],

    }
    return output_dict
################################ Fraction_Section_Functions_end ################################


@api_view(['GET'])
def convert_text_q_to_picture_q(request):
    try:
        question = request.META.get('HTTP_QUESTION')
        # question = request.data['question']
        if question:
            if text_to_picture.validate_question(question):
                img = text_to_picture.convert_text_to_pic(question)
                return img
            else:
                response_obj = ResponseClass(206, "Text is not proper")
                return JsonResponse(response_obj.__dict__, status=206)
        else:
            response_obj = ResponseClass(400, "Question can not be empty")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called question")
            return JsonResponse(response_obj.__dict__, status=400)


@api_view(['POST'])
def convert_pictorial_text_q_to_picture_q(request):
    try:
        image = request.data['image']
        question_text = text_to_picture.get_question_from_image(image)
        question_set = text_to_picture.get_all_questions(question_text)
        if question_set:
                img = text_to_picture.convert_set_of_text_to_pic(question_set)
                return img
        else:
            response_obj = ResponseClass(400, "Image does not have a question")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called image")
            return JsonResponse(response_obj.__dict__, status=400)

###################################### Practice-Starts ################################
@api_view(['GET'])
def addition_by_get(request):
    try:
        a =int( request.META.get('HTTP_A'))
        b =int( request.META.get('HTTP_B'))
        # question = request.data['question']
        if a and b:
            c = a+b
            response_obj = ResponseClass(200, "Add Successful",c)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "a and b cannot be empty")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called a nad b")
            return JsonResponse(response_obj.__dict__, status=400)

# @api_view(['POST'])
# def addition_by_post(request):
#     try:
#         a =int( request.data["a"])
#         b =int( request.data["b"])
#         # question = request.data['question']
#         if a and b:
#             c = a+b
#             dicct = {
#                 "num1":a,
#                 "num2":b,
#                 "ans":c
#             }
#             response_obj = ResponseClass(200, "Add Successful",dicct)
#             return JsonResponse(response_obj.__dict__, status=200)
#         else:
#             response_obj = ResponseClass(400, "a and b cannot be empty")
#             return JsonResponse(response_obj.__dict__, status=400)

    # except KeyError as e:
    #         response_obj = ResponseClass(400, "no field called a nad b")
    #         return JsonResponse(response_obj.__dict__, status=400)


@api_view(['POST'])
def addition_by_post(request):
    try:
        num_of_ques = int(request.data["num"])
        if num_of_ques:

            dict_data = {}
            # a =int( request.data["a"])
            # b =int( request.data["b"])
            # question = request.data['question']
            for i in range(num_of_ques):
                a = random.randint(1,10)
                b = random.randint(1,10)
                c = a + b
                dicct = {
                    "num1":a,
                    "num2":b,
                    "answer":c
                }
                dict_data[i] = dicct
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "a and b cannot be empty")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called a nad b")
            return JsonResponse(response_obj.__dict__, status=400)
################################# Practice-ends #########################################

################################## Random_Number_Generator_Section ######################
@api_view(['POST'])
def rand_ques_generator(request):
    try:
        
        question_number  = int(request.data["number_of_questions"])
        question_type    = request.data["operation_type"]

        if question_number and question_type:
             
            dict_data = question(question_type, question_number )
        
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "a and b cannot be empty")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called a nad b")
            return JsonResponse(response_obj.__dict__, status=400)   


################################## Random_Number_Generator_Section ends #################


###################################### Count_pictures_and_add section ####################
@api_view(['POST'])
def count_pictures_and_add(request):
    try:
        num_of_ques = int(request.data["num_of_questions"])
        if num_of_ques:
            object_list =["Fish","Ball","Finger","Pen","Pencil","Rubber"]
            dict_data = {}
            
            for i in range(num_of_ques):
                num_01 = random.randint(1,10)
                num_02 = random.randint(1,10)
                object_num = random.randint(0,5)

                object = object_list[object_num]
                ans = num_01 + num_02
                dicct = {
                    "obj_01":{num_01:object},
                    "obj_02":{num_02:object},
                    "answer":{ans:object}
                }
                dict_data[i] = dicct
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "a and b cannot be empty")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called a nad b")
            return JsonResponse(response_obj.__dict__, status=400)   

################################ Count_pictures_and_add_section end ######################

#################################### Fraction_Section ###################################

@api_view(['POST'])
def fraction_question_generator(request):
    try:
        num_of_ques = int(request.data["num_of_questions"])
        if num_of_ques:
            
            dict_data = {}
            
            for i in range(num_of_ques):
                fraction_output = fraction_question()
                dict_data[i] = fraction_output

            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "a and b cannot be empty")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called a nad b")
            return JsonResponse(response_obj.__dict__, status=400) 

##################################### Fraction_Section_end ##############################