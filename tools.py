import json
from json.decoder import JSONDecodeError
import os
import csv






"""
functions in  this file:
                        
                        - write_json
                        - read_json
                        - percent_calculator
                        - percent_change
                        - input_int
                        - input_str

"""




class Tool:


    @staticmethod
    def create_json(filename):
        if os.path.exists(filename):
            print("le fichier existe deja")
            
        else:
            try:
                with open(f"./{filename}", "x") as f:
                    i = []
                    j = json.dumps(i)
                    f.write(j)
            except FileNotFoundError:
                print(FileNotFoundError)
            except JSONDecodeError:
                print(JSONDecodeError)
    @staticmethod
    def rewrite_json(filename, text):
        try:
            with open(f'{filename}', 'w+') as f:
                j = json.dumps(text)
                f.write(j)
        except FileNotFoundError:
            print(FileNotFoundError)
        except JSONDecodeError:
            print(JSONDecodeError)

    @staticmethod
    def append_json(filename ,text):
        """ append a json file

            give parameters:
                            - filename(and path)
                            - text to put in the file
                            
        
        """
        try:
            with open(f'{filename}', 'r+') as f:
                i=[]
                j = json.load(f)
                i.append(j)
                i.append(text)
            with open(f'{filename}', 'w+') as f:
                json.dump(i, f, indent=4)

            print(f"saved in {filename} ")
        except FileNotFoundError:
            print(FileNotFoundError)
        except JSONDecodeError:
            print(JSONDecodeError)
    
    @staticmethod
    def read_json(filename:str):
        """
        read a json file

        give parameters:
                        -filename(with path)
        """
        try:
            with open(f'{filename}', 'r+') as f:
                j = json.load(f)
            return j
        except FileNotFoundError:
            print(FileNotFoundError)
        except JSONDecodeError:
            print(JSONDecodeError)
        

    @staticmethod
    def percent_calculator(number: float, percentage: float):
        """
        calcule d'un nombre par rapport a un pourcentage du nombre d'origine
        """
        z = number+((number*percentage)/100)
        return z

    @staticmethod
    def percent_change( original_number: float, new_number: float):
        """
        variation du prix en pourcentage entrer 2nombres
        """
        z = ((new_number-original_number)/original_number)*100
        return z

    @staticmethod
    def input_int(text):
        """veuiller entrez un texte qui sera affiche"""
        while True:
            try:
                x=int(input(text))
                break
            except:
                pass
    
    @staticmethod
    def input_str(text):
        """veuiller entrez un texte qui sera affiche"""
        while True:
            try:
                x = str(input(text))
                break
            except:
                pass
    
    @staticmethod
    def write_csv(filename, text):
        with open(f"{filename}","w", newline="") as csvfile:
            spamwriter = csv.writer(filename, delimiter=" ")
            spamwriter.writerows(text)