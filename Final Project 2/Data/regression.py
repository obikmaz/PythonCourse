
import numpy as np
import pandas as pd
from scipy import stats


def reg(x,y):    
    betas = est_coeff(x,y)
    sd = beta_sd(x,y)
    confidence_intervals = conf_interval(x,y)
    x1 = np.array(x).transpose()
    n = x1.shape[0]
    k = x1.shape[1]
    variable_list = listwise_deletion(x,y)
    significance = ttests(x,y)
    error = error_calc(x,y) # y - y_estimates
    y = variable_list[1]        
    

    #calculating SSE
    error2 = error**2
    e2 = np.array(error2)
    sse = np.sum(e2)
    
    #calculating SSR
    y_estimates = -1*(error - y)
    ssr = np.sum(((y_estimates-np.average(y))**2))
   
    #calculating MSR
    df_reg = k
    msr = ssr/df_reg
    
    #calculating MSE
    df_res = n - k - 1
    mse = sse/df_res
    
    #calculating F-stats
    F_stats = msr/mse
    
    #model significance
    model_p = 1-stats.f.cdf(F_stats,df_reg,df_res)
    
    #calculating R^2
    R_2 = ssr/(sse+ssr)
    
    #calculating adjusted R^2
    adj_r = 1 - ((1-R_2)*(n - 1)/(n-k-1))
    
    print("Model Summary")
    print("------------------------------------------------")
    print("n = " + str(n))
    print("Model significance= " + str(model_p))
    print("R^2 = " + str(R_2))
    print("Adjusted R^2 = " + str(adj_r))
    print("------------------------------------------------")
    

    
    return  pd.concat([betas,sd,confidence_intervals,significance], axis=1)


def listwise_deletion(x,y):
    #listwise deletion 
    x = np.array(x).transpose()
    y = np.array(y).transpose()
    y = pd.DataFrame(y)
    x = pd.DataFrame(x)    
    z = pd.concat([x,y], axis=1)    
    z = z.dropna()
    
    #Creating matrix for variables 
    x = np.array(z.iloc[:,:-1])
    n = len(x)
    y = np.array(z.iloc[:,-1]).reshape(n,1)        
    ax = np.ones(n).reshape(n,1) #initialize matrix with 1s for intercept
    x = np.concatenate([ax,x], axis=1) #create x matrix
    return x, y

def est_coeff(x,y):            
    variable_list = listwise_deletion(x,y)
    x = variable_list[0]
    y = variable_list[1]
    
    #Estimation of betas
    first_part = np.linalg.inv(x.transpose()@x)
    second_part = first_part@x.transpose()
    betas = second_part@y
    
    #create beta list
    beta_list = []
    for i in betas:
        beta_list.append(float(i))
    
    return pd.DataFrame(beta_list, columns = ["Coefficients"])

def y_estimator(x,y):
    betas = est_coeff(x,y)
    betas = np.array(betas)
    variable_list = listwise_deletion(x,y)
    x = variable_list[0]
    return x@betas

def error_calc(x,y):
    y_estimates = y_estimator(x,y)
    variable_list = listwise_deletion(x,y)
    y = variable_list[1]
    return y - y_estimates

def variance(x,y):
    error = error_calc(x,y)
    variable_list = listwise_deletion(x,y)
    x = variable_list[0]
    y = variable_list[1]
    n = x.shape[0]
    k = x.shape[1] - 1
    return (error.transpose()@error)/(n-k-1)

def beta_sd(x,y):
    var = variance(x,y)
    variable_list = listwise_deletion(x,y)
    x = variable_list[0]
    y = variable_list[1]  
    variances = var*(np.linalg.inv(x.transpose()@x))
    k = x.shape[1]
    
    #extract variances
    var_list = []
    for i in range(k):
        var_list.append(variances[i,i])
    
    var_list = np.array(var_list)
    sd_list = np.sqrt(var_list)    
    return pd.DataFrame(sd_list, columns = ["Standard Errors"])

def conf_interval(x,y):
    betas = est_coeff(x,y)
    betas = np.array(betas)
    sd = beta_sd(x,y)
    sd = np.array(sd)
    
    #Z distribution was used to estimate confidence intervals
    lower_tails = []
    for i,k in zip(sd,betas):
        lower_tails.append(k - (1.96*i))
    
    upper_tails = []
    for i,k in zip(sd,betas):
        upper_tails.append(k + (1.96*i))  


    a = pd.DataFrame(lower_tails, columns = ["Lower 95%"])
    b = pd.DataFrame(upper_tails, columns = ["Upper 95%"])
    return pd.concat([a,b], axis=1)

def ttests(x,y):
    betas = est_coeff(x,y)
    betas = np.array(betas)
    sd = beta_sd(x,y)
    sd = np.array(sd)
    variable_list = listwise_deletion(x,y)
    x = variable_list[0]
       
    tstats = []
    for i,k in zip(sd,betas):
        a = k/i
        tstats.append(k/i)

    tstats = np.array(tstats)
    #calculating p-values
    df = x.shape[0] - x.shape[1] - 1
    
    p_values = []
    for i in range(len(tstats)):
        p_values.append(1-stats.t.cdf(tstats[i],df=df))
  
    a = pd.DataFrame(tstats, columns = ["t-stats"])
    b = pd.DataFrame(p_values, columns = ["p-value"])
    return pd.concat([a,b], axis=1)
    

    
    


    
    
    
    
    


