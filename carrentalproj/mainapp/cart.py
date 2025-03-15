class Cart(): 
    def __init__(self, request):
        self.session = request.session
        
        cart = self.session.get('session_key')
        
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        self.cart = cart
    
    
    def add(self, detail):
        detail_id = str(detail.id)
        
        if detail_id in self.cart:
            pass
        else:
            self.cart[detail_id] = {'hire_amount': str(detail.hire_amount)}
            
        self.session.modified = True
        
        
def __len__(self):
    return len(self.cart)