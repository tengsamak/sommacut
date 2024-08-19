from products.models import Product, Variants,Images
import decimal
from django.contrib import messages
#for Cartsession with variant
class Cartsession():
        
        #def __init__(self,request):
        def __init__(self,request):
                #super().__init__(*args, **kwargs)
                self.session = request.session
                cartsession = self.session.get('cartsess_key')
                if 'cartsess_key' not in request.session:
                        cartsession=self.session['cartsess_key']={}
                
                self.cartsession=cartsession    
#for Cartsession with variant

        #for product with no_variant        
        def add(self,product,qty):
                product_id=str(product.id)
                product_qty=int(qty)
                #Logic
                if product_id in self.cartsession:
                        pass
                else:
                        self.cartsession[product_id]=int(qty)
                                # {
                                # 'productid':str(product.id),
                                # 'qty':product_qty,
                                # }
                self.session.modified=True
        #for product with no_variant        
        # def add_no_var(self,product,qty):
        #         product_id=str(product.id)
        #         product_qty=int(qty)
        #         #Logic
        #         if product_id in self.cartsession:
        #                 pass
        #         else:
        #                 self.cartsession[product_id]=int(qty)
        #                         # {
        #                         # 'productid':str(product.id),
        #                         # 'qty':product_qty,
        #                         # }
        #         self.session.modified=True        
        
        # with cart with Variant        
        def add_var(self,product,qty,varid):
                product_id=int(product)
                product_qty=int(qty)
                variant_id=int(varid)
                #Logic
                if product_id in self.cartsession:
                        pass
                else:
                        self.cartsession[product_id]={
                                'productid':int(product),
                                'qty':product_qty,
                                'variant_id':int(varid),
                                }
                                #int(qty)
                self.session.modified=True
                        
                
        # for count or quantity of items in session
        def __len__(self):
                return len(self.cartsession)
        
        #function for Cart list products in Session
        def cart_list_session_var(self):
                # get Ids of products from Session key that has create
                product_ids=self.cartsession.keys()
                get_sess_items=self.cartsession.items()
                get_sess_items_value=self.cartsession.values()
                # print("Get keys:",product_ids)
                # print("Get values:",get_sess_items_value)
                # print("Get items:",get_sess_items)
                #z=[]
                y=[]
                for x in get_sess_items_value:
                        #z.append(str(x['qty']))
                        y.append(str(x['variant_id']))
                        # print("x:",x.get('variant_id'))                       
                # print("x:",type(get_sess_items_value))
                # print("Y:",y)
                # print("Z:",z)
                #get_pid_varid={'32','43','48'}
                get_pid_varid=y
               
                #print("sess pro items Ids",get_sess_items)
                
                #use the product_ids to lookup in DB
                products_in_session=Product.objects.filter(id__in=product_ids)
                var_session=Variants.objects.filter(id__in=get_pid_varid,product__in=product_ids)
                #var_session=Variants.objects.filter(id__in=y,product__in=product_ids)
                #images_session=Images.objects.filter(product__in=product_ids)
                #print("var:",var_session)
                data_session=[
                        products_in_session,
                        var_session,
                        #images_session,
                ]        
                
                
                return var_session
                
                #return data_session
        # def cart_list_session_no_var(self):
        #         # get Ids of products from Session key that has create
        #         product_ids=self.cartsession.keys()
        #         get_sess_items=self.cartsession.items()
        #         get_sess_items_value=self.cartsession.values()
               
               
        #         #print("sess pro items Ids",get_sess_items)
                
        #         #use the product_ids to lookup in DB
        #         products_in_session=Product.objects.filter(id__in=product_ids)
        #         #var_session=Variants.objects.filter(id__in=get_pid_varid,product__in=product_ids)
        #         #var_session=Variants.objects.filter(id__in=y,product__in=product_ids)
        #         #images_session=Images.objects.filter(product__in=product_ids)
        #         #print("var:",var_session)
        #         data_session=[
        #                 products_in_session,
        #                 #var_session,
        #                 #images_session,
        #         ]        
                
                
        #         return products_in_session
                
        #function delete fro wish list sess
        def delete_pro_sess(self,productid):
                product_id=str(productid)
                # Deleted from Dictionary wish list sess
                if product_id in self.cartsession:
                        del self.cartsession[product_id]
                self.session.modified = True
                
        # def get_qty_no_var(self):
        #         qty= self.cartsession
        #         return qty
        
        def get_qty_var(self):
                qty_var= self.cartsession.values()
                y=[]
                z=[]
                for x in qty_var:
                        #get list to z for product id
                        z.append(str(x['productid']))
                        #print("z",z)
                        #get list to y for qty 
                        y.append(x['qty'])
                        #print("y",y)
                        # print("x:",x['qty'])  
                # zip list z and list y together        
                thisdict1 = zip(z, y)
                #convert list to dict
                thisdict=dict(thisdict1)
                #print("new Y:",dict(thisdict))
                return thisdict
        def get_var_qty(self):
                #Get start
                ourcart_var=self.cartsession.values()
                # qty_var= self.cartsession.values()
                y=[]
                z=[]
                for x in ourcart_var:
                        #get list to z for product id
                        z.append(str(x['variant_id']))
                        #print("z",z)
                        #get list to y for qty 
                        y.append(x['qty'])
                # zip list z and list y together        
                thisdict1 = zip(z, y)
                #convert list to dict
                thisdict=dict(thisdict1)
                #print("new Y:",dict(thisdict))
                return thisdict
                
                
                #update dictionary of Cart no var
                # ourcart_var[_pid] = _qty  
                # self.session.modified=True
                # thing=self.cartsession_no_var
                # return thing
        def updatecart_var(self,newdict):
                # Note: 'cartsess_key': {'9': {'productid': 9, 'qty': 3, 'variant_id': 43}, '13': {'productid': 13, 'qty': 1, 'variant_id': 20}, '15': {'productid': 15, 'qty': 1, 'variant_id': 27}}
                
                #Get start
                ourcart_var=self.cartsession
                
                # ourcart_var['7']['qty']=2
                # ourcart_var['9']['qty']=3
                # ourcart_var['13']['qty']=4
                # self.session.modified=True
                #ourcart_var[9]['qty']
                for x,y in newdict.items():
                        for z,t in ourcart_var.items():
                                #print("x:z**:",str(x),x,z)
                                if x==z:
                                        ourcart_var[x]['qty']=y
                                        self.session.modified=True
                #update dictionary of Cart no var
                # ourcart_no_var[_pid] = _qty  
                # self.session.modified=True
                thing=self.cartsession
                return thing
        def get_total_var(self):
                # get Ids of products from Session key that has create
                product_ids=self.cartsession.keys()
                quantity=self.cartsession
                #for get varid
                get_sess_items_value=self.cartsession.values()
                y=[]
                for x in get_sess_items_value:
                        #z.append(str(x['qty']))
                        y.append(str(x['variant_id']))
                get_varid=y
                # Note: 'cartsess_key': {'9': {'productid': 9, 'qty': 3, 'variant_id': 43}, '13': {'productid': 13, 'qty': 1, 'variant_id': 20}, '15': {'productid': 15, 'qty': 1, 'variant_id': 27}}
                #use the product_ids to lookup in DB
                products_in_session=Variants.objects.filter(id__in=get_varid,product_id__in=product_ids)
                total=0
                for pid,qty in quantity.items():
                        pid=int(pid)
                        print("pid",pid)
                        for var in products_in_session:
                                print("var pid:",var.product_id)
                                if pid == int(var.product_id) :
                                        print("pid var_pid:",pid,var.product.id)
                                        print("qty:",qty['qty'])
                                        total += float(var.price) * int(qty['qty']) 
                                        
                total_var=total   
                print("total_var:",total_var)             
                return total_var
        def check_pid_in_cart_var(self,pid):
                pid=int(pid)
                check=False
                yourcart_no_var=self.cartsession
                for x in yourcart_no_var.keys():
                        if int(x) == pid :
                                check=True
                                print("Your Product already in Cart session")
                                #messages.info("Your Product already in Cart session")
                        else:
                                check
                                print("Add to Cart session")
                                #messages.info("Add to Cart session")
                return check
        
#Cartsession no_var        
class Cartsession_no_var():
        
        #def __init__(self,request):
        def __init__(self,request):
                #super().__init__(*args, **kwargs)
                self.session = request.session
                cartsession_no_var = self.session.get('cartsess_key_no_var')
                if 'cartsess_key_no_var' not in request.session:
                        cartsession_no_var=self.session['cartsess_key_no_var']={}
                
                self.cartsession_no_var=cartsession_no_var  
         #for product with no_variant        
        def add_no_var(self,product,qty):
                product_id=str(product.id)
                product_qty=int(qty)
                #Logic
                if product_id in self.cartsession_no_var:
                        pass
                else:
                        self.cartsession_no_var[product_id]=int(qty)
                                # {
                                # 'productid':str(product.id),
                                # 'qty':product_qty,
                                # }
                self.session.modified=True    
        # for count or quantity of items in session
        def __len__(self):
                return len(self.cartsession_no_var)
        
        def cart_list_session_no_var(self):
                # get Ids of products from Session key that has create
                product_ids=self.cartsession_no_var.keys()
                
                #use the product_ids to lookup in DB
                products_in_session=Product.objects.filter(id__in=product_ids)
                #var_session=Variants.objects.filter(id__in=get_pid_varid,product__in=product_ids)
                #var_session=Variants.objects.filter(id__in=y,product__in=product_ids)
                #images_session=Images.objects.filter(product__in=product_ids)
                #print("var:",var_session)

                return products_in_session
        
        def get_qty_no_var(self):
                qty= self.cartsession_no_var
                return qty
        
        def delete_pro_sess_no_var(self,productid):
                product_id=str(productid)
                # Deleted from Dictionary wish list sess
                if product_id in self.cartsession_no_var:
                        del self.cartsession_no_var[product_id]
                self.session.modified = True
                
                
        def updatecart_no_var(self,newdict):
                #_newdict=newdict
                # _pid=str(pid)    
                # _qty=str(qty) 
                # Note:'cartsess_key_no_var': {'8': 2, '16': 2}
                
                #Get start
                ourcart_no_var=self.cartsession_no_var
                for x,y in newdict.items():
                        for z in ourcart_no_var:
                                if x==z :
                                        ourcart_no_var[z]=y
                                        print("UdateFC_No_var: z:y=",ourcart_no_var[z],y)
                                        self.session.modified=True
                                        
                #update dictionary of Cart no var
                # ourcart_no_var[_pid] = _qty  
                # self.session.modified=True
                thing=self.cartsession_no_var
                return thing
        
        def get_total_no_var(self):
                # get Ids of products from Session key that has create
                product_ids=self.cartsession_no_var.keys()
                quantity=self.cartsession_no_var
                #cartsess_key_no_var': {'8': '1'}
                #use the product_ids to lookup in DB
                products_in_session=Product.objects.filter(id__in=product_ids)
                total=0
                for pid,qty in quantity.items():
                        pid=int(pid)
                        qty=int(qty)
                        for product in products_in_session:
                                if pid == product.id :
                                        total += float(product.price) * qty 
                                        
                total_no_var=total                
                return total_no_var
        
        def check_pid_in_cart_no_var(self,pid):
                pid=int(pid)
                check=False
                yourcart_no_var=self.cartsession_no_var
                for x in yourcart_no_var.keys():
                        if int(x) == pid :
                                check=True
                                print("Your Product already in Cart session")
                                #messages.info("Your Product already in Cart session")
                        else:
                                check
                                print("Add to Cart session")
                                #messages.info("Add to Cart session")
                return check
        