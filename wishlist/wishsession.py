from products.models import Product
class Wishsession():
        
        #def __init__(self,request):
        def __init__(self,request):
                #super().__init__(*args, **kwargs)
                self.session = request.session
                wishsession = self.session.get('session_key')
                if 'session_key' not in request.session:
                        wishsession=self.session['session_key']={}
                
                self.wishsession=wishsession    
                
        def add(self,product):
                product_id=str(product.id)
                #Logic
                if product_id in self.wishsession:
                        pass
                else:
                        self.wishsession[product_id]={'productid':str(product.id)}
                self.session.modified=True
                
        # for count or quantity of items in session
        def __len__(self):
                return len(self.wishsession)
        
        #function for Wish list products in Session
        def wish_list_session(self):
                # get Ids of products from Session key that has create
                product_ids=self.wishsession.keys()
                #use the product_ids to lookup in DB
                products_in_session=Product.objects.filter(id__in=product_ids)
                
                return products_in_session
                
        #function delete fro wish list sess
        def delete_pro_sess(self,productid):
                product_id=str(productid)
                # Deleted from Dictionary wish list sess
                if product_id in self.wishsession:
                        del self.wishsession[product_id]
                self.session.modified = True