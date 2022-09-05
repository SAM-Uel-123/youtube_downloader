class validation:
    def valLink(link):
        if link:
            domains = ['https://www.youtube.com/', 'https://youtu.be/']
            for domain in domains:
                if domain in link:
                    if len( (link.replace(domain, '')) ) > 0:
                        return True
                
        return False


class input_validation:
    def inputValInt(msg= ''):
        valor = None
        while True:
            try:
                valor = int(input(msg))

            except:
                print('Valor errado.')
                continue
    
            else:
                return valor
        

    def inputValFloat(msg= ''):
        valor = None
        while True:
            try:
                valor = float(input(msg))

            except:
                print('Valor errado.')
                continue

            else:
                return valor

    def inputValString(msg= '', opcs = None, lower = 0, upper = 0):
        if not opcs:
            opcs = []
            
        valor = None

        while True:
            try:
               valor = str(input(msg))
               if valor in opcs:
                    if lower:
                        valor = valor.lower()

                    if upper:
                        valor = valor.upper()
                    
                    return valor


            except:
                print('Entrada invalida.')
                continue


            else:
                return valor


