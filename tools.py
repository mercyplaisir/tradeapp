import json
from json.decoder import JSONDecodeError
import os
import csv
from csv import Error





"""
functions in  this file:
                        - create_json
                        - rewrite_json
                        - append_json
                        - write_json
                        - read_json
                        - percent_calculator
                        - percent_change
                        - input_int
                        - input_str
                        - 

"""

FILESTORAGE = "./files/"


class Tool:


    @staticmethod
    def create_json(filename:str):
        assert filename.isalnum(),"Argument 'filename' doit etre alpha numeric"

        if os.path.exists(filename):
            print("le fichier existe deja")
            
        else:
            try:
                with open(f"{FILESTORAGE}/{filename}", "x") as f:
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
            with open(f"{FILESTORAGE}/{filename}", 'w') as f:
                j = json.dumps(text, indent=4)
                #os.remove(f"{FILESTORAGE}/{filename}")
                f.write(j)
        except FileNotFoundError:
            print(FileNotFoundError)
        except JSONDecodeError:#en cas d'erreur
            os.remove(filename)#efface le fichier
            Tool.create_json(filename)#creez en une autre de meme nom
            Tool.rewrite_json(filename,text)#et refait l'ecriture

    @staticmethod
    def append_json(filename ,text):
        """ append a json file

            give parameters:
                            - filename(and path)
                            - text to put in the file
                            
        
        """
        try:
            with open(f"{FILESTORAGE}/{filename}", 'r+') as f:
                i=[]
                j = json.load(f)
                i.append(j)
                i.append(text)
            with open(f"{FILESTORAGE}/{filename}", 'w+') as f:
                json.dump(i, f, indent=4)

            print(f"saved in {FILESTORAGE}/{filename}")
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
            with open(f"{FILESTORAGE}/{filename}", 'r+') as f:
                j = json.load(f)
            return j
        except FileNotFoundError:
            print(FileNotFoundError)
        except JSONDecodeError:
            print(JSONDecodeError)
        

    @staticmethod
    def percent_calculator(number: float, percentage: float) -> int:
        """
        return z = z + z*x/100
        ex: 100 + 2% =102
        """
        z = number+((number*percentage)/100)
        return z

    @staticmethod
    def percent_change( original_number: float, new_number: float) -> int:
        """
        percent variation between two numbers
        ex: 100 and 98 -> -2%
        """
        z = ((new_number-original_number)/original_number)*100
        return z

    @staticmethod
    def input_int(text):
        """
        for input integer only
        """
        while True:
            try:
                x=int(input(text))
                break
            except:
                pass
        return x

    @staticmethod
    def input_str(text):
        """
        for input string only
        """
        while True:
            try:
                x = str(input(text))
                break
            except:
                pass
        return x


    @staticmethod
    def write_csv(filename, text):
        """
        write a csv file
        """
        if os.path.exists(f"{FILESTORAGE}/{filename}"):
            try:
                with open(f"{FILESTORAGE}/{filename}","w", newline="") as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=" ")
                    spamwriter.writerows(text)
            except FileNotFoundError:
                print(FileNotFoundError)
            except FileExistsError:
                print(FileExistsError)
            except Error:
                print(Error)


    @staticmethod
    def read_csv(filename):
        """
        read a csv file.
        
        return a list of multilist containing rows
        """
        

        if os.path.exists(f"{FILESTORAGE}/{filename}"):
            try:
                
                with open(f"{FILESTORAGE}/{filename}", newline='') as csvfile:
                    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                    a = [row for row in spamreader]
                        #print(', '.join(row))
                #a.append(spamreader.__str__())

            except FileNotFoundError:
                print(FileNotFoundError)
            except Error:
                print(Error)

            return a

        else:
            #return "fichier n'existe pas"
            pass
            

        

        
