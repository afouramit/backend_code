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

############################################# text-to-speech #########################
from django.http import FileResponse
from rest_framework.decorators import api_view

from gtts import gTTS
import io

from googletrans import Translator
translator = Translator()

def generate_audio(text,lang):
    out = translator.translate(text,dest=lang)
    tts = gTTS(text=out.text, lang=lang)
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    response = FileResponse(fp, content_type='audio/mpeg')
    response['Content-Disposition'] = 'attachment; filename="audio.mp3"'
    return response

@api_view(['GET'])
def text_to_speech(request):
    try:
        
        text  = request.META.get('HTTP_TEXT')
        lang    = request.META.get('HTTP_LANG')

        if text and lang:
             
            dict_data = generate_audio(text,lang)
            return dict_data
        else:
            response_obj = ResponseClass(400, "text and lang parameter cannot be null")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called text and lang")
            return JsonResponse(response_obj.__dict__, status=400) 


############################################# text-to-speech end #########################



############################################# Text-to-Text ###########################
from googletrans import Translator
translator = Translator()
def text_to_text_conversion(text,lang):
    out = translator.translate(text,dest=lang)
    return {"converted_text":out.text}

@api_view(['GET'])
def txt_to_txt(request):
    try:
        
        text  = request.META.get('HTTP_TEXT')
        lang    = request.META.get('HTTP_LANG')

        if text and lang:
             
            dict_data = text_to_text_conversion(text,lang)
        
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "text and lang parameter cannot be null")
            return JsonResponse(response_obj.__dict__, status=400)

    except KeyError as e:
            response_obj = ResponseClass(400, "no field called text and lang")
            return JsonResponse(response_obj.__dict__, status=400) 



############################################# Text-to-Text-end #######################

############################################## Fahads Code ###########################

Add_question = "Anand has 27 stickers. Nitin has 5 stikers. How many stickers they have together?" 
Sub_question = "Anand has 27 stickers. He gives 5 stickers to Sita. How many stickers does Anand left?"
Multi_question = "Anand has 27 stickers. He bought each of 5 rupees. What is the total cost?"
Div_question = "Anand has 9 stickers. He distrubted among 3 children. How much stickers does each child got?"

def text_explanation(answer,question_type,obj_extractor,version=None):
    
    if question_type == "addition":
        
        if version == '5':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]

            start = int(num_01)
            end = int(num_01) + int(num_02)

            numbers = [str(num) for num in range(start, end + 1)]
            result = ','.join(numbers)

            ques = f"{num_01} + {num_02} = ?"

            text_exp ={
                        0 : {
                                "commentary" : f"We are asked to find out {num_01} + {num_02} = how much?",
                            },
                        1 : {
                                "commentary" : f"We know that addition is bringing things together or mixing them. It means we will mix  or add {num_02} objects to {num_01} objects and count the total.",
                            },  
                        2 : {
                                "commentary" : f"We already have {num_01} objects & after adding {num_02} more they will increase by {num_02}.Counting all of them together will give us the answer.",
                            },        
                        3 : {
                                "commentary" : f"To achieve this we will count {num_02} ahead of {num_01}. i.e {result}",  
                            }, 
                        4 : {
                                "commentary" : f"This is called as forward counting. Let us see how we can do this .",  
                            }, 
                        5 : {
                                "commentary" : f"We have {num_01}. We want to further count {num_02} more.This process can be done in 2 ways.",  
                            }, 
                        6 : {
                                "commentary" : f"Method 1: We will count further by one every time which is same as adding one.This will be done as many times equal to the number to be added. Let us repeat it {num_02} times as we are to add {num_02}.",  
                            },   
                        7 : {
                                "commentary" : f"This way we have added one {num_02} times to {num_01} to get the answer as {num_01}+{num_02}={answer}",  
                            }, 
                        8 : {
                                "commentary" : f"Method 2: Alternatively we can do the same addition as follows. We will start with {num_01} and count {num_02} numbers forward to get the answer.",  
                            },   
                        9 : {
                                "commentary" : f"Thus we have added {num_02} to {num_01} to get the answer, as {answer}. Thus our answer is {answer} and is written as {num_01}+{num_02}={answer}",  
                            },
                        10 : {
                                "commentary" : f"Thus {num_01}+{num_02} is found out by counting {num_02} ahead of {num_01}. i.e {result}",  
                            },   
                        11 : {
                                "commentary" : f"This is called as forward counting.",  
                            },                             
                    }
        elif version == '4':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            first_name = extracted_objects['names'][0]
            if len(extracted_objects['names']) == 2:
                second_name = extracted_objects['names'][1]
                if first_name == second_name:
                    second_name = "Akshay"
            else:
                second_name = "Akshay"


            ques = f"{first_name}  has {num_01} {object} and {second_name} has {num_02} {object}. How many {object} they have together ?"

            text_exp ={
                0 : {
                        "commentary" : f"To find how many {object} {first_name} and {second_name} have together,we need to do the addition of the {object} each of them have,",
                    },
                1 : {
                        "commentary" : f"To find the total, read out numbers next to the number of {object} {first_name} has.",
                    },  
                2 : {
                        "commentary" : f"{first_name} has {num_01} {object} and {second_name} has {num_02} {object}. To find the total number of {object}, count {num_02} numbers next to {num_01}.",
                    },        
                3 : {
                        "commentary" : f"Thus it would be ",   
                    },    
                4 : {
                        "commentary" : f"Therefore the total number of {object} are {int(num_01) + int(num_02)}.",   
                    },               
            }   

        elif version == '3':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]

            ques = f"{num_01} + {num_02} = ?"

            text_exp ={
                        0 : {
                                "commentary" : f"Here plus sign indicates addition",
                            },
                        1 : {
                                "commentary" : f"Addition is nothing but bringing the things together or mixing the things together or joining the things together or combining two or more things together.",
                            },  
                        2 : {
                                "commentary" : f"For example,Let Umesh has {num_01} {object} in one basket.",
                            },        
                        3 : {
                                "commentary" : f"and Rahim has {num_02} {object} in other basket",  
                            }, 
                        4 : {
                                "commentary" : f"To add them together, we need to combine {num_01} and {num_02} {object}.",  
                            }, 
                        5 : {
                                "commentary" : f"Now let us count these combined {object}.",  
                            }, 
                        6 : {
                                "commentary" : f"Mathematically this is represented as.",  
                            },   
                        7 : {
                                "commentary" : f"Therefore {num_01} plus {num_02} is equal to {int(num_01) + int(num_02)}.",  
                            },                     
                    }
            
        elif version == '2':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]

            ques = f" There are {num_01} {object} in one basket. And {num_02} {object} in another basket. How many total {object} are there? "
            
            text_exp ={
                0 : {
                        "commentary" : f"There are {num_01} {object} in one basket",
                    },
                1 : {
                        "commentary" : f"And {num_02} {object} in another basket.",
                    },  
                2 : {
                        "commentary" : f"To find the answer for this we need to combine the {object} from both the baskets together in a new basket.",
                    },        
                3 : {
                        "commentary" : f"This is called addition. Addition is nothing but bringing the things together or mixing the things together or joining the things together or combining two or more things together.",      
                    }, 
                4 : {
                        "commentary" : f"Now let us count these combined {object}.",      
                    }, 
                5 : {
                        "commentary" : f"Mathematically this is represented as",      
                    }, 
                6 : {
                        "commentary" : f"This sign is called equal to and it represents result.",      
                    }, 
                7 : {
                        "commentary" : f"So the total number of {object} are {int(num_01) + int(num_02)}.",      
                    },                               
            } 

        elif version == '1':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            
            ques = f"There are some {object} in one basket. And  some {object} in another basket.How many total {object} are there ?"

            text_exp ={
                0 : {
                        "commentary" : f"There are some {object} in one basket",
                    },
                1 : {
                        "commentary" : f"And some {object} in another basket.",
                    },  
                2 : {
                        "commentary" : f"To find the answer for this we need to combine the {object} from both the baskets together.",
                    },        
                3 : {
                        "commentary" : f"This is called addition and it is symbolically represented as.",      
                    }, 
                4 : {
                        "commentary" : f"This sign is called plus and it represents addition.",      
                    }, 
                5 : {
                        "commentary" : f"Addition is nothing but bringing the things together or mixing the things together or joining the things together or combining two or more things together.",      
                    }, 
                6 : {
                        "commentary" : f"Now let us count these combined (total) {object}.",      
                    }, 
                7 : {
                        "commentary" : f"So the total number of {object} are {int(num_01) + int(num_02)}.",      
                    },                               
            } 
        return ques,text_exp 
        
    if question_type == "subtraction":
        if version == '1':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            

            ques = f"There are some {object} in the basket.Some {object} were given away and are shown as highlighted {object}. How many {object} are remaining?"

            text_exp ={
                0 : {
                        "commentary" : f"There are some {object} in the basket. some of them were given away and are shown as highlighted {object}.",
                    },
                1 : {
                        "commentary" : f"Let us understand the meaning of this action .",
                    },  
                2 : {
                        "commentary" : f"Of the given quantity, when something is removed, taken away, broken, something is eaten, damaged, given away, lost, used, consumed, etc. we know that all such processes reduce the original quantity.",
                    },        
                3 : {
                        "commentary" : f"And this process is called subtraction .",      
                    }, 
                4 : {
                        "commentary" : f"Now the {object} which are not highlighted are the  remaining {object} and we see them in the basket .Here we have removed the {object} which are already given away.",      
                    }, 
                5 : {
                        "commentary" : f" Now let us count the remaining {object}",      
                    }, 
                6 : {
                        "commentary" : f"Therefore the remaining {object} are {answer} is the answer ",      
                    },                               
            } 

        if version == '2':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            first_name = extracted_objects['names'][0]

            ques = f"There are {num_01} {object} in the basket.{first_name} took {num_02} {object} from it. How many {object} are remaining?"

            text_exp ={
                0 : {
                        "commentary" : f"We can see that there are some {object} in the basket and they are {num_01} {object}.",
                    },
                1 : {
                        "commentary" : f"{first_name}  took {num_02} {object} from this basket.",
                    },  
                2 : {
                        "commentary" : f"To find the remaining {object} we need to take out {num_02} {object} from {num_01} {object}.",
                    },        
                3 : {
                        "commentary" : f"while we remove {num_02} {object} from basket, the {object} in the basket are decreasing.",      
                    }, 
                4 : {
                        "commentary" : f"Now we see the remaining {object} in the basket.",      
                    }, 
                5 : {
                        "commentary" : f"Let us understand the meaning of this action. We are removing {object} from the basket. Thus the {object} remaining in the basket are getting reduced. Taking out something, giving away, being used, being consumed, separating out, being damaged, being eaten, being thrown away etc. all such similar actions decreases the original quantity.This is called subtraction",      
                    }, 
                6 : {
                        "commentary" : f"Now let us count the remaining {object} in the basket one by one. ",      
                    }, 
                7 : {
                        "commentary" : f"Therefore the remaining {object} are {answer}",      
                    },    
                8: {
                        "commentary" : f"Mathematically this is represented as {num_01} - {num_02} = {answer}. ",      
                    },  
                9: {
                        "commentary" : f"This sign is called minus and it represents the process of subtraction, or we simply call it as subtraction. ",      
                    },                               
            } 
        if version == '3':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            

            ques = f"{num_01} - {num_02} = ?"

            text_exp ={
                0 : {
                        "commentary" : f"Here minus sign indicates subtraction.",
                    },
                1 : {
                        "commentary" : f"We are already aware, that when something is being taken out, giving away, being used, being consumed, separated out, being damaged, being eaten, being thrown away and such similar actions leads to process of Subtraction.",
                    },  
                2 : {
                        "commentary" : f"Here in all these actions, remaining quantity is always less than the original quantity and original quantity gets reduced.",
                    },        
                3 : {
                        "commentary" : f"This is a Subtraction problem.To find the answer for this we need to subtract {num_02} from {num_01}. This is same as taking out {num_02} things from {num_01} things and then count remaining to get the answer.",      
                    }, 
                4 : {
                        "commentary" : f"For example, Let Radhika has {num_01} {object} in the basket.",      
                    }, 
                5 : {
                        "commentary" : f" Rosy took out {num_02} {object} from the basket for herself. To find the remaining {object}, let us take away {num_02} {object} from {num_01} {object}. ",      
                    }, 
                6 : {
                        "commentary" : f"After removing {num_02} {object}, the remaining {object} in the basket will be the answer. So, let us count these remaining {object}.",      
                    },
                7 : {
                        "commentary" : f"Therefore the remaining {object} are {answer} is the answer "
                    },                                   
            } 

        if version == '4':
            extracted_objects = obj_extractor
            num_01 = extracted_objects['numbers'][0]
            num_02 = extracted_objects['numbers'][1]
            object = extracted_objects['objects'][0]
            first_name = extracted_objects['names'][0]

            ques = f"One shop has {num_01} {object}. Out of those {num_02} {object} were sold. How many {object} are left in the shop?"

            text_exp ={
                0 : {
                        "commentary" : f"There are {num_01} {object}.",
                    },
                1 : {
                        "commentary" : f"Out of these {num_01} {object}, {num_02} were sold.",
                    },  
                2 : {
                        "commentary" : f"To find remaining {object}, we need to remove those {object} which were sold.",
                    },        
                3 : {
                        "commentary" : f"We will highlight the {num_02} sold {object}.",      
                    }, 
                4 : {
                        "commentary" : f"As we have highlighted the {num_02} sold {object}, this is a subtraction. Thus it is a subtraction of {num_02} from {num_01}.",      
                    }, 
                5 : {
                        "commentary" : f"There are 2 methods by which this can be done.",      
                    }, 
                6 : {
                        "commentary" : f"Method 1: To find the remaining {object}, we can count the number of {object} which are not highlighted. And they come out to be {answer}. And mathematically can be written as {num_01}   -   {num_02}   =   {answer} is the answer. ",      
                    }, 
                7 : {
                        "commentary" : f"Method 2: Out of {num_01} {object}, it is given that {num_02} were sold. It means we still have some {object} left. So, we will start counting only non-highlighted from {num_02} onwards till we count all.",      
                    },    
                8: {
                        "commentary" : f"Therefore there are {answer} {object} remained in the shop, is the answer.",      
                    },  
                9: {
                        "commentary" : f" It can be written mathematically as, {num_01}   -   {num_02}   =   {answer} is the answer. ",      
                    },                               
            } 
    
        return ques,text_exp     
    
    if question_type == "multiplication":
        object = obj_extractor["objects"][0]
        num_01 = int(obj_extractor['numbers'][0])
        num_02 = int(obj_extractor['numbers'][1])

        number_word_list = ["first","second","third","fourth","fifth","sixth","Seventh","Eighth","Ninth","Tenth"]
        Dict = dict()
        num_list = list()
        for i in range(num_01):
                if i == 0:
                    num_list.append(str(num_02))
                else:    
                    num_list.append(f"+{num_02}")     

        for i in range(4):
            
            if i == 0 :
                Dict[i] = {"commentary":"The result of multiplication can be obtained by repeatative addition."}
            if i == 1 :
                Dict[i] = {"commentary":f"Each {object} costs {num_02} rupees .To find total cost we have to add {num_02}, {num_01} times ."} 
            if i == 2:
                Dict[i] = {"commentary":f"The total cost now is {''.join(num_list)} = {answer} "}
            if i == 3:
                Dict[i] = {"commentary":f"So, the total cost of all {object} is {answer} ruppees"}
                text_exp = Dict  

    if question_type == "division":
        object = obj_extractor["objects"][0]
        num_01 = int(obj_extractor['numbers'][0])
        num_02 = int(obj_extractor['numbers'][1])

        text_exp = dict()
        for i in range(3):
            if i == 0 :
                text_exp[i] = {"commentary":",The result of Division can be obtained by repeatative Subtraction and is represented by '%' sign"}
            if i == 1 :
                text_exp[i] = {"commentary":f"We shall make set of {num_02} {object}, and repeatedly, move it to the second mat, untill there remains 0 {object} on first mat"}
            else: 
                pass     
                                         
    return text_exp


def subs():
    Subtrahend  = random.randint(2,5)
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
    # objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Bears","Cupcakes","Donuts","Lanterns","Toys","Ducks"]
    objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Cupcakes","Donuts","Lanterns","Toys"]
    # ["Apples", "Oranges", "Bats", "Balls", "Books"]
    text = Add_question
    
    doc = nlp(Add_question)

    for token in doc:
        if token.pos_ == "PROPN":
            text = re.sub(token.text, names_list[random.randint(0,len(names_list)-1)], text)
        elif token.pos_ == "NUM": 
            text = re.sub(token.text, str(random.randint(2,8)), text)  
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
    # objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Bears","Cupcakes","Donuts","Lanterns","Toys","Ducks"]
    objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Cupcakes","Donuts","Lanterns","Toys"]
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
    # objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Bears","Cupcakes","Donuts","Lanterns","Toys","Ducks"]
    objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Cupcakes","Donuts","Lanterns","Toys"]
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
    # objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Bears","Cupcakes","Donuts","Lanterns","Toys","Ducks"]
    objects_list = ["Apples","Oranges","Bats","Balls","Pens","Books","Cupcakes","Donuts","Lanterns","Toys"]
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
    
    if question_type == "addition":
        lst_add = []
        for i  in range(question_number):
            question_add = {}
            text, addition = random_question_generator_add()
            obj_extractor = numbers_and_object_extracor(text)
            question_add.update({'Question':text})
            question_add.update({'Answer':addition})
            
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
            
        return lst_div

def question_with_text_exp(question_type, question_number, version = None ):
    if question_type == "addition":
        lst_add = []
        for i  in range(question_number):
            question_add = {}
            text, addition = random_question_generator_add()
            obj_extractor = numbers_and_object_extracor(text)
            ques,txt_explanation = text_explanation(addition,question_type,obj_extractor,version)
            question_add.update({'Question':ques})
            question_add.update({'Answer':addition})
            question_add.update({'Version':version})
            question_add.update({'question_type':question_type})
            question_add.update({'Objects':obj_extractor})
            question_add.update({'Text_Explanation':txt_explanation})
            lst_add.append(question_add)
        return lst_add
    
    elif question_type == "subtraction":
        lst_sub = []
        for i  in range(question_number):
            question_sub = {}
            text, difference = random_question_generator_subtract()
            obj_extractor = numbers_and_object_extracor(text)
            ques,txt_explanation = text_explanation(difference,question_type,obj_extractor,version)
            question_sub.update({'Question':ques})
            question_sub.update({'Answer':difference})
            question_sub.update({'Version':version})
            question_sub.update({'question_type':question_type})
            question_sub.update({'Objects':obj_extractor})
            question_sub.update({'Text_Explanation':txt_explanation})
            lst_sub.append(question_sub)  
        return lst_sub
    
    elif question_type == "multiplication":
        lst_multi = []
        for i  in range(question_number):
            question_multi = {}
            text, multiplication = random_question_generator_multi()
            question_multi.update({'Question':text})
            question_multi.update({'Answer':multiplication})
            obj_extractor = numbers_and_object_extracor(text)
            question_multi.update({'Objects':obj_extractor})
            txt_explanation = text_explanation(multiplication,question_type,obj_extractor)
            question_multi.update({'Text_Explanation':txt_explanation})
            lst_multi.append(question_multi)
            
        return lst_multi
    
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
            txt_explanation = text_explanation(quotient,question_type,obj_extractor)
            question_div.update({'Text_Explanation':txt_explanation})
            lst_div.append(question_div)
        return lst_div

############################################## Fahads Code-end #######################

################################################ number_and_object_extractor ###########
def numbers_and_object_extracor(question):
    doc = nlp(question)

    num_list = []
    object_list = []
    name_list = []
    dicts = {}

    for token in doc:
        
        if token.pos_ == "NUM": 
            num_list.append(token.text)  
        elif (token.pos_ == "PROPN" and token.dep_ == "dobj") or (token.pos_ == "NOUN" and token.dep_ == "dobj"):
            object_list.append(token.text) 
        elif (token.pos_ == "PROPN" and token.dep_ == "nsubj") or (token.pos_ == "PROPN" and token.dep_ == "pobj"):
            name_list.append(token.text)    
        else:
            pass  

    dicts['numbers'] = num_list
    dicts['objects'] = object_list 
    dicts['names'] = name_list  

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

    circle = [{"object":"tire","url":"https://i.ibb.co/594FR44/tire.png","object_type":"circle"},{"object":"plate","url":"https://i.ibb.co/3mzn20R/plate.png","object_type":"circle"}]

    triangle = [{"object":"hanger","url":"https://i.ibb.co/0FKqYRM/hanger.png","object_type":"triangle"},{"object":"green_cap","url":"https://i.ibb.co/hLj6tyy/green-cap.png","object_type":"triangle"},{"object":"blue_cap","url":"https://i.ibb.co/y5hyKRX/blue-cap.png","object_type":"triangle"}]

    square = [{"object":"mobile","url":"https://i.ibb.co/rpT2J3N/mobile.png","object_type":"square"},{"object":"window","url":"https://i.ibb.co/Htp0dWx/window.png","object_type":"square"},{"object":"book","url":"https://i.ibb.co/W09pRjn/book.png","object_type":"square"}]

    for i in range(number):
        rand_num = random.randint(1,3)
        if rand_num == 1:
            circle_obj += 1
            rand_num =  random.randint(0,1)
            value = copy.copy(circle[rand_num])
            value["count"] = circle_obj
            output_object_list.append(value)
        elif rand_num == 2:
            triangle_object += 1
            rand_num =  random.randint(0,2)
            value = copy.copy(triangle[rand_num])
            value["count"] = triangle_object
            output_object_list.append(value)
        else:
            square_object += 1
            rand_num =  random.randint(0,2)
            value = copy.copy(square[rand_num])
            value["count"] = square_object
            output_object_list.append(value)

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
        "fig":"https://i.ibb.co/qR5QHrZ/fig-01.png",
        "coli_points":['MOT','RON',1],
        "rays":['OR','OM','OS','OT','ON','OP',0],
        "line_seg":['OP','ON','OT','OS','OR','OM','MT','RN',1],
        "lines":['MT','RN',1]
    },
    {
        "fig":"https://i.ibb.co/02RfmFs/fig-02.png",
        "coli_points":['XOA',1],
        "rays":['OB','OA','OE','OD','OX','OC',0],
        "line_seg":['OB','OA','OE','OD','OX','OC','XA',1],
        "lines":['XA',1]
    },
    {
        "fig":"https://i.ibb.co/0MHSCZN/fig-03.png",
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
    

def naming_figures_single_question(numbers):
    question_list = []

    problem_list = [
    {
        "fig":"https://i.ibb.co/qR5QHrZ/fig-01.png",
        "coli_points":{"points":['MOT','RON'],"reverse":True},
        "rays":{"points":['OR','OM','OS','OT','ON','OP'],"reverse":False},
        "line_seg":{"points":['OP','ON','OT','OS','OR','OM','MT','RN'],"reverse":True},
        "lines":{"points":['MT','RN'],"reverse":True}
    },
    {
        "fig":"https://i.ibb.co/02RfmFs/fig-02.png",
        "coli_points":{"points":['XOA'],"reverse":True},
        "rays":{"points":['OB','OA','OE','OD','OX','OC'],"reverse":False},
        "line_seg":{"points":['OB','OA','OE','OD','OX','OC','XA'],"reverse":True},
        "lines":{"points":['XA'],"reverse":True}
    },
    {
        "fig":"https://i.ibb.co/0MHSCZN/fig-03.png",
        "coli_points":{"points":['BOD','AOC'],"reverse":True},
        "rays":{"points":['OE','OD','OC','OB','OA'],"reverse":False},
        "line_seg":{"points":['OE','OD','OC','OB','OA','BD','AC'],"reverse":True},
        "lines":{"points":['BD','AC'],"reverse":True}
    }]

    for num in range(numbers):
        random_question = random.randint(0,len(problem_list)-1)
        figure_components = ["Colinear Points", "Rays", "Line Segment","Lines"]
        key_list = ["coli_points","rays","line_seg","lines"]
        selected_fig_compnt = random.randint(0,3) 
        question = "Name "+str(figure_components[selected_fig_compnt])+" from the following figure" 
        question_dict = {
            "question": question,
            "figure": problem_list[random_question]["fig"],
            key_list[selected_fig_compnt]:problem_list[random_question][key_list[selected_fig_compnt]],
        }
        question_list.append(question_dict)
    return question_list  

@api_view(['GET'])
def naming_fig_single_ques(request):
    try:
        num_of_ques = int(request.META.get('HTTP_NUMBERS'))
        if num_of_ques > 0 :
            dict_data = naming_figures_single_question(num_of_ques)
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
            response_obj = ResponseClass(400, "no field called a and b")
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

################################## Random_Number_Generator_with_text_explanation_Section ######################
@api_view(['GET'])
def rand_ques_generator_with_text_explanation(request):
    try:
        
        question_number  = int(request.META.get('HTTP_A'))
        question_type    = request.META.get('HTTP_TYPE')
        question_version = request.META.get('HTTP_VERSION')

        if question_number>0 and question_number<11 and question_type or question_version:
            dict_data = question_with_text_exp(question_type, question_number,question_version)
            response_obj = ResponseClass(200, "Add Successful",dict_data)
            return JsonResponse(response_obj.__dict__, status=200)
        else:
            response_obj = ResponseClass(400, "question and question type cannot be empty,or zero, or greater than 10")
            return JsonResponse(response_obj.__dict__, status=400)
    except KeyError as e:
            response_obj = ResponseClass(400, "no field called question and question_type")
            return JsonResponse(response_obj.__dict__, status=400)   


################################## Random_Number_Generator_with_text_explanation_Section ends #################
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