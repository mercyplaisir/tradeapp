import json




"""
functions in  this file:
                        
                        - write_json
                        - read_json
                        - percent_calculator
                        - percent_change

"""



BASECOIN ="BTC"







class Tool:

    @staticmethod
    def write_json(filename:str ,text):
        """ Write in a json file

            give parameters:
                            -filename(and path)
                            -text to put in the file
        
        """

        with open(f'./{filename}', 'r') as f:
            j = json.load(f)
            j.append(text)
        with open(f'./{filename}', 'w') as f:
            json.dump(j, f, indent=4)

        print(f"saved in {filename} ")

    
    @staticmethod
    def read_json(filename:str):
        """
        read a json file

        give parameters:
                        -filename(with path)
        """
        with open(f'./{filename}', 'r') as f:
            j = json.load(f)
        
        return j


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
    
