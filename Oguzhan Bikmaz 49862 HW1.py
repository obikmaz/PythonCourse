# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import datetime

import random
 
class Portfolio(object):
    def __init__(self):
        self.cash = 0
        self.mutualfundlist = {}
        self.stocklist = {}
        self.transaction = []
        
        
    def pluscash(self,other):
        self.cash = self.cash + other
        self.transaction.append(str(datetime.datetime.now()) + "     "+ "$" +str(other)+" added")
        return self.cash
    def minuscash(self,other): 
        self.cash = self.cash - other
        self.transaction.append(str(datetime.datetime.now()) + "     "+ "$" +str(other)+" withdrawn")
        return self.cash
    
    def __str__(self):
        return "{" + str(self.cash) + "," + str(self.mutualfundlist) + "," + str(self.stocklist) + "}"
    
    def plusmutualfund(self,quantity,mfname):
        mf_name = mfname.getmfname
        if self.cash < quantity : 
            return "insufficent funds" 
        else:
           if type(quantity) == float:               
               if mf_name in self.mutualfundlist:
                   self.mutualfundlist[mf_name] += quantity
                   self.cash = self.cash - quantity
                   self.transaction.append(str(datetime.datetime.now()) + "     "+ str(quantity) + " unit " + str(mf_name)+" purchased")
               else:
                   self.mutualfundlist[mf_name] = 0
                   self.mutualfundlist += quantity
                   self.cash -= quantity
                   self.transaction.append(str(datetime.datetime.now()) + "     "+ str(quantity) + " unit " + str(mf_name)+" purchased")
           else:
               print("Mutual funds can only be purchased as fractional shares.")
    def sellmutualfund(self,quantity, mfname):
        mf_name = mfname.getmfname
        p = random.uniform(0.9,1.2) * quantity
        try:
            self.mutualfundlist[mf_name] = self.mutualfundlist[mf_name] - p
            self.cash = self.cash + p
            return self.mutualfundlist[mf_name]
            self.transaction.append(str(datetime.datetime.now()) + "     "+ str(quantity) + " unit " + str(mf_name)+" sold")
            
        except: 
            print ("you do not have this mutualfund kind")
    
    def plusstock(self,amount,stock):
        p = stock.getprice()
        s = stock.getname()
        if type(amount) == int:
            if self.cash < amount*p: 
                return "insufficent funds" 
            else:
                if s in self.stocklist:
                    self.stocklist[s] += p*amount
                    self.cash = self.cash - p*amount
                    self.transaction.append(str(datetime.datetime.now()) + "     "+ str(amount) + " shares " + str(s)+" purchased")
                else:
                    self.stocklist[s] = 0
                    self.stocklist[s] += p*amount
                    self.cash = self.cash - p*amount
                    self.transaction.append(str(datetime.datetime.now()) + "     "+ str(amount) + " shares " + str(s)+" purchased")
        else: 
            print("stock can only be purchased as whole units.")
            
    def sellstock(self,amount,stock):
        p = stock.getprice()
        s = stock.getname()
        random1 = random.uniform(0.5,1.5)*p
        if type(amount) ==int:
            try:
                self.stocklist[s] = self.stocklist[s] - random1*amount
                self.cash = self.cash + random1*amount
                return self.stocklist[s]
                self.transaction.append(str(datetime.datetime.now()) + "     "+ str(amount) + " shares " + str(s)+" sold")
            except: 
                print ("you do not have this mutualfund kind")
        else:
            print("stock can only be sold as whole units.")
    def history(self):
        for l in self.transaction:
            print (l)
class mutualfund(Portfolio):
    def __init__(self,mfname):
        self.mfname = mfname
    def getmfname(self):
        return self.mfname
    def __str__(self):
        return "#" + str(self.mfname)
    
class stock(Portfolio):
    def __init__(self, price, stockname):
        self.price = price
        self.stockname = stockname 
    def getprice(self):
        return self.price
    def getname(self):
        return self.stockname
    def __str__(self):
        return "#" + str(self.stockname) + " " + str(self.price) 

class Bond(Portfolio):
    
    def __init__ (self,bondkind):
        self.bondkind = bondkind
    def getbondkind(self):
        return self.bondkind
    def __str__(self):
        return str(self.bondkind)
    
        
oguz = Portfolio()
mf1= mutualfund ("KLM")
mf2= mutualfund ("QWE")
s1= stock (5,"ISBANK")
s2 = stock(7,"ASLSN")
oguz.plusstock(10,s1)
oguz.plusmutualfund(11,mf2)

oguz.pluscash(1000)

oguz.plusstock(10,s1)
oguz.plusmutualfund(11,mf2)

oguz.sellstock(3,s1)
oguz.sellmutualfund(7,mf2)


oguz.plusstock(5,s2)
oguz.plusmutualfund(9,mf1)

print (oguz)

oguz.history()

