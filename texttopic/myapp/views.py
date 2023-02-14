from . import text_to_picture
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .response_class import ResponseClass
import random

from functools import reduce
import spacy
import re
nlp = spacy.load("en_core_web_sm")
import copy
import ast
from random import choice

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

def lcm_numbers(nums):
    storing_output_arr = []
    increment_value = 2
    nums_base_copy = copy.deepcopy(nums)

    answer_set=[]
    answer = 1

    while(sum(nums)>len(nums)):
        nums_copy = copy.deepcopy(nums)
        value = [ True if i % increment_value == 0 else False for i in nums ]
        if True in value:
            storing_output_arr.append((increment_value,nums_copy))
            answer *= increment_value
            answer_set.append(increment_value)
            for i in range(len(nums)):
                if nums[i] % increment_value == 0:
                    nums[i] = nums[i] // increment_value  
                else:
                    nums[i] = nums[i]      

        else:
            increment_value += 1

    return nums_base_copy,storing_output_arr,answer_set,answer     

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

    dicts['numbers'] = num_list
    dicts['objects'] = object_list    

    # if len(num_list) == len(object_list):
    #     for i in range(len(num_list)):
    #         dicts[num_list[i]] = object_list[i]
    # else:
    #     for i in range(len(num_list)):
    #         dicts[num_list[i]] = object_list[0]


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

################################# Sample_question_mahesh_sir #################################

################## Identifying shapes############################
def identify_the_shape(number):

    circle_obj = 0
    square_object = 0
    triangle_object = 0

    output_object_list = []

    object_list = ["circle","triangle","square"]

    circle = [{"object":"tire","url":"https://i.ibb.co/594FR44/tire.png"},{"object":"plate","url":"https://i.ibb.co/3mzn20R/plate.png"}]

    triangle = [{"object":"hanger","url":"https://i.ibb.co/0FKqYRM/hanger.png"},{"object":"green_cap","url":"https://i.ibb.co/hLj6tyy/green-cap.png"},{"object":"blue_cap","url":"https://i.ibb.co/y5hyKRX/blue-cap.png"}]

    square = [{"object":"mobile","url":"https://i.ibb.co/rpT2J3N/mobile.png"},{"object":"window","url":"https://i.ibb.co/Htp0dWx/window.png"},{"object":"book","url":"https://i.ibb.co/W09pRjn/book.png"}]

    for i in range(number):
        rand_num = random.randint(1,3)
        if rand_num == 1:
            circle_obj += 1
            rand_num =  random.randint(0,1)
            output_object_list.append(circle[rand_num])
        elif rand_num == 2:
            triangle_object += 1
            rand_num =  random.randint(0,2)
            output_object_list.append(triangle[rand_num])
        else:
            square_object += 1
            rand_num =  random.randint(0,2)
            output_object_list.append(square[rand_num])

    output = {"objects":output_object_list,"answer":{"circle":circle_obj,"square":square_object,"triangle":triangle_object}}        

    return output  

@api_view(['GET'])
def identifying_shapes(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            
            dict_data = identify_the_shape(num_of_ques)
            
            

            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400) 
######################### Identifying Shapes ######################

######################### measuring angles ########################
def measuring_angle(number):
    question_list = []

    for i in range(number):
        angle_value = random.randrange(5,170,5)
        option_list = [
                        angle_value,
                        angle_value + 5,
                        angle_value - 5,
                        angle_value + 10
                      ]
        random.shuffle(option_list)
        data = {
                    "angle":angle_value,
                    "options":option_list,
               }
        question_list.append(data)

    return question_list    

@api_view(['GET'])
def measure_angle(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            
            dict_data = measuring_angle(num_of_ques)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400) 

######################### measuring angles ########################
def displaying_angle(number):
    question_list = []

    for i in range(number):
        angle_value = choice([i for i in range(5,75,5) if i not in [45]])
        option_list = [
                        angle_value,
                        180 - angle_value ,
                        "r "+str(180 - angle_value) ,
                        90 - angle_value
                      ]
        random.shuffle(option_list)
        data = {
                    "angle":angle_value,
                    "options":option_list,
               }
        question_list.append(data)

    return question_list  

@api_view(['GET'])
def display_angle(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            
            dict_data = displaying_angle(num_of_ques)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400) 
######################### Observing angle #########################

######################### Observing angle #########################

######################### Identifying Angles ########################
def angle_problem(number):
    question_list = []

    for i in range(number):
        obj = ["an acute angle","a complete angle","a obtuse angle","a reflex angle","a right angle","a straight angle",]
        object_list = [
    {0:{"acute_30":"https://i.ibb.co/NCc4yXm/acute-30.png"},
     1:{"acute_45":"https://i.ibb.co/W0kvMc7/acute-45.png"},
     2:{"acute_60":"https://i.ibb.co/V9JRyFg/acute-60.png"}
     },

    {0:{"complete_angle_01":"https://i.ibb.co/fMqscGL/complete-angle-01.png"},
     1:{"complete_angle_02":"https://i.ibb.co/f825TVC/complete-angle-02.png"},
     2:{"complete_angle_03":"https://i.ibb.co/DbDsJ0q/complete-angle-03.png"}
     },

    {0:{"obtuse_106":"https://i.ibb.co/pnkX6Sw/obtuse-106.png"},
     1:{"obtuse_110":"https://i.ibb.co/sjp7nnj/obtuse-110.png"},
     2:{"obtuse_120":"https://i.ibb.co/TtQ73kX/obtuse-120.png"}
     },
     
     {0:{"reflex_220":"https://i.ibb.co/0DT0tNr/reflex-220.png"},
     1:{"reflex_225":"https://i.ibb.co/tPSZy0d/reflex-225.png"},
     2:{"reflex_320":"https://i.ibb.co/gFxnxFZ/reflex-320.png"}
     },

    {0:{"rignt_angle_01":"https://i.ibb.co/TBKsBt1/rignt-angle-01.png"},
     1:{"rignt_angle_02":"https://i.ibb.co/Pr2tShZ/rignt-angle-02.png"},
     2:{"rignt_angle_03":"https://i.ibb.co/YTHNb6Q/rignt-angle-03.png"}
     },

    {0:{"straight_01":"https://i.ibb.co/0DscpnF/straight-01.png"},
     1:{"straight_02":"https://i.ibb.co/VBXnCZC/straight-02.png"},
     2:{"straight_03":"https://i.ibb.co/L6n9xqB/straight-03.png"}
     },
    ]
        rand_obj = random.randint(0,len(obj)-1)
        ques = "Which of the following is "+ obj[rand_obj]
        option = []
        answer = []
        qus_num = random.randint(0,2)
        for i in range(4):
            if i == 0:
                option.append(object_list[rand_obj][qus_num])
                answer.append(object_list[rand_obj][qus_num])
            else: 
                obj_selection = random.randint(0,len(obj)-1)
                obj_of_obj_selection = random.randint(0,2)

                if obj_selection == rand_obj:
                    option.append(object_list[rand_obj][obj_of_obj_selection])
                    answer.append(object_list[rand_obj][obj_of_obj_selection])
                else:
                    option.append(object_list[obj_selection][obj_of_obj_selection])

        random.shuffle(option)
        qus_dict = {
            "question":ques,
            "options":option,
            "answer":answer
        }
        question_list.append(qus_dict)
    return question_list

@api_view(['GET'])
def identifying_angle(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            
            dict_data = angle_problem(num_of_ques)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400) 

######################### Idntifying Angles #########################


######################### Naming Figures ############################
def naming_figures(numbers):
    question_list = []

    problem_list = [
    {
        "fig":"fig_link_01",
        "coli_points":['MOT','RON',1],
        "rays":['OR','OM','OS','OT','ON','OP',0],
        "line_seg":['OP','ON','OT','OS','OR','OM','MT','RN',1],
        "lines":['MT','RN',1]
    },
    {
        "fig":"fig_link_02",
        "coli_points":['XOA',1],
        "rays":['OB','OA','OE','OD','OX','OC',0],
        "line_seg":['OB','OA','OE','OD','OX','OC','XA',1],
        "lines":['XA',1]
    },
    {
        "fig":"fig_link_03",
        "coli_points":['BOD','AOC',1],
        "rays":['OE','OD','OC','OB','OA',0],
        "line_seg":['OE','OD','OC','OB','OA','BD','AC',1],
        "lines":['BD','AC',1]
    }]

    for num in range(numbers):
        random_question = random.randint(0,len(problem_list)-1)
        question_list.append(problem_list[random_question])

    return question_list    

@api_view(['GET'])
def naming_fig(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            
            dict_data = naming_figures(num_of_ques)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400)

######################### Naming Figures-end ########################


################################# Sample_question_mahesh_sir #################################



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
        a =request.META.get('HTTP_A')
        b =request.META.get('HTTP_B')
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
@api_view(['GET'])
def rand_ques_generator(request):
    try:
        
        question_number  = int(request.META.get('HTTP_A'))
        question_type    = request.META.get('HTTP_TYPE')

        if question_number>0 and question_number<11 and question_type:
             
            dict_data = question(question_type, question_number )
        
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "question and question type cannot be empty,or zero, or greater than 10")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called question and question_type")
            return JsonResponse(response_obj.__dict__, status=400)   


################################## Random_Number_Generator_Section ends #################


###################################### Count_pictures_and_add section ####################
@api_view(['GET'])
def counting_pictures(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques>0 and num_of_ques<11:
            object_list =["Fish","Ball","Finger","Pen","Pencil","Rubber"]
            dict_data = [0]*num_of_ques
            
            for i in range(num_of_ques):
                num_01 = random.randint(1,10)
                num_02 = random.randint(1,10)
                object_num = random.randint(0,5)

                object = object_list[object_num]
                ans = num_01 + num_02
                dicct = {
                    "object":object,
                    "count":[num_01,num_02],
                    "answer":ans
                }
                dict_data[i] = dicct
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero, or greater than 10")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field for number")
            return JsonResponse(response_obj.__dict__, status=400)   

################################ Count_pictures_and_add_section end ######################

#################################### Fraction_Section ###################################

@api_view(['GET'])
def fraction_question_generator(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 and num_of_ques <11:
            
            dict_data = {}
            
            for i in range(num_of_ques):
                fraction_output = fraction_question()
                dict_data[i] = fraction_output

            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "input cannot be zero, or greater than 10")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field specified")
            return JsonResponse(response_obj.__dict__, status=400) 

##################################### Fraction_Section_end ##############################

############################### API for generating qustions objects,numbers and operations #
@api_view(['GET'])
def obtaining_objects(request):
    try:
        question = str(request.META.get('HTTP_QUESTION'))
    
        if question:
            if text_to_picture.validate_question(question):
                operation = text_to_picture.find_operation(question)
                numbers =  text_to_picture.find_numbers(question)
                subjects =  text_to_picture.find_subject(question)
                dicct = {
                    "Question":question,
                    "Operation":operation,
                    "numbers":numbers,
                    "objects":subjects
                }
                response_obj = ResponseClass(200, "Add Successful",dicct)
                return JsonResponse(response_obj.__dict__, status=200)
            else:
                response_obj = ResponseClass(206, "Text is not proper")
                return JsonResponse(response_obj.__dict__, status=206)
        else:
            response_obj = ResponseClass(400, "Question can not be empty")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called question")
            return JsonResponse(response_obj.__dict__, status=400)

##################################### LCM ###########################################
@api_view(['GET'])
def LCM_numbers(request):
    try:
        list_a ="".join(request.META.get('HTTP_LIST'))

        
        integer_list = ast.literal_eval(list_a)
        
        
        if len(integer_list)>1 and len(integer_list)<5:
            nums_base_copy,storing_output_arr,answer_set,answer  = lcm_numbers(integer_list)
            c = [
                {   "Passed_List":nums_base_copy,
                    "Vertical_Arrangement":storing_output_arr,
                    "Answer_Set":answer_set,
                    "Answer":answer
                }
            ] 
            
            response_obj = ResponseClass(200, "Add Successful",c)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "list cannot be empty, pass two to four numbers list")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called list")
            return JsonResponse(response_obj.__dict__, status=400)
                       